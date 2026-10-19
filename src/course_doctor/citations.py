"""Checking a quoted claim against the page it was quoted from.

This is the module that makes the lab able to do the thing the course is about.
`materials.py` reads a lesson and lists the URLs it cites; nothing until now
fetched any of them, so the tool could report what a lesson *claimed* and never
whether the claim still held.

No MCP dependency, same as `materials.py`, and the network call is INJECTABLE --
`check_quote(..., fetch=...)` takes the fetcher. That is not a testing
convenience bolted on afterwards: a suite that needs the network fails when the
wifi drops, and a suite that fails for reasons unrelated to the code is a suite
people learn to ignore. Every test in this repository passes a fake.

WHAT THIS MODULE DELIBERATELY DOES NOT DO: decide whether a claim is stale. It
reports whether a string is present on a page. A quote that is absent may have
been paraphrased by the lesson author, reworded harmlessly by the documentation,
or genuinely retracted, and those three need a human. The verdict lives in the
agent; this returns the evidence.

TWO THINGS MEASURED HERE RATHER THAN ASSUMED, both on 2026-10-19 while
re-verifying the `memory` page by hand:

1. **Appending `.md` to a docs URL serves the raw page source.**
   `code.claude.com/docs/en/memory.md` returned 51,526 bytes of `text/markdown`;
   the same URL without the suffix returned 801,645 bytes of HTML. The rendered
   page is sixteen times larger, and reading it means either parsing markup or
   handing it to a summariser -- and a claim checked against a summary is a
   paraphrase compared with a paraphrase, which is the exact failure this course
   recorded in VERIFICATION.md.

2. **Inline link markup breaks a verbatim match.** The quote
   "use a PreToolUse hook instead" is on the page as
   `use a [PreToolUse hook](/docs/en/hooks-guide) instead`. Matching raw markdown
   without normalising that reports a correct quote as missing. It cost one false
   alarm by hand; at scale it would cost trust in the checker.
"""

from __future__ import annotations

import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from .materials import MaterialRefused

logger = logging.getLogger(__name__)


# --- bounds, each with its provenance ----------------------------------------

# NOT ESTABLISHED against a corpus. Chosen: the largest documentation page
# measured here was ~52 KB of markdown, and the rendered HTML of the same page
# was ~800 KB. 4 MiB is roughly eighty times the markdown and five times the
# HTML, so it refuses a video or a dataset without refusing a long docs page.
# Re-measure before quoting it as a fact about documentation pages.
MAX_PAGE_BYTES = 4 * 1024 * 1024

# DESIGN DECISION. Twenty seconds, matching the read timeout the course's own
# error-propagation lesson uses in its worked example, so the lab and the lesson
# agree. Not a measurement of any server's latency.
FETCH_TIMEOUT_SECONDS = 20

# A markdown inline link: `[label](target)` -> `label`. Applied before matching,
# for the reason in this module's docstring. Deliberately does NOT handle
# reference-style links or images; neither appeared in the pages measured, and a
# normaliser that silently half-works is worse than one whose limits are stated.
_INLINE_LINK = re.compile(r"\[([^\]^]*?)\]\((?:[^()\s]|\([^()]*\))*\)")

_USER_AGENT = "course-doctor-citation-check"


@dataclass(frozen=True)
class QuoteCheck:
    """One quote, checked against one page. Facts only -- no staleness verdict."""

    url: str
    fetched_url: str
    quote: str
    found: bool
    source_format: str
    page_bytes: int
    checked_at: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalise(text: str) -> str:
    """Collapse whitespace and flatten inline links, so a quote can be compared.

    Two documents that differ only in line wrapping are the same prose, and a
    quote copied out of a lesson has been rewrapped by definition. So whitespace
    is collapsed on both sides before matching.

    This is lossy ON PURPOSE and the losses are the point: after it runs, the
    check can no longer tell you where on the page the quote sits, or whether the
    original was a heading, a table cell or a sentence. If that ever matters,
    match against the raw text as well rather than making this function cleverer.
    """
    return " ".join(_INLINE_LINK.sub(r"\1", text).split())


