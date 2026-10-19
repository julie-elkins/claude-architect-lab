"""Checking a quote against a page: the normalisation, the bounds, the refusals.

Every test here passes a FAKE fetcher. None of them touches the network, on
purpose: a suite that fails when the wifi drops is a suite people learn to
ignore, and `check_quote` takes its fetcher as an argument so that the choice is
structural rather than a mocking trick.

Two of these tests exist because the failures happened by hand on 2026-10-19
while re-verifying the `memory` page: a correct quote reported as missing because
the page carried an inline markdown link inside the quoted sentence, and the
rendered HTML being served under the same URL as the markdown source.
"""

from __future__ import annotations

import pytest

from course_doctor.citations import MAX_PAGE_BYTES, check_quote, normalise
from course_doctor.materials import MaterialRefused


def fake(body: str, content_type: str = "text/markdown; charset=utf-8"):
    """A fetcher that serves one body for a `.md` URL and nothing else.

    Serving ONLY the `.md` form is deliberate: it pins that the source variant is
    what gets tried, and a change that stopped preferring source would fail these
    tests rather than quietly matching against rendered markup.
    """

    def fetch(url: str) -> tuple[str, str, int]:
        if not url.endswith(".md"):
            raise MaterialRefused("unreachable", "no plain variant here", "use .md")
        return body, content_type, len(body.encode("utf-8"))

    return fetch


class TestNormalisation:
    def test_whitespace_is_collapsed_so_a_rewrapped_quote_still_matches(self):
        # A quote copied out of a lesson has been rewrapped by definition.
        assert normalise("one   two\n\nthree") == "one two three"

    def test_an_inline_link_inside_a_sentence_is_flattened(self):
        """MEASURED 2026-10-19: the exact false alarm this normalisation exists for.

        The page says `use a [PreToolUse hook](/docs/en/hooks-guide) instead`; the
        lesson quotes "use a PreToolUse hook instead". Without flattening, a
        correct quote reads as a missing one.
        """
        page = "To block an action, use a [PreToolUse hook](/docs/en/hooks-guide) instead."
        assert "use a PreToolUse hook instead" in normalise(page)

    def test_a_link_target_containing_parentheses_does_not_eat_the_sentence(self):
        # A greedy pattern here would swallow everything to the last `)` on the
        # line, silently deleting prose from the page before matching it.
        page = "see [the docs](https://x.test/a_(b)_c) for more"
        assert normalise(page) == "see the docs for more"

    def test_normalisation_is_applied_to_BOTH_sides(self):
        # Applying it to the page only would fail any quote that itself carries a
        # link, which is most quotes copied out of a lesson's markdown.
        check = check_quote(
            "https://x.test/p",
            "use a [PreToolUse hook](/docs/en/hooks-guide) instead",
            fetch=fake("To block an action, use a PreToolUse hook instead."),
        )
        assert check.found is True


class TestAMatch:
    def test_a_present_quote_is_found(self):
        check = check_quote(
            "https://x.test/p", "Neither set overrides the other",
            fetch=fake("... Neither set overrides the other: if a user rule ..."),
        )
        assert check.found is True
        assert check.source_format.startswith("markdown source")

    def test_an_absent_quote_is_not_found_rather_than_refused(self):
        # The positive direction's partner. A checker that refused on a miss would
        # make "absent" indistinguishable from "could not check", which is the one
        # distinction this tool exists to preserve.
        check = check_quote(
            "https://x.test/p", "a sentence that is not there",
            fetch=fake("something else entirely"),
        )
        assert check.found is False

    def test_the_source_variant_is_tried_first_not_as_a_fallback(self):
        # The rendered page also returns 200, so a fallback ordering would always
        # take the HTML and never discover that source was available.
        asked: list[str] = []

        def fetch(url: str) -> tuple[str, str, int]:
            asked.append(url)
            return "x", "text/markdown", 1

        check_quote("https://x.test/p", "x", fetch=fetch)
        assert asked[0] == "https://x.test/p.md"

    def test_a_url_already_ending_in_md_is_not_double_suffixed(self):
        asked: list[str] = []

        def fetch(url: str) -> tuple[str, str, int]:
            asked.append(url)
            return "x", "text/markdown", 1

        check_quote("https://x.test/p.md", "x", fetch=fetch)
        assert asked == ["https://x.test/p.md"]


