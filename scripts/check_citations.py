#!/usr/bin/env python3
"""Check that every lesson's claims are cited, and that the citations are usable.

Why this exists: `SOURCES.md` and the per-lesson claim tables were hand-maintained,
so nothing failed when a lesson made an uncited claim. A verification procedure
that never fires reads exactly like one that passes — which is the failure this
course is about, committed by the course.

What it CAN check, mechanically:

- every lesson in the build manifest has a `## Sources` section
- every claim-table row names a source
- every source is either an exam-guide reference (`EG §n`) or an `https://` URL
- every URL-cited row carries a read date, because a live link is not a verified
  claim — pages get rewritten under the same URL
- outstanding items are declared as unchecked boxes rather than omitted

What it CANNOT check, and this is the important limit: **whether the cited page
still says what the row claims.** That needs something to read both. It is the
`verify-course-content` skill's job, and `--urls` here only reports whether a URL
still resolves — which is strictly weaker and must not be mistaken for the real
check.

Run `--urls` manually. It needs the network, so it is deliberately not in the unit
suite: a test that fails when the wifi drops teaches people to ignore the suite.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
COURSE = REPO / "course"

SOURCES_HEADING = re.compile(r"^## Sources\s*$", re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(?P<claim>[^|]+)\|(?P<source>[^|]+)\|\s*$", re.MULTILINE)
EG_REF = re.compile(r"EG\s*§\s*\d")
URL = re.compile(r"https?://[^\s)\]]+")
READ_DATE = re.compile(r"read\s+\d{4}-\d{2}-\d{2}")
UNCHECKED = re.compile(r"^\s*- \[ \]", re.MULTILINE)

VERIFICATION = REPO / "VERIFICATION.md"
# The verified-pages table in VERIFICATION.md. Matched on a backticked URL in the
# first cell of a row whose later cells carry a read date, so prose mentioning a URL
# elsewhere in that file cannot promote a page to verified by accident.
VERIFIED_ROW = re.compile(
    r"^\|\s*`(?P<url>https?://[^`]+)`\s*\|[^|]*(?P<date>\d{4}-\d{2}-\d{2})[^|]*\|",
    re.MULTILINE,
)


def normalise(url: str) -> str:
    """Trim trailing punctuation and markdown that rides along in a citation."""
    return url.rstrip("`.,;:)\"'").rstrip("/")


def verified_pages() -> dict[str, str]:
    """URL -> re-verification date, from VERIFICATION.md.

    A MISSING file means zero verified pages, not an error. That direction is
    deliberate: deleting the record must make the course look LESS verified, never
    more. The same reasoning applies to a page nobody remembered to add — an
    unlisted page is reported as outstanding, so the count understates coverage
    rather than flattering it.
    """
    if not VERIFICATION.is_file():
        return {}
    text = VERIFICATION.read_text(encoding="utf-8")
    return {
        normalise(m.group("url")): m.group("date")
        for m in VERIFIED_ROW.finditer(text)
    }


def lessons() -> list[tuple[str, pathlib.Path]]:
    """Lesson files from the guide manifest, so the two cannot disagree."""
    sys.path.insert(0, str(REPO / "scripts"))
    import build_guide

    seen: dict[str, str] = {}
    for ts, _title, rel in build_guide.MANIFEST:
        seen.setdefault(rel, ts)
    return [(ts, COURSE / rel) for rel, ts in seen.items()]


def check_lesson(path: pathlib.Path) -> tuple[list[str], dict[str, int]]:
    """Return (problems, counts) for one lesson."""
    text = path.read_text(encoding="utf-8")
    name = path.relative_to(REPO)
    problems: list[str] = []
    counts = {"rows": 0, "guide": 0, "docs": 0, "outstanding": 0}

    if not SOURCES_HEADING.search(text):
        problems.append("%s: no '## Sources' section" % name)
        return problems, counts

    sources = text[SOURCES_HEADING.search(text).start():]
    counts["outstanding"] = len(UNCHECKED.findall(sources))

    for match in TABLE_ROW.finditer(sources):
        claim = match.group("claim").strip()
        source = match.group("source").strip()
        # Skip the header and separator rows of a markdown table.
        if not claim or claim.lower() == "claim" or set(claim) <= set("-: "):
            continue
        counts["rows"] += 1

        has_eg = bool(EG_REF.search(source))
        has_url = bool(URL.search(source))
        if not (has_eg or has_url):
            problems.append(
                "%s: row cites nothing usable: %r -> %r" % (name, claim[:60], source)
            )
            continue
        if has_eg:
            counts["guide"] += 1
        if has_url:
            counts["docs"] += 1
            if not READ_DATE.search(source):
                # A live link is not a verified claim: pages get rewritten under
                # the same URL, so a citation without a read date cannot be
                # re-checked against what it said when it was read.
                problems.append(
                    "%s: URL cited with no read date: %r" % (name, claim[:60])
                )
    if counts["rows"] == 0:
        problems.append("%s: Sources section has no claim table rows" % name)
    return problems, counts


def report_coverage(paths: list[pathlib.Path]) -> None:
    """Print how many distinct cited pages carry a re-verification record.

    This replaced a fixed sentence that said content verification "has not been run
    on these lessons." Once it HAD been run on some pages, that sentence was false
    in one direction while staying true in the other, and a reader cannot tell which
    half applies to the claim in front of them. A fraction can carry both.
    """
    # Count rows in the Sources section only. Counting whole-file occurrences would
    # fold in prose mentions, and counting distinct FILES would report "2" for a page
    # carrying twenty claims — which inverts the triage order this list exists for.
    cited: dict[str, int] = {}
    for p in paths:
        text = p.read_text(encoding="utf-8")
        head = SOURCES_HEADING.search(text)
        if not head:
            continue
        for match in TABLE_ROW.finditer(text[head.start():]):
            for raw in URL.findall(match.group("source")):
                url = normalise(raw)
                cited[url] = cited.get(url, 0) + 1

    verified = verified_pages()
    outstanding = sorted(set(cited) - set(verified))

    print("CONTENT VERIFICATION (does the page still SAY it?)")
    if not verified:
        print("  no verification record found — treating every page as unverified")
    print("  distinct cited pages:  %d" % len(cited))
    print("  re-verified verbatim:  %d" % len(set(cited) & set(verified)))
    print("  not re-verified:       %d" % len(outstanding))
    # Cite-count is the triage order: the most-cited unverified page is where a stale
    # claim does the most damage, not the alphabetically first one.
    for url in sorted(outstanding, key=lambda u: (-cited[u], u)):
        print("    %-62s %3d claim row(s)" % (url, cited[url]))
    print()
    print("  A page listed as re-verified was re-fetched and had to return the")
    print("  claim's VERBATIM wording. 'Not re-verified' is not a defect and is")
    print("  not a pass — see VERIFICATION.md. Structural citation != verified")
    print("  content, and neither one proves the lesson TEACHES the claim right.")


def check_urls(paths: list[pathlib.Path]) -> int:
    """Report whether each cited URL still resolves. NOT a content check."""
    import urllib.error
    import urllib.request

    urls: dict[str, set[str]] = {}
    for p in paths:
        for u in URL.findall(p.read_text(encoding="utf-8")):
            urls.setdefault(u.rstrip(".,"), set()).add(str(p.relative_to(REPO)))

    print("Resolving %d distinct URL(s). THIS IS NOT A CONTENT CHECK — a page can" % len(urls))
    print("return 200 and no longer say what the lesson claims.\n")
    failures = 0
    for u in sorted(urls):
        try:
            req = urllib.request.Request(u, method="HEAD",
                                         headers={"User-Agent": "course-citation-check"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                print("  %s  %s" % (resp.status, u))
        except urllib.error.HTTPError as exc:
            # Some hosts refuse HEAD; a 405 is not a dead link.
            if exc.code == 405:
                print("  405 (HEAD refused, link not proven dead)  %s" % u)
            else:
                print("  FAIL %s  %s  [%s]" % (exc.code, u, ", ".join(sorted(urls[u]))))
                failures += 1
        except Exception as exc:  # noqa: BLE001 — report, do not crash the run
            print("  FAIL %s  %s  [%s]" % (exc, u, ", ".join(sorted(urls[u]))))
            failures += 1
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--urls", action="store_true",
                        help="also resolve every cited URL (needs the network)")
    args = parser.parse_args(argv)

    found = lessons()
    all_problems: list[str] = []
    totals = {"rows": 0, "guide": 0, "docs": 0, "outstanding": 0}

    for ts, path in found:
        if not path.is_file():
            all_problems.append("TS %s: lesson missing: %s" % (ts, path))
            continue
        problems, counts = check_lesson(path)
        all_problems.extend(problems)
        for k in totals:
            totals[k] += counts[k]

    print("Checked %d lesson file(s)." % len(found))
    print("  claim rows:            %d" % totals["rows"])
    print("  cited to the guide:    %d" % totals["guide"])
    print("  cited to a doc URL:    %d" % totals["docs"])
    print("  outstanding citations: %d  (declared, not hidden)" % totals["outstanding"])
    print()

    if all_problems:
        print("PROBLEMS:")
        for p in all_problems:
            print("  " + p)
    else:
        print("Every claim row names a source, and every URL carries a read date.")

    print()
    report_coverage([p for _, p in found if p.is_file()])

    rc = 1 if all_problems else 0
    if args.urls:
        print()
        if check_urls([p for _, p in found if p.is_file()]):
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
