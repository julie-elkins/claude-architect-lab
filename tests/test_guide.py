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
import re
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
    # If this disclaimer is ever removed, a passing check starts implying more than
    # it establishes. Pinned on the imperative rather than one sentence: an earlier
    # version of this test asserted an exact phrase, and rewording the output to
    # report verification COVERAGE broke it while making the output stricter. That
    # is a test pinning the prose instead of the property.
    text = (REPO / "scripts" / "check_citations.py").read_text(encoding="utf-8")
    assert "Structural citation != verified" in text
    assert "not a pass" in text


def _coverage_module():
    sys.path.insert(0, str(REPO / "scripts"))
    import check_citations

    return check_citations


def test_a_missing_verification_record_reports_zero_verified_not_an_error():
    """Deleting the record must make the course look LESS verified, never more.

    This is the load-bearing direction. A verification store that errors when
    absent gets worked around; one that defaults to "everything is fine" is the
    failure this whole course is about. Measured once for real, by accident: the
    URLs in VERIFICATION.md were first written without an `https://` scheme, the
    regex matched nothing, and the checker reported 0 of 13 verified rather than
    claiming coverage it did not have.
    """
    mod = _coverage_module()
    original = mod.VERIFICATION
    try:
        mod.VERIFICATION = REPO / "no-such-verification-file.md"
        assert mod.verified_pages() == {}
    finally:
        mod.VERIFICATION = original


def test_the_real_record_verifies_some_pages_and_not_the_ones_it_disclaims():
    """The positive direction, pinned beside the negative one.

    A regex loose enough to match any URL anywhere in VERIFICATION.md would
    promote the eight pages that file lists as NOT re-verified — flattering the
    count using the very text that admits the gap. So assert both halves: the
    five in the table are found, and at least one named in the outstanding prose
    is not.

    MEASURED 2026-10-18, and the first version of this test was worthless. A
    mutant replacing the anchored row pattern with "any URL anywhere" SURVIVED,
    because the outstanding URLs in VERIFICATION.md were written without an
    `https://` scheme — so the loose regex missed them too, and the assertion
    held for a reason that had nothing to do with the property. Normalising
    those URLs to carry schemes made the two regexes actually differ, and the
    same mutant is now killed by this test. Keep the schemes: without them this
    test passes on a checker that counts prose as proof.
    """
    mod = _coverage_module()
    verified = mod.verified_pages()
    assert verified, "the committed VERIFICATION.md should verify some pages"
    assert "https://code.claude.com/docs/en/hooks" in verified
    # Listed in VERIFICATION.md's prose as outstanding. Must not count as verified.
    assert "https://code.claude.com/docs/en/memory" not in verified


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


