#!/usr/bin/env python3
"""Notice when the published exam guide changes. Nothing else in this repo can.

WHY THIS IS THE BIGGEST HOLE IT CLOSES. The exam guide is the source of most of this
course's claim rows, and it is the one source the citation checker cannot touch: it is a
PDF, not a page, so `check_citations.py --urls` has never looked at it and the verbatim
re-check in `course_doctor.citations` has no way to read it. `VERIFICATION.md` has said
so in its own words — *"the exam guide is not verifiable from here"*. This script does
not make it verifiable. It makes a CHANGE to it impossible to miss, which is a different
and much cheaper claim.

WHAT IT WATCHES, and why two things rather than one. The guide is reached through the
certification page, and the PDF sits on a storage URL carrying a generated path segment.
So either can move independently:

  1. **The link on the page** — a new upload gets a new path. The address changing is by
     itself evidence that something was republished.
  2. **The bytes behind the link** — the same address serving different content.

Either one means: go and read the guide, and treat every exam-guide-cited row as
unverified until you have.

WHAT IT DELIBERATELY DOES NOT DO:

- **It does not parse the PDF.** It hashes it. A hash answers "did this change", which is
  the only question worth automating here; *what* changed is a judgement and belongs to a
  person reading the new guide. This is the same split `course_doctor.materials` already
  uses, and it has a second benefit worth naming: content nobody interprets cannot carry
  an instruction aimed at whoever reads it.
- **It does not extract the version string.** That would need a PDF parser, which is a new
  dependency for a weaker signal than the hash already gives. Accepted ceiling: when this
  fires, you learn the guide moved and not which version it moved to.
- **It does not decide anything.** A changed guide may not touch a single claim in this
  course. That comparison is the re-read.

"COULD NOT CHECK" IS NEVER "UNCHANGED". Every failure path — page unreachable, no PDF link
found, download refused — exits non-zero and says so. A network failure that exited 0
would make an unchecked guide read exactly like an unchanged one, which is the failure this
whole repository is about.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

REPO = pathlib.Path(__file__).resolve().parent.parent
BASELINE = REPO / "data" / "exam-guide-baseline.json"

# The stable address. SOURCES.md cites this page rather than the PDF for the same reason
# this script starts here: the page is the published entry point and the storage URL is
# not promised to be durable.
CERT_PAGE = (
    "https://anthropic-partners.skilljar.com/"
    "claude-certified-architect-foundations-certification"
)

# MEASURED 2026-10-19: the exam guide PDF is 628,815 bytes. 8 MiB is roughly thirteen
# times that, so it refuses a video or a dataset served from a redirected link without
# refusing a guide that grew several times over. NOT a finding about how big exam guides
# get -- it is a bound chosen against one measurement.
#
# An earlier draft of this comment said "614,100 bytes", from a tool that reported
# 614.1 KiB. Same file, different unit. The near-miss is worth keeping: a size recorded
# in the wrong unit would have made the very first run of this check report a change
# that had not happened, and a tripwire whose first act is a false alarm gets switched off.
MAX_PDF_BYTES = 8 * 1024 * 1024

# Seconds. DESIGN DECISION, not measured: long enough that a slow CDN is not reported as
# a missing guide, short enough that a hung socket does not look like a running check.
TIMEOUT = 30

# An `https` link ending in `.pdf`.
PDF_LINK = re.compile(r"""https://[^\s"'<>)\\]+?\.pdf""")

# The guide this course is written against, as the decoded filename. MEASURED 2026-10-19:
# the certification page carries NINE exam-guide PDFs, so a match on "exam guide" alone is
# not identifying -- it returns all four certifications plus a Japanese edition of each.
# Pinning the exact filename is what makes this check about THIS exam.
#
# Note the EN DASH (U+2013). The English guides use it; the Japanese editions use a plain
# hyphen and carry a parenthetical. That is incidental rather than a rule, which is why
# this matches a declared filename instead of inferring the language from punctuation.
EXPECTED_GUIDE = "Claude Certified Architect – Foundations Exam Guide.pdf"

# Links arrive twice on this page: once as HTML and once inside embedded JSON, where a
# hyphen is written `-`. Unescaping before matching is not cosmetic -- the escaped
# copy sorts FIRST, so a check that took the first candidate would record a baseline
# against a URL that cannot be fetched at all.
JSON_ESCAPE = re.compile(r"\\u([0-9a-fA-F]{4})")

USER_AGENT = "course-doctor-exam-guide-check/1.0 (+https://github.com/julie-elkins/claude-architect-lab)"