class TestFallingBackToTheRenderedPage:
    def test_html_is_matched_against_but_the_result_says_so(self):
        """A page with no source variant must still be checkable, and must say it was.

        MEASURED: the same docs URL served 801,645 bytes of HTML and 51,526 bytes
        of markdown. Matching against markup can miss for markup reasons, so
        `source_format` qualifies `found` and the server relays it as a warning.
        """
        def fetch(url: str) -> tuple[str, str, int]:
            if url.endswith(".md"):
                raise MaterialRefused("unreachable", "404", "fall back")
            return "<p>Neither set overrides the other</p>", "text/html", 40

        check = check_quote("https://x.test/p", "Neither set overrides the other", fetch=fetch)
        assert check.found is True
        assert check.fetched_url == "https://x.test/p"
        assert "as served" in check.source_format

    def test_a_md_url_serving_html_falls_back_instead_of_matching_it(self):
        """The trap that makes this more than a 404 check.

        A docs host that serves the RENDERED page for `<url>.md` returns 200 with
        `text/html`. Treating that as source would report `source_format` as
        markdown while matching against markup -- a result that is wrong about its
        own provenance, which is worse than a miss.
        """
        served: list[str] = []

        def fetch(url: str) -> tuple[str, str, int]:
            served.append(url)
            return "<p>hello</p>", "text/html", 12

        check = check_quote("https://x.test/p", "hello", fetch=fetch)
        assert served == ["https://x.test/p.md", "https://x.test/p"]
        assert "as served" in check.source_format


class TestRefusals:
    @pytest.mark.parametrize("url", ["", "   "])
    def test_an_empty_url_refuses(self, url):
        with pytest.raises(MaterialRefused) as caught:
            check_quote(url, "x", fetch=fake("x"))
        assert caught.value.code == "invalid_input"

    @pytest.mark.parametrize("quote", ["", "   "])
    def test_an_empty_quote_refuses_rather_than_matching_everything(self, quote):
        # An empty needle is in every haystack, so without this the tool would
        # report every claim as verified -- a clean-looking total failure.
        with pytest.raises(MaterialRefused) as caught:
            check_quote("https://x.test/p", quote, fetch=fake("anything"))
        assert caught.value.code == "invalid_input"

    def test_an_unreachable_page_refuses_and_says_nothing_was_checked(self):
        def fetch(url: str) -> tuple[str, str, int]:
            raise MaterialRefused(
                "unreachable", "HTTP 404",
                "NOTHING WAS CHECKED, so do not record this quote as absent",
            )

        with pytest.raises(MaterialRefused) as caught:
            check_quote("https://x.test/p", "x", fetch=fetch)
        assert caught.value.code == "unreachable"
        # The remedy, not just the rule: an unreachable page and a retracted claim
        # are different findings and the guidance has to keep them apart.
        assert "not record this quote as absent" in caught.value.guidance


class TestTheRealFetcherBounds:
    """The real `_fetch`, exercised without the network.

    Only the size cap is reachable without a socket, and it is the one worth
    pinning: a page read up to exactly the cap is a TRUNCATED page, and a quote
    missing from a truncated page would be reported as absent.
    """

    def test_a_page_over_the_cap_refuses_rather_than_being_truncated(self, monkeypatch):
        import course_doctor.citations as mod

        class FakeResponse:
            headers = {"Content-Type": "text/markdown"}

            def read(self, size):
                # The real urlopen returns what was asked for; the module asks for
                # one byte past the cap precisely so the cap can be detected.
                return b"x" * size

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        monkeypatch.setattr(mod.urllib.request, "urlopen", lambda *a, **k: FakeResponse())
        with pytest.raises(MaterialRefused) as caught:
            mod._fetch("https://x.test/big.md")
        assert caught.value.code == "page_too_large"
        assert "not truncated and checked" in caught.value.guidance

    def test_a_page_at_the_cap_is_read(self, monkeypatch):
        # The positive direction. A cap tested only from above passes just as well
        # if the comparison is inverted, and an inverted cap refuses everything --
        # which looks like a strict tool rather than a broken one.
        import course_doctor.citations as mod

        class FakeResponse:
            headers = {"Content-Type": "text/markdown"}

            def read(self, size):
                return b"y" * MAX_PAGE_BYTES

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        monkeypatch.setattr(mod.urllib.request, "urlopen", lambda *a, **k: FakeResponse())
        text, content_type, byte_count = mod._fetch("https://x.test/ok.md")
        assert byte_count == MAX_PAGE_BYTES
        assert "markdown" in content_type
        assert len(text) == MAX_PAGE_BYTES