def test_production_assets_are_self_consistent():
    """Stated slide counts, numbering, links, and the authoritative header.

    Every rule this enforces was broken by hand in this repository, and three of
    the four shipped. The slide-count rule specifically: writing episodes 2 and 3
    produced a stated count that disagreed with the slides TWICE IN TWO FILES
    (14 against 15, then 19 against 20). Somebody building a deck from the header
    comes up a slide short with nothing to flag it.

    Verified by breaking it five ways on 2026-10-18 — a wrong stated count, a
    duplicated slide number, a broken relative link, a removed production-asset
    header, and a chapter marker pointing at a slide that does not exist. All
    five were caught, exit 1; restored, exit 0.
    """
    result = subprocess.run(
        [sys.executable, "scripts/check_production.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _recall_rows() -> list[tuple[str, list[str]]]:
    """Table rows of RECALL.md as (first cell, lesson paths it links to).

    Header and separator rows are dropped. A row is kept even when it links
    nowhere, so a row that quietly lost its lesson link still shows up in the
    link test's denominator rather than passing by disappearing.
    """
    text = (REPO / "RECALL.md").read_text(encoding="utf-8")
    rows: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or set(line) <= set("|-: "):
            continue
        first = cells[0]
        if first.lower() in {"path", "field", "flag", "name", "the thing"}:
            continue
        rows.append((first, re.findall(r"\((course/[^)]+\.md)\)", line)))
    return rows


def test_every_recall_sheet_link_resolves():
    """RECALL.md restates the lessons, so a dead link there is a dead end.

    Covers every link in the file, not only the ones inside table rows: the
    loading-order note under the first table links out in prose, and a test
    that only read tables would call the file clean with that link broken.
    """
    text = (REPO / "RECALL.md").read_text(encoding="utf-8")
    targets = re.findall(r"\]\((course/[^)]+\.md|[A-Z]+\.md)\)", text)
    assert targets, "RECALL.md links to no lessons -- it is an index of nothing"
    for rel in targets:
        assert (REPO / rel).is_file(), "RECALL.md links to a missing file: %s" % rel


def test_every_recall_sheet_term_appears_in_the_lesson_it_points_at():
    """The cheap half of the staleness problem, and the half that is checkable.

    RECALL.md is a third copy of claims the lessons own -- the same shape as an
    episode script, and `check_production.py` exists because a script lagged its
    lesson and nothing noticed. So: if a row names `--json-schema` and no linked
    lesson mentions it any more, the flag was renamed or the row was invented,
    and both are caught here.

    WHAT THIS CANNOT CATCH, and it is the failure that actually ships: a row
    whose wording survived while its MEANING drifted. `allowed-tools` appearing
    in a lesson proves nothing about whether the lesson still says it
    pre-approves rather than restricts. Only a person re-reading both does that,
    which is why RECALL.md opens by naming the lessons as authoritative.
    """
    rows = _recall_rows()
    assert len(rows) >= 20, "expected the recall sheet's rows; found %d" % len(rows)
    cache: dict[str, str] = {}
    for first_cell, links in rows:
        terms = re.findall(r"`([^`]+)`", first_cell)
        if not terms or not links:
            continue
        # Placeholder segments are the author's, not the product's: a row may
        # write `.claude/skills/<name>/SKILL.md` where the lesson writes a real
        # name. Match on the fixed prefix so the test checks the convention
        # rather than the illustration.
        term = terms[0].split("<")[0].rstrip("/")
        for rel in links:
            if rel not in cache:
                # A missing lesson belongs to the link test above. Reading it
                # here would raise FileNotFoundError from pathlib instead, which
                # names a temp path and not the row that is wrong.
                if not (REPO / rel).is_file():
                    continue
                cache[rel] = (REPO / rel).read_text(encoding="utf-8")
            assert term in cache[rel], (
                "RECALL.md names %r and links to %s, which no longer mentions it"
                % (term, rel)
            )


def test_recall_sheet_declares_the_drift_it_cannot_see():
    # Same reasoning as the production-asset disclaimer below: this page is a
    # restatement, so without the warning a reader takes it for a source and
    # stops checking the lesson it came from.
    text = (REPO / "RECALL.md").read_text(encoding="utf-8")
    assert "The lessons are authoritative" in text
    assert "cannot catch a row whose meaning drifted" in text
    # No row may be a new claim; the page says so, and the suite pins it.
    assert "No row here is a new claim" in text


def test_the_readme_count_of_surprising_defaults_matches_the_table():
    """A hand-maintained count in a README goes stale DOWNWARD, which reads as
    modesty rather than as an error -- measured in this repository once already,
    where the README claimed 72 claim rows against a real 329 and nobody
    noticed. So the README says "nine places where the default is the opposite"
    and this counts them. Adding a row means editing the number on purpose.
    """
    recall = (REPO / "RECALL.md").read_text(encoding="utf-8")
    heading = "## Where the default is the opposite of the guess"
    start = recall.find(heading)
    assert start != -1, "the surprising-defaults section was renamed or removed"
    section = recall[start:]
    end = section.find("\n## ", 1)
    section = section if end == -1 else section[:end]
    rows = [
        l for l in section.splitlines()
        if l.strip().startswith("|")
        # A separator row is nothing but pipes, dashes, colons and spaces.
        and not set(l.strip()) <= set("|-: ")
        and not l.strip().startswith("| The thing")
    ]
    assert len(rows) == 9, "the table has %d rows; the README says nine" % len(rows)
    assert "nine places where" in (REPO / "README.md").read_text(encoding="utf-8")


def test_production_check_declares_the_drift_it_cannot_see():
    # The one real failure here is a script disagreeing with its lesson, and no
    # diff can detect it. If this disclaimer goes, a passing check starts implying
    # the scripts were verified against the lessons. They were not.
    text = (REPO / "scripts" / "check_production.py").read_text(encoding="utf-8")
    assert "NOT CHECKED HERE" in text
    assert "Re-read the lessons before recording" in text
