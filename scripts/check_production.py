#!/usr/bin/env python3
"""Check the video production assets for the defects that actually happened.

Why this exists: every rule below was broken by hand, in this repository, and three
of the four shipped. Production assets get less scrutiny than lessons because they
are not the course — which is exactly why a stale one survives.

MEASURED, 2026-10-18. Writing episodes 2 and 3 produced a stated slide count that
did not match the slides **twice in two files** (14 against 15, then 19 against 20).
Both read as authoritative and both were wrong, and a reader building a deck from
the header would have come up a slide short with nothing to flag it. Two instances
out of two files written is not a slip, it is a recurring failure, so it gets a
check instead of a resolution to be more careful.

What it CAN check:

- a slides file's stated slide count matches the actual number of `## Slide N`
  headings
- slide numbers are sequential from 1, with no gaps and no duplicates
- every chapter-marker slide named in a header exists
- every relative link resolves to a real file
- every production asset carries the header saying the written lessons are
  authoritative, because without it a reader cannot tell a script from a lesson

What it CANNOT check, and this is the limit that matters: **whether a script still
agrees with the lessons it covers.** A script is prose restating a lesson, not a
copy of one, so a diff cannot tell a legitimate rewording from a stale claim. That
failure is real — episode 1 taught a corrected-away claim for five days — and the
only defence is the ⚠ header this script enforces the presence of, plus a person
re-reading before recording.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
COURSE = REPO / "course"

SLIDE_HEADING = re.compile(r"^## Slide (\d+)\s*$", re.MULTILINE)
STATED_COUNT = re.compile(r"^(\d+) slides\b", re.MULTILINE)
CHAPTER_MARKERS = re.compile(r"[Cc]hapter markers go at slides ([\d,\s and]+)")
REL_LINK = re.compile(r"\[[^\]]+\]\((?!https?:)([^)#]+)")
AUTHORITATIVE = "written lessons are authoritative"
PRODUCTION_ASSET = "production asset, not the lesson"


def assets() -> list[pathlib.Path]:
    return sorted(COURSE.rglob("production/*.md"))


def check(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    name = path.relative_to(REPO)
    problems: list[str] = []

    # Every production file must identify itself as one. A reader who cannot tell a
    # narration script from a lesson will study the script, which is the weaker text
    # and the one allowed to lag.
    low = text.lower()
    if AUTHORITATIVE not in low and PRODUCTION_ASSET not in low:
        problems.append(
            "%s: no header marking this a production asset with the lessons "
            "authoritative" % name
        )

    for target in REL_LINK.findall(text):
        if not (path.parent / target).resolve().exists():
            problems.append("%s: broken relative link -> %s" % (name, target))

    if "slides" not in path.name:
        return problems

    numbers = [int(n) for n in SLIDE_HEADING.findall(text)]
    if not numbers:
        problems.append("%s: a slides file with no '## Slide N' headings" % name)
        return problems

    stated = STATED_COUNT.search(text)
    if not stated:
        # Not optional. The count is what somebody builds a deck against.
        problems.append("%s: no stated slide count ('N slides for a ...')" % name)
    elif int(stated.group(1)) != len(numbers):
        problems.append(
            "%s: states %s slides, contains %d"
            % (name, stated.group(1), len(numbers))
        )

    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        problems.append(
            "%s: slide numbers are not sequential from 1: %r" % (name, numbers)
        )

    markers = CHAPTER_MARKERS.search(text)
    if markers:
        present = set(numbers)
        for raw in re.findall(r"\d+", markers.group(1)):
            if int(raw) not in present:
                problems.append(
                    "%s: header names chapter marker at slide %s, which does not exist"
                    % (name, raw)
                )
    return problems


def main() -> int:
    found = assets()
    all_problems: list[str] = []
    for path in found:
        all_problems.extend(check(path))

    slides = [p for p in found if "slides" in p.name]
    scripts = [p for p in found if "script" in p.name]
    print("Checked %d production asset(s): %d script(s), %d slide deck(s)."
          % (len(found), len(scripts), len(slides)))

    if all_problems:
        print("\nPROBLEMS:")
        for p in all_problems:
            print("  " + p)
    else:
        print("Stated slide counts match, numbering is sequential, links resolve,")
        print("and every asset declares itself a production asset.")

    print()
    print("NOT CHECKED HERE: whether a script still AGREES with the lessons it")
    print("covers. A script restates a lesson in spoken prose, so no diff can tell")
    print("a rewording from a stale claim. Episode 1 taught a corrected-away claim")
    print("for five days. Re-read the lessons before recording.")
    return 1 if all_problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
