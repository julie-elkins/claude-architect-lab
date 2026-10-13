"""The library's bounds, refusals and the one real read.

Fixtures under `tests/fixtures/materials/` are hand-written prose rather than output
from a seeded generator. That is a deliberate shortcut and here is the ceiling it
accepts: there is no test asserting the committed bytes match a generator, so nothing
stops a future fixture being pasted in from a real course instead of written for the
test. With three short files of invented prose that trade is worth taking; if this
directory grows past a handful of files, add the generator.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from course_doctor.materials import (
    MAX_MATERIAL_BYTES,
    MaterialRefused,
    extract_cited_urls,
    read_material,
)

FIXTURES = Path(__file__).parent / "fixtures" / "materials"


class TestCitationExtraction:
    def test_deduplicates_while_preserving_first_appearance_order(self):
        urls = extract_cited_urls(
            "see https://b.example/two then https://a.example/one "
            "then https://b.example/two again"
        )
        # Order is first-appearance, NOT sorted. Sorting would put a.example first and
        # discard the only cheap signal about which citation the material leans on.
        assert urls == ["https://b.example/two", "https://a.example/one"]

    def test_strips_sentence_punctuation_from_a_trailing_url(self):
        assert extract_cited_urls("read https://example.org/spec.") == [
            "https://example.org/spec"
        ]

    def test_does_not_swallow_a_markdown_links_closing_bracket(self):
        assert extract_cited_urls("[spec](https://example.org/a)") == [
            "https://example.org/a"
        ]

    def test_requires_a_scheme(self):
        # A bare hostname is not a citation this tool can later fetch, so it must not
        # be reported as one -- an unfetchable "citation" is a promise the next episode
        # cannot keep.
        assert extract_cited_urls("docs.claude.com and ftp://example.org") == []

    def test_no_citations_is_an_empty_list_not_an_error(self):
        assert extract_cited_urls("nothing here") == []


class TestReadMaterial:
    def test_reads_a_file_and_reports_its_citations(self):
        reading = read_material("cites-two.md", FIXTURES)
        assert reading.cited_urls == [
            "https://docs.claude.com/en/docs/claude-code/overview",
            "https://modelcontextprotocol.io/specification",
        ]
        assert reading.line_count > 0
        assert reading.read_at.endswith("+00:00")

    def test_hashes_the_raw_bytes_not_the_decoded_text(self):
        path = FIXTURES / "cites-none.md"
        reading = read_material("cites-none.md", FIXTURES)
        assert reading.sha256 == hashlib.sha256(path.read_bytes()).hexdigest()

    def test_counts_a_final_line_with_no_trailing_newline(self, tmp_path):
        (tmp_path / "m.md").write_text("one\ntwo", encoding="utf-8")
        # Two lines, one newline. `count("\n")` would say one, and the off-by-one is
        # invisible until the count is quoted beside a line number.
        assert read_material("m.md", tmp_path).line_count == 2


class TestRefusals:
    """Each refusal must name a remedy, not just a condition.

    The assertion on `guidance` being non-trivial is the load-bearing one. A refusal
    that says "not found" and nothing else gets an identical retry, so a message
    without a next step costs a call and buys nothing.
    """

    @pytest.mark.parametrize(
        "path, expected",
        [
            ("", "invalid_input"),
            ("   ", "invalid_input"),
            ("missing.md", "not_found"),
            ("../outside.md", "outside_root"),
            ("/etc/passwd", "outside_root"),
        ],
    )
    def test_refusal_codes(self, path, expected):
        with pytest.raises(MaterialRefused) as caught:
            read_material(path, FIXTURES)
        assert caught.value.code == expected
        assert len(caught.value.guidance) > 40

    def test_a_directory_refuses_rather_than_reading_everything_under_it(self):
        with pytest.raises(MaterialRefused) as caught:
            read_material(".", FIXTURES)
        assert caught.value.code == "not_a_file"

    def test_a_sibling_directory_sharing_the_roots_name_prefix_is_outside(self, tmp_path):
        # The boundary is written with `is_relative_to`, not a string prefix compare.
        # A prefix compare passes for `/materials-backup` against root `/materials`,
        # which is the usual way this check is written and still wrong.
        root = tmp_path / "materials"
        root.mkdir()
        sibling = tmp_path / "materials-backup"
        sibling.mkdir()
        (sibling / "secret.md").write_text("x", encoding="utf-8")
        with pytest.raises(MaterialRefused) as caught:
            read_material("../materials-backup/secret.md", root)
        assert caught.value.code == "outside_root"

    def test_oversized_file_refuses_and_reads_nothing(self, tmp_path):
        big = tmp_path / "big.md"
        big.write_bytes(b"x" * (MAX_MATERIAL_BYTES + 1))
        with pytest.raises(MaterialRefused) as caught:
            read_material("big.md", tmp_path)
        assert caught.value.code == "too_large"
        # The bound appears in the message, so the caller learns the limit from the
        # refusal rather than having to find it in source.
        assert str(MAX_MATERIAL_BYTES) in caught.value.message

    def test_a_file_at_exactly_the_limit_is_read(self, tmp_path):
        # The positive direction, pinned alongside the negative one. A bound tested
        # only from above passes just as well if the comparison is inverted, and an
        # inverted bound refuses everything -- which looks like a strict tool rather
        # than a broken one.
        at_limit = tmp_path / "at.md"
        at_limit.write_bytes(b"x" * MAX_MATERIAL_BYTES)
        assert read_material("at.md", tmp_path).byte_count == MAX_MATERIAL_BYTES

    def test_undecodable_bytes_refuse(self, tmp_path):
        (tmp_path / "b.bin").write_bytes(b"\xff\xfe\x00\x01not utf8")
        with pytest.raises(MaterialRefused) as caught:
            read_material("b.bin", tmp_path)
        assert caught.value.code == "undecodable"
