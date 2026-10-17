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
