"""The generated GUIDE.md must agree with the lessons it is built from.

A generated reading copy has exactly one failure mode a hand-written one does
not: it goes stale silently. Someone edits a lesson, does not regenerate, and
the guide keeps serving the old text while the lesson file is correct — so the
course and the thing learners actually read disagree, and nothing says so.

These tests are the only thing that catches that. MUTATE INVERTED: the mutant
worth running edits a lesson without regenerating, which is the real-world
version of the bug.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def test_guide_is_not_stale():
    result = subprocess.run(
        [sys.executable, "scripts/build_guide.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "GUIDE.md disagrees with the lessons under course/.\n"
        "Run: python3 scripts/build_guide.py\n" + result.stderr
    )


def test_every_manifest_lesson_exists_on_disk():
    # A lesson listed in the manifest but missing would otherwise drop out of
    # the guide without a word, which is the one thing a generated file can do
    # that a hand-written one cannot.
    sys.path.insert(0, str(REPO / "scripts"))
    import build_guide

    for ts, _title, rel in build_guide.MANIFEST:
        assert (REPO / "course" / rel).is_file(), "TS %s -> missing %s" % (ts, rel)


def test_guide_declares_itself_generated():
    # Without this line someone edits the guide and loses the change on the
    # next build.
    text = (REPO / "GUIDE.md").read_text(encoding="utf-8")
    assert "This file is generated" in text
    assert "scripts/build_guide.py" in text


def test_guide_contains_every_listed_lesson_body():
    sys.path.insert(0, str(REPO / "scripts"))
    import build_guide

    guide = (REPO / "GUIDE.md").read_text(encoding="utf-8")
    for _ts, _title, rel in build_guide.MANIFEST:
        body = (REPO / "course" / rel).read_text(encoding="utf-8").strip()
        # First heading of each lesson must appear in the guide.
        heading = next(l for l in body.splitlines() if l.startswith("# "))
        assert heading[2:].strip() in guide, "missing from guide: %s" % rel


def test_every_lesson_claim_is_cited():
    """Structural citation check: every claim row names a usable source.

    Verified by BREAKING it, three ways: a row citing nothing, a URL with no
    read date, and a lesson with no Sources section. All three were caught.

    This does NOT verify that a cited page still says what a row claims — only
    the verify-course-content skill can do that, and it has not been run on
    these lessons. A passing structural check is not a verified lesson, and
    conflating the two would be the exact failure the course teaches.
    """
    result = subprocess.run(
        [sys.executable, "scripts/check_citations.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_citation_check_declares_what_it_cannot_verify():
    # If this line is ever removed, a passing check starts implying more than
    # it establishes.
    text = (REPO / "scripts" / "check_citations.py").read_text(encoding="utf-8")
    assert "still SAYS what the row claims" in text


def test_no_screen_reader_defects():
    """The markdown structure IS the accessibility layer for this course.

    A blind learner uses a screen reader, which navigates by heading, skips,
    re-reads and searches -- so the work is structural, and structural defects
    are checkable. Verified by reintroducing all three HIGH defects: eleven
    links labelled 'read', a blank table column header, and an image with no
    alt text. All three caught, exit 1, exit 0 clean.

    HIGH only. LOW findings are reported and not gated: the bare-code-fence
    count is an upper bound because a closing fence is also bare, and gating on
    a metric that overcounts teaches people to ignore the check.
    """
    result = subprocess.run(
        [sys.executable, "scripts/check_accessibility.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_accessibility_check_declares_what_it_cannot_verify():
    text = (REPO / "scripts" / "check_accessibility.py").read_text(encoding="utf-8")
    assert "No mechanical defects is not an accessible course" in text


def test_guide_includes_the_program_notice_from_the_readme():
    """The December 7 notice is extracted from the README, not duplicated.

    Two copies of a notice drift, and the first time they do a reader is told
    something no longer true. Single-sourcing makes drift impossible; this test
    catches the other failure -- the heading being renamed, so the guide
    silently stops carrying the notice while the README still has it.
    """
    sys.path.insert(0, str(REPO / "scripts"))
    import build_guide

    guide = (REPO / "GUIDE.md").read_text(encoding="utf-8")
    assert build_guide.NOTICE_HEADING in guide
    # Whitespace-normalised, because the phrase spans a line wrap in the source
    # and asserting on wrapped prose breaks on any reflow -- a test that fails
    # when a paragraph is rewrapped teaches people to stop trusting the suite.
    flat = " ".join(guide.split())
    assert "is not named in that announcement" in flat


def test_guide_includes_the_prerequisite_stack():
    flat = " ".join((REPO / "GUIDE.md").read_text(encoding="utf-8").split())
    assert "What this exam sits on top of" in flat
    # The correction that makes the page worth having.
    assert "is not this exam's" in flat


def test_a_renamed_notice_heading_fails_loudly():
    """Extraction must raise rather than emit nothing.

    A notice that quietly vanishes from the guide is worse than one never
    written, because the README still carries it and nothing says they disagree.
    """
    sys.path.insert(0, str(REPO / "scripts"))
    import build_guide

    try:
        build_guide.extract_section(REPO / "README.md", "## A heading that does not exist")
    except ValueError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("extract_section silently returned on a missing heading")
