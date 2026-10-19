#!/usr/bin/env python3
"""Re-check every claim in the course at the strongest tier available, and never pool them.

WHAT WAS MISSING, AND WHY THIS IS THE GAP RATHER THAN THE SCHEDULE.
`course_doctor.citations.check_quote` has been able to re-fetch a page and demand a claim's
verbatim wording back since 2026-10-19. Nothing drove it: the six re-verified pages in
VERIFICATION.md were done by calling the MCP tool by hand, one quote at a time, inside a
session. The check existed and the loop did not, and a loop nobody can run unattended is a
procedure rather than automation.

EVERY CLAIM HAS A MECHANISM. THEY ARE NOT EQUALLY STRONG. That is the whole design, and
reporting one blended number would destroy it:

  - **GUIDE** — the claim cites the exam guide, a *static* PDF at a fixed version. Covered
    by `check_exam_guide.py`, which records the published guide's address and byte hash. If
    the hash holds, the guide says exactly what it said when the claim was written, so the
    claim cannot have silently drifted. This is STRONGER than a per-claim check, because it
    covers the whole document rather than one sentence per claim. What it does NOT give is
    independent verification: it preserves whatever state existed, and for most of these
    rows that state is "authored from one read, never re-checked".
  - **VERBATIM** — the claim carries a contiguous quoted span of documentation prose. The
    page is re-fetched and must still contain it. The strongest per-claim evidence here.
  - **IDENTIFIER** — the claim carries no quotable prose but does name a distinctive symbol
    (`--strict-mcp-config`, `${VAR:-default}`). The page must still contain the symbol.
    **This is deliberately weak**: it catches a rename or a removal and nothing else. A page
    that still mentions `--fork-session` has not thereby confirmed anything about what the
    flag does. Rename-and-removal is a real and probably the commonest drift mode on a
    product shipping monthly, which is why it is worth having -- and why it is reported on
    its own row and never added to the verbatim count.
  - **UNCOVERED** — a paraphrase of documentation prose with no distinctive symbol in it.
    Nothing automated can check these. They need a recorded supporting quote, or a person.

**A report claiming "all claims verified" over a tenth of them would be this repository's own
failure mode committed against itself**, so the per-tier table prints before any result.

TWO MEASURED CALIBRATIONS, both of which cut against the obvious implementation:

1. **The quote threshold is robust rather than tuned.** MEASURED 2026-10-19: the
   verbatim-checkable count is FLAT at 36 for every minimum quote length from 10 to 30, and
   only falls at 40 (33) and 60 (27). So the figure is what the corpus contains across a 3x
   range of the parameter, not an artefact of the default.
2. **Most backticked tokens are too common to be evidence.** MEASURED 2026-10-19: of 140
   distinct identifiers in paraphrased rows, 56 were bare words — `Bash`, `Edit`, `Read`,
   `Glob`, `agent`, `allow`, `"block"`, `-p`. "The page still contains the word Read" is not
   a check. Requiring a structural marker or internal capital drops those and keeps 84,
   taking the tier from 66 rows of noise-and-signal to 52 of signal.

A STITCHED QUOTE IS NOT A FINDING, IT IS AN AUTHORING BUG. A quote joined across an ellipsis
cannot match verbatim however the page reads, so reporting it NOT FOUND fires on every future
run, and an alarm nobody can clear teaches the reader to ignore the ones they can. Measured:
4 of the first 9 not-found results were exactly this, and when the fragments were tested
separately, 3 of the 4 matched the page on BOTH sides of the ellipsis -- so nothing had
drifted at all.

"COULD NOT CHECK" IS NEVER "PASSED". A failed fetch exits 2, outranking a finding's exit 1,
because an incomplete run is worse to report than a known result.

AND `found=False` IS NOT A VERDICT. The documentation may have been harmlessly reworded, the
lesson may have drifted into paraphrase, or the claim may be gone. Three findings; only a
person separates them. This script reports and never edits a lesson.
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
BACKTICKED = re.compile(r"`([^`]+)`")

# See calibration 1 in the module docstring. The default sits in the middle of the flat
# region rather than at either end of it.
DEFAULT_MIN_QUOTE = 25

# See the module docstring: a quote spanning an ellipsis cannot match verbatim.
STITCHED = re.compile(r"\.\.\.|…")

# A distinctive identifier carries a structural marker or an internal capital. See
# calibration 2: without this, the tier fills with bare words whose presence on a page
# proves nothing.
STRUCTURAL = re.compile(r"[-_./${}:=]|\(\)")
INTERNAL_CAPITAL = re.compile(r"[a-z][A-Z]")
MIN_IDENTIFIER = 3

TIERS = ("GUIDE", "VERBATIM", "IDENTIFIER", "UNCOVERED")


def quoted_run(claim: str, min_length: int) -> tuple[str | None, str | None]:
    """The longest usable contiguous quoted run, or why there isn't one.

    Returns `(quote, reason_it_is_unusable)` — exactly one of the two is set.
    """
    runs = [m.group(1) for m in re.finditer(r'"([^"]+)"', claim)]
    long_enough = [r for r in runs if len(r) >= min_length]
    if not long_enough:
        return None, "no quoted span"

    whole = [r for r in long_enough if not STITCHED.search(r)]
    if not whole:
        return None, (
            "quote is stitched across an ellipsis, so it cannot match verbatim — "
            "record one contiguous span instead"
        )
    return max(whole, key=len), None


def identifiers(claim: str) -> list[str]:
    """Distinctive backticked symbols in a claim, deduplicated and order-preserving.

    Reduced to the leading whitespace-delimited token, so `--resume <name>` and
    `--resume <transcript-path>` both become `--resume`. Checking the whole backticked
    string would fail on a page that documents the same flag with a different
    placeholder, which is a difference in the DOCS' notation rather than a change to the
    thing being claimed.
    """
    found: dict[str, None] = {}
    for match in BACKTICKED.finditer(claim):
        raw = match.group(1).strip().strip("\"'")
        if not raw:
            continue
        token = raw.split()[0]

        # Truncate at a placeholder. MEASURED 2026-10-19:
        # `.claude/skills/<name>/SKILL.md` is absent from the skills page while
        # `.claude/skills/` is present -- the docs write the same path with different
        # notation, so matching the templated form reports a rename that did not happen.
        # Two of the first three IDENTIFIER misses were this. The stem is weaker evidence
        # and still catches the thing this tier is for: the directory being renamed away.
        if "<" in token:
            token = token.split("<", 1)[0]

        if len(token) < MIN_IDENTIFIER:
            continue
        if STRUCTURAL.search(token) or INTERNAL_CAPITAL.search(token):
            found.setdefault(token, None)
    return list(found)


def lessons() -> list[pathlib.Path]:
    """Lesson files from the guide manifest, so the two cannot disagree."""
    import build_guide

    seen: list[str] = []
    for _ts, _title, rel in build_guide.MANIFEST:
        if rel not in seen:
            seen.append(rel)
    return [COURSE / rel for rel in seen]


class Row:
    __slots__ = ("lesson", "claim", "source", "url", "tier", "quote", "symbols", "note")

    def __init__(self, lesson, claim, source, url, tier, quote=None, symbols=(), note=None):
        self.lesson, self.claim, self.source, self.url = lesson, claim, source, url
        self.tier, self.quote, self.symbols, self.note = tier, quote, list(symbols), note


def collect(min_quote: int = DEFAULT_MIN_QUOTE) -> list[Row]:
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
                note = None if EG_REF.search(source) else "cites no URL and no guide section"
                rows.append(Row(name, claim, source, None, "GUIDE", note=note))
                continue

            url = found_url.group(0).rstrip(".,;:)]`")
            quote, why = quoted_run(claim, min_quote)
            if quote:
                rows.append(Row(name, claim, source, url, "VERBATIM", quote=quote))
                continue

            symbols = identifiers(claim)
            if symbols:
                rows.append(Row(name, claim, source, url, "IDENTIFIER", symbols=symbols,
                                note=why))
                continue

            rows.append(Row(name, claim, source, url, "UNCOVERED", note=why))
    return rows


def caching_fetcher(fetch_one=None):
    """Fetch each URL at most once per run, and reuse it across every claim on it.

    Not only a speed-up. The `memory` page alone carries 22 claim rows, so fetching per
    claim would hit one host 22 times in a few seconds and invite a rate limit that this
    script would then have to report as "could not check" for a reason it caused itself.
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
        help="report the tier table and check nothing. Exits 2, because a run that "
             "checked nothing has not passed",
    )
    args = parser.parse_args(argv)

    rows = collect(args.min_quote)
    total = len(rows)
    by_tier = {tier: [r for r in rows if r.tier == tier] for tier in TIERS}

    lines = [
        f"# Claim verification — {date.today().isoformat()}",
        "",
        "**Every claim row has a freshness mechanism. They are not equally strong, and "
        "these counts are deliberately never added together.**",
        "",
        "| Rows | Tier | What it establishes |",
        "|---|---|---|",
        f"| {len(by_tier['GUIDE'])} | GUIDE | the exam guide is a static PDF; "
        "`check_exam_guide.py` watches its bytes, so no cited claim can have silently "
        "drifted. Not independent verification. |",
        f"| {len(by_tier['VERBATIM'])} | VERBATIM | the cited page still contains the "
        "claim's exact quoted wording. Strongest per-claim evidence here. |",
        f"| {len(by_tier['IDENTIFIER'])} | IDENTIFIER | the cited page still contains a "
        "distinctive symbol the claim names. **Catches rename and removal only.** |",
        f"| {len(by_tier['UNCOVERED'])} | UNCOVERED | nothing automated can check these. "
        "A recorded supporting quote would move them to VERBATIM. |",
        f"| **{total}** | total | |",
        "",
    ]

    notes: dict[str, int] = {}
    for row in rows:
        if row.note:
            notes[row.note] = notes.get(row.note, 0) + 1
    if notes:
        lines += ["## Why a row is not at a stronger tier", ""]
        for note, count in sorted(notes.items(), key=lambda kv: -kv[1]):
            lines.append(f"- **{count} rows** — {note}")
        lines.append("")

    verbatim_ok: list[Row] = []
    verbatim_miss: list[Row] = []
    symbol_ok: list[Row] = []
    symbol_miss: list[tuple[Row, list[str]]] = []
    failed: list[tuple[Row, str]] = []

    if args.offline:
        lines += ["## Checked", "", "Nothing. `--offline` was passed.", ""]
    else:
        fetch = caching_fetcher(fetch_one)

        for row in by_tier["VERBATIM"]:
            try:
                result = check_quote(row.url, row.quote, fetch=fetch)
            except Exception as exc:  # noqa: BLE001 - a fetch problem is a finding
                failed.append((row, str(exc)))
                continue
            (verbatim_ok if result.found else verbatim_miss).append(row)

        for row in by_tier["IDENTIFIER"]:
            gone: list[str] = []
            broke = None
            for symbol in row.symbols:
                try:
                    if not check_quote(row.url, symbol, fetch=fetch).found:
                        gone.append(symbol)
                except Exception as exc:  # noqa: BLE001
                    broke = str(exc)
                    break
            if broke:
                failed.append((row, broke))
            elif gone:
                symbol_miss.append((row, gone))
            else:
                symbol_ok.append(row)

        lines += [
            "## VERBATIM tier",
            "",
            f"- **{len(verbatim_ok)} still exact**",
            f"- **{len(verbatim_miss)} NOT FOUND**",
            "",
            "## IDENTIFIER tier — rename and removal only",
            "",
            f"- **{len(symbol_ok)} symbols all still present**",
            f"- **{len(symbol_miss)} rows name a symbol the page no longer contains**",
            "",
            "A row passing here has NOT had its claim verified. The symbol exists; what "
            "the claim says about it is unchecked.",
            "",
            f"Could not be checked at all: **{len(failed)}** — neither pass nor fail. "
            f"Pages fetched: {len(getattr(fetch, 'cache', {}))}.",
            "",
        ]

        if verbatim_miss:
            lines += [
                "### VERBATIM not found — each needs a person, not an edit",
                "",
                "`found=False` is not a verdict that the claim is wrong. The page may have "
                "been reworded harmlessly, the lesson may have drifted into paraphrase, or "
                "the claim may be gone. Only a human separates those.",
                "",
            ]
            for row in verbatim_miss:
                lines.append(f"- `{row.lesson}`  \n  {row.url}  \n  quote: \"{row.quote}\"")
            lines.append("")

        if symbol_miss:
            lines += ["### IDENTIFIER missing — a rename or a removal", ""]
            for row, gone in symbol_miss:
                lines.append(f"- `{row.lesson}`  \n  {row.url}  \n  gone: {', '.join(gone)}")
            lines.append("")

        if failed:
            lines += ["### Could not check", ""]
            for row, why in failed:
                lines.append(f"- `{row.lesson}` — {row.url} — {why}")
            lines.append("")

    lines += [
        "## What this report does not show",
        "",
        "- Whether a **GUIDE**-tier claim is a correct reading of the guide. The hash "
        "proves the guide has not changed, not that the claim was right when written.",
        "- Whether an **IDENTIFIER**-tier claim is true. A symbol still existing says "
        "nothing about what it does.",
        "- Whether an **UNCOVERED** paraphrase is still true. Nothing automated can.",
        "- Whether a lesson **teaches** any claim correctly. A verbatim match proves the "
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
        # Outranks a finding on purpose: an incomplete run is worse to report than a known
        # result, because you do not know what it would have found.
        print(f"\n{len(failed)} row(s) could not be checked.", file=sys.stderr)
        return 2
    if verbatim_miss or symbol_miss:
        print(
            f"\n{len(verbatim_miss)} verbatim miss(es), {len(symbol_miss)} missing "
            "symbol(s).", file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