class CheckFailed(Exception):
    """A failure that must not be reported as a clean result."""

    def __init__(self, state: str, message: str, guidance: str) -> None:
        super().__init__(message)
        self.state = state
        self.message = message
        self.guidance = guidance


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch(url: str, *, limit: int) -> bytes:
    """Fetch up to `limit` bytes, or raise. Replaced wholesale in tests.

    Injected rather than monkeypatched, same as `course_doctor.citations`: a suite that
    needs the network fails when the wifi drops, and a suite that fails for reasons
    unrelated to the code is a suite people learn to ignore.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        # Read one byte past the limit so an oversized body is detected rather than
        # silently truncated into a hash of its first 8 MiB -- which would be a stable,
        # confident, wrong digest.
        body = response.read(limit + 1)
    if len(body) > limit:
        raise CheckFailed(
            "REFUSED",
            f"{url} returned more than {limit} bytes.",
            "Nothing was hashed. Check the link actually points at the guide; a bound "
            "this high is usually hit by a redirect to something that is not a PDF.",
        )
    return body


def find_guide_link(page_html: str) -> str:
    """The exam-guide PDF link on the certification page.

    Raises rather than returning None. A missing link is not "no change" -- it means the
    page was restructured and this check no longer knows where to look, which needs a
    person.
    """
    unescaped = JSON_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), page_html)

    candidates = [
        url
        for match in PDF_LINK.finditer(unescaped)
        for url in [match.group(0)]
        if urllib.parse.unquote_plus(url).endswith(EXPECTED_GUIDE)
    ]

    unique = list(dict.fromkeys(candidates))
    if not unique:
        raise CheckFailed(
            "LINK_NOT_FOUND",
            f"No link to {EXPECTED_GUIDE!r} found on the certification page.",
            "The page was restructured, the guide was renamed, or it was withdrawn. All "
            "three need a person, and NONE of them is evidence the guide is unchanged. "
            "Open the page, find the guide, and re-record the baseline against it.",
        )
    if len(unique) > 1:
        raise CheckFailed(
            "AMBIGUOUS_LINK",
            f"{len(unique)} links match {EXPECTED_GUIDE!r}: {unique}",
            "Two addresses for one filename means this check cannot tell which is "
            "current. Pick it by hand and record the baseline against that URL.",
        )
    return unique[0]


def measure(fetcher=fetch) -> dict[str, object]:
    """Fetch the page, find the guide, hash it. Returns the current observation."""
    try:
        page = fetcher(CERT_PAGE, limit=MAX_PDF_BYTES).decode("utf-8", errors="replace")
    except CheckFailed:
        raise
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise CheckFailed(
            "UNREACHABLE",
            f"Could not reach the certification page: {exc}",
            "Nothing was checked. This is not a pass. Re-run when the network is "
            "available; if the page is gone rather than unreachable, that is a finding "
            "about the certification program and needs a person.",
        ) from exc

    pdf_url = find_guide_link(page)

    try:
        pdf = fetcher(pdf_url, limit=MAX_PDF_BYTES)
    except CheckFailed:
        raise
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise CheckFailed(
            "UNREACHABLE",
            f"Found the guide link but could not download it: {exc}",
            "Nothing was hashed. The link moving is itself worth noticing -- compare the "
            "URL below against the recorded baseline before assuming this is transient.",
        ) from exc

    return {
        "pdf_url": pdf_url,
        "sha256": hashlib.sha256(pdf).hexdigest(),
        "byte_count": len(pdf),
        "checked_at": _now(),
    }


def load_baseline() -> dict[str, object] | None:
    if not BASELINE.is_file():
        return None
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def compare(baseline: dict[str, object] | None, current: dict[str, object]) -> tuple[str, list[str]]:
    """Return (state, findings). State is UNCHANGED only when both signals match."""
    if baseline is None:
        return "NO_BASELINE", [
            "No baseline recorded, so there is nothing to compare against.",
            "Run with --record to establish one. Until then this check cannot fire.",
        ]

    findings = []
    if baseline.get("pdf_url") != current["pdf_url"]:
        findings.append(
            "THE LINK MOVED.\n"
            f"  was: {baseline.get('pdf_url')}\n"
            f"  now: {current['pdf_url']}\n"
            "  A new path usually means a new upload."
        )
    if baseline.get("sha256") != current["sha256"]:
        findings.append(
            "THE BYTES CHANGED.\n"
            f"  was: {baseline.get('sha256')} ({baseline.get('byte_count')} bytes)\n"
            f"  now: {current['sha256']} ({current['byte_count']} bytes)"
        )

    return ("CHANGED" if findings else "UNCHANGED"), findings


def record(current: dict[str, object]) -> None:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--record",
        action="store_true",
        help="Write the current observation as the new baseline. Deliberately manual: "
        "an automatic refresh would overwrite the evidence that something changed.",
    )
    args = parser.parse_args(argv)

    try:
        current = measure()
    except CheckFailed as failed:
        print(f"{failed.state}: {failed.message}\n\n{failed.guidance}", file=sys.stderr)
        return 2

    baseline = load_baseline()
    state, findings = compare(baseline, current)

    if args.record:
        record(current)
        print(f"Baseline recorded: {BASELINE.relative_to(REPO)}")
        print(f"  url    {current['pdf_url']}")
        print(f"  sha256 {current['sha256']}")
        print(f"  bytes  {current['byte_count']}")
        if state == "CHANGED":
            print("\nNOTE: this overwrote a DIFFERENT baseline. What changed:")
            for finding in findings:
                print(f"  {finding}")
        return 0

    if state == "NO_BASELINE":
        print("NO_BASELINE: " + " ".join(findings), file=sys.stderr)
        return 2

    if state == "CHANGED":
        print("EXAM GUIDE CHANGED\n")
        for finding in findings:
            print(finding + "\n")
        print(
            "WHAT THIS DOES AND DOES NOT TELL YOU.\n"
            "  It tells you the published guide is not the one this course was written\n"
            "  against. It does NOT tell you what moved, or whether any claim in this\n"
            "  course is affected -- this check does not read the PDF.\n\n"
            "WHAT TO DO.\n"
            "  Read the new guide. Until you have, treat every exam-guide-cited row in\n"
            "  the course as unverified, and check the version string in SOURCES.md\n"
            "  against the guide's own section 18 version history. Then --record."
        )
        return 1

    print(f"UNCHANGED: guide matches the recorded baseline ({current['sha256'][:12]}).")
    print(f"  checked {current['checked_at']}")
    print(
        "  This compares the published PDF against a recorded hash. It does not\n"
        "  re-verify any claim against the guide's contents."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
