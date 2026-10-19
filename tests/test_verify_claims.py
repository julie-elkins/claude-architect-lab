"""The claim-verification loop, and mostly the things it must not report as passing.

MUTATE INVERTED. The valuable mutants make a failure read as a success: drop the exit-2
on a failed fetch, let `--offline` return 0, classify a stitched quote as checkable so it
fails forever, or print the results before the coverage line. Breaking the happy path is
caught by any assertion; those four are caught only here.

No network. The fetcher is injected.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import verify_claims as vc  # noqa: E402


def page(text: str):
    """What `citations._fetch` returns: (text, content_type, byte_count)."""
    return (text, "text/markdown", len(text))


class TestWhatCountsAsCheckable:
    def test_a_long_quoted_run_is_checkable(self):
        quote, reason = vc.quoted_run(
            'the docs say "persistent rules belong in CLAUDE.md because it is re-injected"', 25
        )
        assert quote == "persistent rules belong in CLAUDE.md because it is re-injected"
        assert reason is None

    def test_a_paraphrase_is_not_checkable_and_says_so(self):
        quote, reason = vc.quoted_run("The hierarchy is user, project and directory", 25)
        assert quote is None
        assert "paraphrase" in reason

    def test_a_short_quoted_identifier_is_not_a_quote(self):
        # `"tool_use"` found on a page is weak evidence that a claim survived.
        quote, reason = vc.quoted_run('stop_reason is `"tool_use"` while tools run', 25)
        assert quote is None
        assert "paraphrase" in reason

    @pytest.mark.parametrize("ellipsis", ["...", "…"])
    def test_a_stitched_quote_is_not_checkable_rather_than_not_found(self, ellipsis):
        # THE CRYING-WOLF CASE, and the reason this classification exists. A quote
        # joined across an ellipsis cannot match verbatim whatever the page says, so
        # reporting it NOT FOUND fires on every future run and trains the reader to
        # ignore the findings that can be cleared. Measured 2026-10-19: 4 of the first
        # 9 not-found results were exactly this.
        claim = f'"Persistent rules belong in CLAUDE.md{ellipsis} and are re-injected every time"'
        quote, reason = vc.quoted_run(claim, 25)
        assert quote is None
        assert "stitched" in reason

    def test_the_longest_whole_quote_wins_over_a_stitched_one(self):
        claim = (
            '"first fragment... second fragment here" and also '
            '"one contiguous span that is comfortably long enough to use"'
        )
        quote, reason = vc.quoted_run(claim, 25)
        assert quote == "one contiguous span that is comfortably long enough to use"
        assert reason is None


class TestCoverageIsTheHeadline:
    def test_the_coverage_line_comes_before_any_result(self, capsys):
        # If results print first, a reader forms a verdict before learning the
        # denominator. That is the failure this whole script is shaped against.
        vc.main(["--offline"])
        out = capsys.readouterr().out
        assert "Coverage:" in out
        assert out.index("Coverage:") < out.index("## Checked")

    def test_the_report_names_what_it_does_not_show(self, capsys):
        vc.main(["--offline"])
        out = capsys.readouterr().out
        assert "What this report does not show" in out
        # The exam guide is the majority of the corpus and the part this cannot touch.
        assert "exam guide" in out

    def test_the_breakdown_accounts_for_every_unchecked_row(self, capsys):
        vc.main(["--offline"])
        out = capsys.readouterr().out
        total = int(out.split("of ")[1].split(" claim rows")[0])
        checkable = int(out.split("Coverage: ")[1].split(" of")[0])
        counted = sum(
            int(line.split("**")[1].split(" rows")[0])
            for line in out.splitlines()
            if line.startswith("- **") and "rows**" in line
        )
        # Every row is either checkable or has a stated reason. A row in neither bucket
        # would be silently dropped from the denominator.
        assert checkable + counted == total


class TestNothingCheckedIsNeverAPass:
    def test_offline_exits_two(self, capsys):
        assert vc.main(["--offline"]) == 2

    def test_a_failed_fetch_exits_two_and_outranks_a_missing_quote(self, capsys):
        # Precedence matters: an incomplete run is worse to report than a known
        # finding, because you do not know what it would have found.
        def dead(url):
            raise OSError("no route to host")

        assert vc.main([], fetch_one=dead) == 2
        out = capsys.readouterr().out
        assert "could not be checked" in out

    def test_a_failed_fetch_is_counted_as_neither_pass_nor_fail(self, capsys):
        def dead(url):
            raise OSError("down")

        vc.main([], fetch_one=dead)
        out = capsys.readouterr().out
        assert "**0 verbatim match**" in out
        assert "**0 NOT FOUND**" in out

    def test_every_quote_present_exits_zero(self, capsys):
        # A page containing every quote in the corpus. Proves the loop CAN pass --
        # a gate that cannot pass is as useless as one that cannot fail.
        rows = [r for r in vc.collect(vc.DEFAULT_MIN_QUOTE) if r.quote]
        everything = page(" ".join(r.quote for r in rows))
        assert vc.main([], fetch_one=lambda url: everything) == 0
        assert "NOT FOUND" in capsys.readouterr().out  # the heading, with a 0 count

    def test_a_missing_quote_exits_one(self, capsys):
        assert vc.main([], fetch_one=lambda url: page("nothing relevant here")) == 1
        assert "**0 verbatim match**" in capsys.readouterr().out


class TestFetchingIsCachedPerUrl:
    def test_one_page_is_fetched_once_however_many_claims_cite_it(self):
        calls: list[str] = []

        def counting(url):
            calls.append(url)
            return page("x")

        fetch = vc.caching_fetcher(counting)
        fetch("https://a.example/p")
        fetch("https://a.example/p")
        fetch("https://b.example/q")
        # The memory page alone carries 22 claim rows; fetching per claim would hit one
        # host 22 times in seconds and invite a rate limit this script would then have
        # to report as "could not check" for a reason it caused itself.
        assert calls == ["https://a.example/p", "https://b.example/q"]

    def test_a_url_that_failed_once_is_not_retried(self):
        calls: list[str] = []

        def dead(url):
            calls.append(url)
            raise OSError("down")

        fetch = vc.caching_fetcher(dead)
        for _ in range(3):
            with pytest.raises(Exception):
                fetch("https://a.example/p")
        assert calls == ["https://a.example/p"]
