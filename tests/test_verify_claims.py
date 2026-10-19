"""The claim-verification loop: the tiers, and the things it must not report as passing.

MUTATE INVERTED. The valuable mutants make a weak result read as a strong one: add the
IDENTIFIER count to the VERBATIM count, let `--offline` return 0, drop the exit-2 on a
failed fetch, classify a stitched quote as checkable so it fails forever, or stop
truncating a templated path so a rename is reported that never happened. Breaking the
happy path is caught by any assertion; those five are caught only here.

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


class TestWhatCountsAsAVerbatimQuote:
    def test_a_long_contiguous_quoted_run_is_usable(self):
        quote, reason = vc.quoted_run(
            'the docs say "persistent rules belong in CLAUDE.md because it is re-injected"', 25
        )
        assert quote == "persistent rules belong in CLAUDE.md because it is re-injected"
        assert reason is None

    def test_a_paraphrase_has_no_quoted_span(self):
        quote, reason = vc.quoted_run("The hierarchy is user, project and directory", 25)
        assert quote is None
        assert reason == "no quoted span"

    def test_a_short_quoted_token_is_not_a_quote(self):
        quote, _ = vc.quoted_run('stop_reason is `"tool_use"` while tools run', 25)
        assert quote is None

    @pytest.mark.parametrize("ellipsis", ["...", "…"])
    def test_a_stitched_quote_is_unusable_rather_than_failing(self, ellipsis):
        # THE CRYING-WOLF CASE. A quote joined across an ellipsis cannot match verbatim
        # whatever the page says, so reporting it NOT FOUND fires on every future run and
        # teaches the reader to ignore the findings that can be cleared. Measured: 4 of
        # the first 9 misses were this, and 3 of those 4 matched the page on BOTH sides of
        # the ellipsis once split -- nothing had drifted at all.
        claim = f'"Persistent rules belong in CLAUDE.md{ellipsis} and are re-injected each time"'
        quote, reason = vc.quoted_run(claim, 25)
        assert quote is None
        assert "stitched" in reason

    def test_a_whole_quote_beats_a_stitched_one_in_the_same_claim(self):
        claim = (
            '"first fragment... second fragment here" and also '
            '"one contiguous span that is comfortably long enough to use"'
        )
        quote, reason = vc.quoted_run(claim, 25)
        assert quote == "one contiguous span that is comfortably long enough to use"
        assert reason is None


class TestWhatCountsAsADistinctiveIdentifier:
    @pytest.mark.parametrize(
        "token", ["--strict-mcp-config", "${VAR:-default}", ".claude/rules/", "PreToolUse"]
    )
    def test_structural_or_camelcase_tokens_are_kept(self, token):
        assert vc.identifiers(f"the claim mentions `{token}` here") == [token]

    @pytest.mark.parametrize("token", ["Bash", "Read", "agent", "allow", "block"])
    def test_bare_words_are_dropped_as_too_common(self, token):
        # "The page still contains the word Read" is not a check. Measured: 56 of 140
        # distinct backticked tokens were bare words like these.
        assert vc.identifiers(f"the claim mentions `{token}` here") == []

    def test_a_templated_path_is_truncated_at_the_placeholder(self):
        # MEASURED: `.claude/skills/<name>/SKILL.md` is absent from the skills page while
        # `.claude/skills/` is present. The docs write the same path with different
        # notation, so matching the templated form reports a rename that never happened.
        assert vc.identifiers("skills live in `.claude/skills/<name>/SKILL.md`") == [
            ".claude/skills/"
        ]

    def test_only_the_leading_token_is_used(self):
        # `--resume <name>` and `--resume <transcript-path>` are one flag documented with
        # two placeholders.
        assert vc.identifiers("`--resume <name>` resumes") == ["--resume"]

    def test_identifiers_deduplicate_and_keep_order(self):
        claim = "`--bare` then `--mcp-config` then `--bare` again"
        assert vc.identifiers(claim) == ["--bare", "--mcp-config"]


class TestEveryRowGetsExactlyOneTier:
    def test_the_tier_table_sums_to_the_total(self, capsys):
        # A row in no tier would be silently dropped from the denominator, which is the
        # flattering direction.
        vc.main(["--offline"])
        out = capsys.readouterr().out
        counts = {}
        for tier in vc.TIERS:
            line = next(ln for ln in out.splitlines() if f"| {tier} |" in ln)
            counts[tier] = int(line.split("|")[1].strip())
        total = int(
            next(ln for ln in out.splitlines() if "| total |" in ln)
            .split("|")[1].replace("*", "").strip()
        )
        assert sum(counts.values()) == total

    def test_a_guide_cited_row_is_guide_tier(self):
        rows = vc.collect()
        guide = [r for r in rows if r.tier == "GUIDE"]
        assert guide, "no guide-tier rows found"
        assert all(r.url is None for r in guide)

    def test_tiers_are_the_only_tiers(self):
        assert {r.tier for r in vc.collect()} <= set(vc.TIERS)


class TestTiersAreNeverPooled:
    def test_the_report_states_the_counts_are_not_added(self, capsys):
        vc.main(["--offline"])
        assert "never added together" in capsys.readouterr().out

    def test_a_passing_identifier_row_is_not_called_verified(self, capsys):
        page_with_everything = page(
            " ".join(
                [r.quote for r in vc.collect() if r.tier == "VERBATIM"]
                + [s for r in vc.collect() if r.tier == "IDENTIFIER" for s in r.symbols]
            )
        )
        vc.main([], fetch_one=lambda url: page_with_everything)
        out = capsys.readouterr().out
        # The weaker tier must say what it does not establish, in the same breath.
        assert "has NOT had its claim verified" in out
        assert "rename and removal only" in out.lower()

    def test_the_tier_table_comes_before_any_result(self, capsys):
        vc.main(["--offline"])
        out = capsys.readouterr().out
        assert out.index("| GUIDE |") < out.index("## Checked")


class TestNothingCheckedIsNeverAPass:
    def test_offline_exits_two(self):
        assert vc.main(["--offline"]) == 2

    def test_a_failed_fetch_exits_two_and_outranks_a_finding(self, capsys):
        # Precedence matters: an incomplete run is worse to report than a known finding,
        # because you do not know what it would have found.
        def dead(url):
            raise OSError("no route to host")

        assert vc.main([], fetch_one=dead) == 2
        assert "Could not check" in capsys.readouterr().out

    def test_a_failed_fetch_counts_as_neither_pass_nor_fail(self, capsys):
        def dead(url):
            raise OSError("down")

        vc.main([], fetch_one=dead)
        out = capsys.readouterr().out
        assert "**0 still exact**" in out
        assert "**0 NOT FOUND**" in out

    def test_everything_present_exits_zero(self, capsys):
        # Proves the loop CAN pass. A gate that cannot be passed is as useless as one
        # that cannot be failed.
        rows = vc.collect()
        everything = page(
            " ".join(
                [r.quote for r in rows if r.tier == "VERBATIM"]
                + [s for r in rows if r.tier == "IDENTIFIER" for s in r.symbols]
            )
        )
        assert vc.main([], fetch_one=lambda url: everything) == 0

    def test_a_missing_quote_exits_one(self, capsys):
        assert vc.main([], fetch_one=lambda url: page("nothing relevant here")) == 1
        assert "**0 still exact**" in capsys.readouterr().out


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
        # host 22 times in seconds and invite a rate limit this script would then have to
        # report as "could not check" for a reason it caused itself.
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


class TestTheReportNamesItsLimits:
    def test_it_says_what_each_tier_does_not_show(self, capsys):
        vc.main(["--offline"])
        out = capsys.readouterr().out
        assert "What this report does not show" in out
        # The guide tier is the majority of the corpus, and the easiest to over-read.
        assert "not that the claim was right when written" in out
        # And the thing no tier reaches.
        assert "teaches" in out