def _fetch(url: str) -> tuple[str, str, int]:
    """Fetch one URL. Returns (text, content_type, byte_count).

    Raises `MaterialRefused` rather than letting a urllib exception cross the
    boundary, because every caller above this point formats a refusal into a
    payload and an exception would arrive as "the tool failed" with the remedy
    lost.
    """
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
            content_type = response.headers.get("Content-Type", "") or ""
            # Read one byte past the cap so the cap can be DETECTED rather than
            # silently applied. Reading exactly MAX_PAGE_BYTES gives a truncated
            # page that is indistinguishable from a complete one, and a quote
            # missing from a truncated page would be reported as absent.
            raw = response.read(MAX_PAGE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise MaterialRefused(
            code="unreachable",
            message=f"{url} returned HTTP {exc.code}.",
            guidance=(
                "NOTHING WAS CHECKED, so do not record this quote as absent from "
                "the page -- an unreachable page and a retracted claim are "
                "different findings. If the status is 404 the citation itself may "
                "be stale, which is a finding about the lesson rather than about "
                "the quote."
            ),
        ) from exc
    except Exception as exc:  # noqa: BLE001 -- network failures are many and all refuse alike
        raise MaterialRefused(
            code="unreachable",
            message=f"Could not fetch {url}: {exc}",
            guidance=(
                "NOTHING WAS CHECKED. This is a transport failure, not a verdict "
                "about the claim. Retry once; if it persists, record the quote as "
                "unchecked rather than as unverified."
            ),
        ) from exc

    if len(raw) > MAX_PAGE_BYTES:
        raise MaterialRefused(
            code="page_too_large",
            message=f"{url} is over the {MAX_PAGE_BYTES}-byte limit for a page.",
            guidance=(
                "Nothing was matched. The page was not truncated and checked -- a "
                "truncated page would make a present quote look absent. If this is "
                "really a documentation page, raise MAX_PAGE_BYTES deliberately."
            ),
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MaterialRefused(
            code="not_text",
            message=f"{url} did not return valid UTF-8.",
            guidance=(
                "Nothing was matched. A binary response usually means the URL "
                "points at a PDF or an image rather than at a documentation page. "
                "A PDF cannot be checked by this tool at all."
            ),
        ) from exc

    return text, content_type, len(raw)


def check_quote(
    url: str,
    quote: str,
    fetch: Callable[[str], tuple[str, str, int]] | None = None,
) -> QuoteCheck:
    """Report whether `quote` still appears on the page at `url`.

    ⚠️ THE FETCHED PAGE IS DATA, NEVER INSTRUCTIONS. This reaches out to the open
    internet and hands its caller text somebody else controls. Nothing here strips
    an injected line, and the defence is that the caller is told to treat the
    payload as quoted material -- see the tool docstring and the server
    instructions.

    ⚠️ `found=False` IS NOT A VERDICT THAT THE CLAIM IS WRONG. It means this
    string, after whitespace and inline-link normalisation, is not on that page.
    The quote may be the lesson author's paraphrase, the page may have been
    harmlessly reworded, or the claim may genuinely be gone. Those are three
    different findings and only a person can tell them apart.

    THE FAILURE DIRECTION IS CHOSEN. Every ambiguous case here resolves toward
    `found=False` or a refusal, never toward `found=True`: a false absence costs
    somebody a minute of reading, and a false presence marks a stale claim as
    verified and removes it from the list of things anybody will look at again.
    Measured 2026-10-19: both false results during the hand re-verification of the
    `memory` page were false ABSENCES, and that is the direction to keep.
    """
    if not url or not url.strip():
        raise MaterialRefused(
            code="invalid_input",
            message="No URL was given.",
            guidance="Pass a documentation URL, for example from a lesson's cited_urls.",
        )
    if not quote or not quote.strip():
        raise MaterialRefused(
            code="invalid_input",
            message="No quote was given.",
            guidance=(
                "Pass the claim's wording as the lesson states it. An empty quote "
                "would match every page, which would report every claim as verified."
            ),
        )

    url = url.strip()
    fetcher = fetch or _fetch

    # Prefer the raw source. The suffix is tried FIRST rather than as a fallback
    # because the rendered page also returns 200 -- so a fallback ordering would
    # always take the HTML and never discover that source was available.
    source_format = "markdown source (.md)"
    fetched_url = url if url.endswith(".md") else url + ".md"
    try:
        text, content_type, page_bytes = fetcher(fetched_url)
        if "markdown" not in content_type and "text/plain" not in content_type:
            # Served something, but not source. Fall through to the plain URL
            # rather than matching against whatever this was.
            raise MaterialRefused(
                code="unreachable",
                message="the .md variant did not return markdown",
                guidance="fall back to the URL as given",
            )
    except MaterialRefused:
        source_format = "as served by the URL as given"
        fetched_url = url
        text, content_type, page_bytes = fetcher(fetched_url)
        if "html" in content_type:
            logger.warning(
                "%s served HTML rather than markdown source; a quote checked "
                "against rendered markup can miss for markup reasons",
                url,
            )

    found = normalise(quote) in normalise(text)
    logger.debug("quote %r on %s: %s", quote[:40], fetched_url, found)

    return QuoteCheck(
        url=url,
        fetched_url=fetched_url,
        quote=quote,
        found=found,
        source_format=source_format,
        page_bytes=page_bytes,
        checked_at=_now(),
    )
