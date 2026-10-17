#!/usr/bin/env python3
"""Check the course markdown for defects that break a screen reader.

Why this exists: this is a written course, so **the markdown structure IS the
accessibility layer.** A blind learner using a screen reader does not want an
audio recording — audio is linear and unsearchable, where a screen reader
navigates by heading, skips, re-reads, changes speed and searches. So the
accessibility work is structural, and structural defects are checkable.

Every rule here was written because the course had the defect. Measured
2026-10-17 before the fix: eleven links in the README all labelled `read`, and
three tables whose first column header was blank.

What it checks:

1. **Ambiguous link text.** Screen readers offer a "list all links" mode that
   presents link text out of its surrounding sentence. Eleven links called
   `read` are eleven indistinguishable entries. Also catches `here`, `click
   here`, `this`, `link`, `more`.
2. **Blank table header cells.** A screen reader announces a column's header
   when reading each cell, so an empty header reads as "blank".
3. **Skipped heading levels.** Heading navigation is the primary way a screen
   reader user moves through a long document; a jump from `##` to `####` breaks
   the outline.
4. **Images without alt text.** The one defect that makes content completely
   unavailable rather than merely awkward.
5. **Untagged code fences.** Lowest severity and still worth it: a tagged fence
   lets assistive tooling announce the language.

What it does NOT check, and this is the honest limit: whether the prose makes
sense when read aloud, whether a diagram's alt text is any good, or whether
meaning is carried by emphasis alone. Those need a person — ideally a person who
uses a screen reader. A passing run means no mechanical defects, not an
accessible course.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

# MEASURED: these were the actual defects. `read` is first because it was ours.
AMBIGUOUS_LINK_TEXT = {
    "read", "here", "click here", "this", "this one", "link", "more",
    "see here", "learn more", "docs", "documentation", "x",
}

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+\S", re.MULTILINE)
TABLE_HEADER = re.compile(r"^\|(?P<cells>.+)\|\s*$\n^\|[\s:|-]+\|\s*$", re.MULTILINE)
BARE_FENCE = re.compile(r"^```\s*$", re.MULTILINE)
FENCED_BLOCK = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def strip_fences(text: str) -> str:
    """Blank out fenced code blocks, preserving line count.

    MEASURED 2026-10-17: without this, a shell comment inside a code block —
    `# Refuse a write outside the project root.` — was counted as an h1 and
    reported as a skipped heading level. A false positive is worse than no
    check, because it teaches the reader to ignore the real ones. Line count is
    preserved so any future line-numbered finding stays accurate.
    """
    return FENCED_BLOCK.sub(
        lambda m: "\n" * m.group(0).count("\n"), text
    )


def check_file(path: pathlib.Path) -> list[tuple[str, str]]:
    """Return a list of (severity, message)."""
    raw = path.read_text(encoding="utf-8")
    # Headings, links and images inside a fenced block are examples, not
    # document structure. Fence counting below deliberately uses the raw text.
    text = strip_fences(raw)
    name = str(path.relative_to(REPO))
    out: list[tuple[str, str]] = []

    # 1. Ambiguous link text, counted so one repeated label reads as one finding.
    labels: dict[str, int] = {}
    for m in LINK.finditer(text):
        label = m.group(1).strip().lower()
        if not label or label.startswith("!"):
            continue
        if label in AMBIGUOUS_LINK_TEXT:
            labels[label] = labels.get(label, 0) + 1
    for label, count in sorted(labels.items()):
        out.append((
            "HIGH",
            "%s: %d link(s) labelled %r — indistinguishable in a screen "
            "reader's link list" % (name, count, label),
        ))

    # 2. Blank table header cells.
    for m in TABLE_HEADER.finditer(text):
        cells = [c.strip() for c in m.group("cells").split("|")]
        if any(c == "" for c in cells):
            out.append((
                "HIGH",
                "%s: table has a blank column header — a screen reader "
                "announces the header with every cell, so it reads as "
                "'blank': |%s|" % (name, m.group("cells")[:60]),
            ))

    # 3. Skipped heading levels.
    levels = [len(m.group(1)) for m in HEADING.finditer(text)]
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            out.append((
                "MEDIUM",
                "%s: heading level jumps from h%d to h%d — breaks heading "
                "navigation" % (name, previous, current),
            ))
            break

    # 4. Images without alt text.
    for m in IMAGE.finditer(text):
        if not m.group(1).strip():
            out.append((
                "HIGH",
                "%s: image with no alt text: %s" % (name, m.group(2)[:60]),
            ))

    # 5. Untagged code fences. Count opening fences only: a bare ``` is a
    #    closing fence half the time, so this is an upper bound and is
    #    reported as LOW for that reason.
    bare = len(BARE_FENCE.findall(raw))
    tagged = len(re.findall(r"^```\S+", raw, re.MULTILINE))
    if bare > tagged:
        out.append((
            "LOW",
            "%s: %d bare code fence(s) against %d tagged — a language tag lets "
            "assistive tooling announce the language (upper bound: closing "
            "fences are also bare)" % (name, bare, tagged),
        ))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="fail on MEDIUM and LOW as well as HIGH")
    args = parser.parse_args(argv)

    targets = sorted(
        [REPO / "README.md", REPO / "GUIDE.md", REPO / "course" / "README.md"]
        + list((REPO / "course").rglob("lesson*.md"))
    )
    targets = [t for t in targets if t.is_file()]

    findings: list[tuple[str, str]] = []
    for t in targets:
        findings.extend(check_file(t))

    by_sev = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for sev, _ in findings:
        by_sev[sev] += 1

    print("Checked %d file(s) for screen-reader defects." % len(targets))
    print("  HIGH %d   MEDIUM %d   LOW %d" % (
        by_sev["HIGH"], by_sev["MEDIUM"], by_sev["LOW"]))
    print()
    for sev in ("HIGH", "MEDIUM", "LOW"):
        for s, msg in findings:
            if s == sev:
                print("  [%s] %s" % (sev, msg))
    if not findings:
        print("  No mechanical defects found.")

    print()
    print("NOT CHECKED HERE: whether the prose reads sensibly aloud, whether any")
    print("alt text is actually useful, or whether meaning is carried by emphasis")
    print("alone. Those need a person, ideally one who uses a screen reader.")
    print("No mechanical defects is not an accessible course.")

    if by_sev["HIGH"]:
        return 1
    if args.strict and (by_sev["MEDIUM"] or by_sev["LOW"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
