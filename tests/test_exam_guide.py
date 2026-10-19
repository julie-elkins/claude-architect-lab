"""The exam-guide tripwire, and mostly its failure directions.

MUTATE INVERTED. Almost every test here asserts that something is NOT reported as
clean. A tripwire that silently passes is indistinguishable from one that found nothing
wrong, so the mutants worth running are the ones that make a failure path return
`UNCHANGED` or exit 0 — not the ones that break the happy path, which any assertion
catches.

No network. The fetcher is injected, so this file runs on a fresh clone with the wifi off.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import check_exam_guide as ceg  # noqa: E402

GUIDE = "Claude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf"
BASE = "https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fx%2Fpublic"


def page_with(*filenames: str) -> str:
    return "".join(f'<a href="{BASE}%2F{i}%2F{name}">guide</a>' for i, name in enumerate(filenames))


class TestFindingTheRightGuide:
    def test_picks_the_architect_foundations_guide_from_a_page_of_nine(self):
        # The real page carries all four certifications plus a Japanese edition of each.
        # Measured 2026-10-19: nine exam-guide PDFs, which is why matching "exam guide"
        # is not identifying.
        html = page_with(
            GUIDE,
            "Claude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf",
            "Claude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf",
            "Claude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf",
            "Claude+Certified+Architect+-+Foundations+Exam+Guide+%28Japanese%29.pdf",
        )
        assert ceg.find_guide_link(html).endswith(GUIDE)

    def test_the_japanese_edition_alone_is_not_accepted_as_the_guide(self):
        # A near-identical filename for a different artefact. Accepting it would record a
        # baseline against the wrong document and then report "unchanged" forever.
        html = page_with("Claude+Certified+Architect+-+Foundations+Exam+Guide+%28Japanese%29.pdf")
        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.find_guide_link(html)
        assert caught.value.state == "LINK_NOT_FOUND"

    def test_a_json_escaped_duplicate_does_not_win(self):
        # The real page emits each link twice, once in HTML and once inside embedded
        # JSON where a hyphen is written -. The escaped copy appears FIRST, so a
        # check that took candidates[0] would record an unfetchable URL and every later
        # run would report a change that never happened.
        plain = f"{BASE}%2F0%2F{GUIDE}"
        escaped = plain.replace("-", "\\u002D")
        assert "\\u002D" in escaped, "fixture did not actually escape anything"
        html = f'"{escaped}"<a href="{plain}">guide</a>'

        found = ceg.find_guide_link(html)

        # One address, not two: the escaped and plain forms must collapse to the same
        # candidate rather than being reported as ambiguous.
        assert found == plain
        assert "\\u002D" not in found

    def test_a_missing_guide_raises_rather_than_returning_none(self):
        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.find_guide_link("<p>no guides here</p>")
        assert caught.value.state == "LINK_NOT_FOUND"
        assert len(caught.value.guidance) > 40

    def test_two_addresses_for_one_filename_is_ambiguous_not_a_guess(self):
        html = (
            f'<a href="{BASE}%2F1%2F{GUIDE}">a</a>'
            f'<a href="{BASE}%2F2%2F{GUIDE}">b</a>'
        )
        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.find_guide_link(html)
        assert caught.value.state == "AMBIGUOUS_LINK"


class TestComparison:
    baseline = {"pdf_url": "u", "sha256": "h", "byte_count": 10}

    def test_unchanged_only_when_both_signals_match(self):
        state, findings = ceg.compare(
            self.baseline, {"pdf_url": "u", "sha256": "h", "byte_count": 10}
        )
        assert state == "UNCHANGED"
        assert findings == []

    def test_changed_bytes_are_reported(self):
        state, findings = ceg.compare(
            self.baseline, {"pdf_url": "u", "sha256": "DIFFERENT", "byte_count": 11}
        )
        assert state == "CHANGED"
        assert any("BYTES CHANGED" in f for f in findings)

    def test_a_moved_link_alone_is_a_change(self):
        # The second signal, and the one a hash-only check would miss: a republished
        # guide gets a new path. Identical bytes at a new address still means something
        # was re-uploaded and is worth a look.
        state, findings = ceg.compare(
            self.baseline, {"pdf_url": "MOVED", "sha256": "h", "byte_count": 10}
        )
        assert state == "CHANGED"
        assert any("LINK MOVED" in f for f in findings)

    def test_no_baseline_is_its_own_state_and_not_unchanged(self):
        state, findings = ceg.compare(None, {"pdf_url": "u", "sha256": "h", "byte_count": 1})
        assert state == "NO_BASELINE"
        assert findings


class TestNothingCheckedNeverReadsAsClean:
    """The property the whole script exists for."""

    def test_an_unreachable_page_raises_rather_than_reporting_unchanged(self):
        def dead(url, *, limit):
            raise OSError("no route to host")

        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.measure(fetcher=dead)
        assert caught.value.state == "UNREACHABLE"
        assert "not a pass" in caught.value.guidance.lower()

    def test_an_unreachable_pdf_after_a_reachable_page_still_fails(self):
        def page_ok_pdf_dead(url, *, limit):
            if url == ceg.CERT_PAGE:
                return page_with(GUIDE).encode()
            raise OSError("502")

        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.measure(fetcher=page_ok_pdf_dead)
        assert caught.value.state == "UNREACHABLE"

    def test_an_oversized_body_refuses_instead_of_hashing_a_prefix(self):
        # Reading exactly `limit` bytes and hashing them would produce a stable,
        # confident digest of the first 8 MiB of something that is not the guide.
        class FakeResponse:
            def read(self, n):
                return b"x" * n

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        ceg.urllib.request.urlopen = lambda *a, **k: FakeResponse()
        with pytest.raises(ceg.CheckFailed) as caught:
            ceg.fetch("https://example.invalid/x.pdf", limit=16)
        assert caught.value.state == "REFUSED"
        assert "Nothing was hashed" in caught.value.guidance

    def test_measure_hashes_the_bytes_it_was_given(self):
        import hashlib

        payload = b"%PDF-1.7 pretend guide"

        def fake(url, *, limit):
            return page_with(GUIDE).encode() if url == ceg.CERT_PAGE else payload

        observed = ceg.measure(fetcher=fake)
        assert observed["sha256"] == hashlib.sha256(payload).hexdigest()
        assert observed["byte_count"] == len(payload)


class TestTheRecordedBaseline:
    def test_the_committed_baseline_is_complete(self):
        # A baseline missing a field compares as "changed" forever, which trains whoever
        # runs this to ignore it.
        baseline = ceg.load_baseline()
        assert baseline is not None, "no baseline committed; run --record"
        for field in ("pdf_url", "sha256", "byte_count", "checked_at"):
            assert baseline.get(field), f"baseline missing {field}"
        assert len(baseline["sha256"]) == 64
        assert baseline["pdf_url"].startswith("https://")
