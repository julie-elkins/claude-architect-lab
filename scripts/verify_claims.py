#!/usr/bin/env python3
"""Re-check every machine-checkable claim in the course, and lead with the coverage.

WHAT WAS MISSING, AND WHY THIS IS THE GAP RATHER THAN THE SCHEDULE.
`course_doctor.citations.check_quote` has been able to re-fetch a page and demand a
claim's verbatim wording back since 2026-10-19. Nothing drove it. The six re-verified
pages in VERIFICATION.md were done by calling the MCP tool by hand, one quote at a time,
inside a session. So the check existed and the loop did not, and a loop nobody can run
unattended is a procedure rather than automation.

THE COVERAGE FIGURE IS THE HEADLINE, NOT A FOOTNOTE, and that is the whole design.
MEASURED 2026-10-19: of 335 claim rows in this course, **36 are machine-checkable** --
about 11%. The other 299 split two ways and neither is a defect:

  - **205 cite the exam guide**, which is a PDF. `check_quote` reads pages. A change to
    the guide is caught by `check_exam_guide.py`; whether a specific claim survived that
    change is not, and cannot be from here.
  - **94 cite a documentation URL but state the claim as a PARAPHRASE.** "The hierarchy
    is user-level, project-level, and directory-level" is the lesson author's sentence,
    not the documentation's, so there is no exact string to look for. A human re-reads
    those or nothing does.

**A report that said "all claims verified" over 11% of them would be this repository's
own failure mode committed against itself** -- a clean result read as a complete one. So
the coverage fraction is printed first, every run, before any result.

THE QUOTE THRESHOLD, and it is robust rather than tuned. A claim counts as checkable when
it contains a double-quoted run of at least `--min-quote` characters; shorter quoted runs
are usually identifiers (`"tool_use"`) and an identifier found on a page is weak evidence
that a claim survived. MEASURED 2026-10-19: the count is **flat at 36 for every threshold
from 10 to 30**, and only falls at 40 (33) and 60 (27). So 36 is not an artefact of the
default -- it is what the corpus contains across a 3x range of the parameter. Re-measure
if the authoring convention changes.

"COULD NOT CHECK" IS NEVER "PASSED". A failed fetch exits 2, which outranks a missing
quote's exit 1, because an incomplete run is a worse thing to report than a known finding.
A run that cannot reach the network must not look like a run that found nothing wrong.

AND `found=False` IS NOT A VERDICT. It means the string is not on the page after
normalisation. The documentation may have been harmlessly reworded, the lesson may have
drifted into paraphrase, or the claim may be gone. Those are three findings and only a
person separates them -- so this script reports and never edits a lesson.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from datetime import date

REPO = pathlib.Path(__file__).resolve().parent.parent
COURSE = REPO / "course"
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

from course_doctor.citations import check_quote  # noqa: E402
from course_doctor.materials import MaterialRefused  # noqa: E402

SOURCES_HEADING = re.compile(r"^## Sources\s*$", re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(?P<claim>[^|]+)\|(?P<source>[^|]+)\|\s*$", re.MULTILINE)
EG_REF = re.compile(r"EG\s*§\s*\d")
URL = re.compile(r"https?://[^\s)\]]+")

# DESIGN DECISION. See the module docstring: the count is insensitive to this between
# 10 and 30, so the default sits in the middle of the flat region rather than at an end.
DEFAULT_MIN_QUOTE = 25


# A quote carrying an ellipsis was STITCHED from two places on the page, so it cannot
# match verbatim no matter what the page says. MEASURED 2026-10-19: 4 of the first 9
# not-found results were this, and every one of them would have fired on every future run.
# An alarm that cannot be cleared trains whoever reads it to ignore the ones that can be,
# so these are classified NOT CHECKABLE rather than NOT FOUND. Both the ASCII and the
# typographic form, because the corpus contains both.
STITCHED = re.compile(r"\.\.\.|…")


def quoted_run(claim: str, min_length: int) -> tuple[str | None, str | None]:
    """The longest usable double-quoted run in a claim, or why there isn't one.

    Returns `(quote, reason_it_is_unusable)` — exactly one of the two is set.
    """
    runs = [m.group(1) for m in re.finditer(r'"([^"]+)"', claim)]
    long_enough = [r for r in runs if len(r) >= min_length]
    if not long_enough:
        return None, "stated as a paraphrase, no exact string to match"

    whole = [r for r in long_enough if not STITCHED.search(r)]
    if not whole:
        return None, (
            "quote is stitched across an ellipsis, so it cannot match verbatim — "
            "record one contiguous span instead"
        )
    return max(whole, key=len), None


def lessons() -> list[pathlib.Path]:
    """Lesson files from the guide manifest, so the two cannot disagree."""
    import build_guide

    seen: list[str] = []
    for _ts, _title, rel in build_guide.MANIFEST:
        if rel not in seen:
            seen.append(rel)
    return [COURSE / rel for rel in seen]


class Row:
    __slots__ = ("lesson", "claim", "source", "url", "quote", "reason")

    def __init__(self, lesson, claim, source, url, quote, reason):
        self.lesson, self.claim, self.source = lesson, claim, source
        self.url, self.quote, self.reason = url, quote, reason


def collect(min_quote: int) -> list[Row]:
    rows: list[Row] = []
    for path in lessons():
        text = path.read_text(encoding="utf-8")
        head = SOURCES_HEADING.search(text)
        if not head:
            continue
        name = str(path.relative_to(REPO))
        for match in TABLE_ROW.finditer(text[head.start():]):
            claim = match.group("claim").strip()
            source = match.group("source").strip()
            if not claim or claim.lower() == "claim" or set(claim) <= set("-: "):
                continue

            found_url = URL.search(source)
            if not found_url:
                # Exam-guide-only rows. Not a defect: see the module docstring.
                reason = (
                    "cites the exam guide (a PDF)"
                    if EG_REF.search(source)
                    else "cites no URL"
                )
                rows.append(Row(name, claim, source, None, None, reason))
                continue

            url = found_url.group(0).rstrip(".,;:)]`")
            quote, reason = quoted_run(claim, min_quote)
            rows.append(Row(name, claim, source, url, quote, reason))
    return rows


def caching_fetcher(fetch_one=None):
    """Fetch each URL at most once per run, and reuse it across every claim on it.

    Not only a speed-up. Several claims cite the same page -- the `memory` page carries
    22 of them -- so fetching per claim would hit one host 22 times in a few seconds and
    invite a rate limit, which this script would then have to report as "could not
    check" for reasons it caused itself.
    """
    if fetch_one is None:
        from course_doctor.citations import _fetch

        fetch_one = _fetch

    cache: dict[str, tuple] = {}
    errors: dict[str, str] = {}

    def fetch(url: str):
        if url in errors:
            raise MaterialRefused(
                code="unreachable", message=errors[url],
                guidance="Already failed once this run; not retried.",
            )
        if url not in cache:
            try:
                cache[url] = fetch_one(url)
            except Exception as exc:  # noqa: BLE001 - recorded, then re-raised
                errors[url] = str(exc)
                raise
        return cache[url]

    fetch.cache = cache
    return fetch


def main(argv=None, fetch_one=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--min-quote", type=int, default=DEFAULT_MIN_QUOTE)
    parser.add_argument(
        "--out", type=pathlib.Path, default=None,
        help="also write the report here. A result is data rather than console output, "
             "so a scheduled run should always pass this",
    )
    parser.add_argument(
        "--offline", action="store_true",
        help="report coverage and check nothing. Exits 2, because a run that checked "
             "nothing has not passed",
    )
    args = parser.parse_args(argv)

    rows = collect(args.min_quote)
    checkable = [r for r in rows if r.quote]
    total = len(rows)

    lines = [
        f"# Claim verification — {date.today().isoformat()}",
        "",
        f"**Coverage: {len(checkable)} of {total} claim rows are machine-checkable "
        f"({100 * len(checkable) / total:.1f}%).**",
        "",
        "This report covers only those. It says nothing about the rest, and the rest is "
        "the majority. Read the breakdown below before treating any of this as a "
        "statement about the course.",
        "",
    ]

    reasons: dict[str, int] = {}
    for row in rows:
        if row.reason:
            reasons[row.reason] = reasons.get(row.reason, 0) + 1
    lines.append("## Why the rest is not checkable here")
    lines.append("")
    for reason, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
        lines.append(f"- **{count} rows** — {reason}")
    lines.append("")

    found: list[Row] = []
    missing: list[Row] = []
    failed: list[tuple[Row, str]] = []

    if args.offline:
        lines += ["## Checked", "", "Nothing. `--offline` was passed.", ""]
    else:
        fetch = caching_fetcher(fetch_one)
        for row in checkable:
            try:
                result = check_quote(row.url, row.quote, fetch=fetch)
            except MaterialRefused as refused:
                failed.append((row, refused.message))
                continue
            except Exception as exc:  # noqa: BLE001 - a fetch problem is a finding
                failed.append((row, str(exc)))
                continue
            (found if result.found else missing).append(row)

        lines += [
            "## Checked",
            "",
            f"- **{len(found)} verbatim match** — the page still carries the claim's "
            "exact wording",
            f"- **{len(missing)} NOT FOUND** — the string is not on the page after "
            "normalisation",
            f"- **{len(failed)} could not be checked** — a fetch failed, so these are "
            "neither pass nor fail",
            f"- pages fetched: {len(getattr(fetch, 'cache', {}))}",
            "",
        ]

        if missing:
            lines += [
                "### Not found — each needs a person, not an edit",
                "",
                "`found=False` is not a verdict that the claim is wrong. The page may "
                "have been harmlessly reworded, the lesson may have drifted into "
                "paraphrase, or the claim may be gone. Three findings; only a human "
                "separates them.",
                "",
            ]
            for row in missing:
                lines.append(f"- `{row.lesson}`  \n  {row.url}  \n  quote: \"{row.quote}\"")
            lines.append("")

        if failed:
            lines += ["### Could not check", ""]
            for row, why in failed:
                lines.append(f"- `{row.lesson}` — {row.url} — {why}")
            lines.append("")

    lines += [
        "## What this report does not show",
        "",
        "- Whether the **exam guide** still supports the 205 rows that cite it. "
        "`check_exam_guide.py` notices the guide changing; it does not read it.",
        "- Whether a **paraphrased** claim is still true. Nothing automated can.",
        "- Whether a lesson **teaches** a claim correctly. A verbatim match proves the "
        "page says it, not that the lesson explains it right — one lesson here once "
        "taught a documented failure mode backwards while citing the correct page.",
        "",
    ]

    report = "\n".join(lines)
    print(report)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report + "\n", encoding="utf-8")
        print(f"\nwritten to {args.out.relative_to(REPO)}", file=sys.stderr)

    if args.offline:
        print("\nOFFLINE: nothing was checked. This is not a pass.", file=sys.stderr)
        return 2
    if failed:
        # Outranks a missing quote on purpose: an incomplete run is worse to report than
        # a known finding, because you do not know what it would have found.
        print(f"\n{len(failed)} claim(s) could not be checked.", file=sys.stderr)
        return 2
    if missing:
        print(f"\n{len(missing)} claim(s) not found on their cited page.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
