"""The MCP adapter, called in-process, plus the surface properties nothing warns about.

The checks in `TestTheToolSurface` are the ones no tool, linter or SDK complains
about -- they are found only by reading, so they are pinned here instead. Each is
derived from the LIVE tool surface rather than a hand-maintained list, because a
list is a second copy that stops matching the day a tool is added.
"""

from __future__ import annotations

import pytest

from course_doctor import server as srv

# MEASURED against mcp 2.3.0: a tool annotated `-> Union[Result, Refusal]` has its
# payload wrapped one level deep under "result" in `structured_content`, rather than
# the model's fields appearing at the top level. A test written against the un-nested
# shape fails with a bare KeyError that says nothing about why, so the unwrap lives
# in one helper with this note attached.
def payload(call_result):
    return call_result.structured_content["result"]


@pytest.fixture
def tools():
    import asyncio

    return asyncio.run(srv.server.list_tools())


@pytest.fixture
def call(monkeypatch, tmp_path):
    """Call a tool with the materials root pointed at a temp directory."""
    import asyncio

    monkeypatch.setenv("COURSE_DOCTOR_ROOT", str(tmp_path))

    def _call(path):
        return payload(
            asyncio.run(srv.server.call_tool("read_material_file", {"path": path}))
        )

    _call.root = tmp_path
    return _call


class TestTheToolSurface:
    def test_every_tool_has_a_title(self, tools):
        # Unset means the client displays the raw function name, so a caller sees
        # `read_material_file` where a human-readable label belongs.
        for tool in tools:
            assert tool.title, f"{tool.name} has no title"

    def test_no_tool_name_is_a_strict_prefix_of_another(self, tools):
        # `Read` beside `ReadDetailed` is a shape models fumble: the bare sibling
        # reads as a dispatcher or a superset covering both cases when it is neither.
        # Trivially true with one tool, and it is here so it fails on the day a
        # second tool is added carelessly -- which is episode 2.
        names = [tool.name for tool in tools]
        for name in names:
            for other in names:
                if name != other:
                    assert not other.startswith(name), f"{other} is prefixed by {name}"

    def test_every_parameter_description_says_more_than_its_type(self, tools):
        # A length floor, because a bare type restatement ("the path, a string")
        # passes a truthiness check while telling a caller nothing. 80 characters is
        # a DESIGN DECISION rather than a measurement: it is about the length of one
        # sentence of consequence, and it is deliberately low enough that a real
        # description never has to be padded to clear it.
        for tool in tools:
            for name, schema in tool.input_schema.get("properties", {}).items():
                description = schema.get("description", "")
                assert len(description) >= 80, f"{tool.name}.{name} under-described"

    def test_every_array_parameter_shows_one_element_of_itself(self, tools):
        # A composite parameter renders as a nested schema an agent will not reliably
        # read, and the failure is silent: the call refuses correctly and the refusal
        # never names the shape. One literal example in the description is the fix.
        # No array parameters exist yet, so this is a guard placed before the need.
        for tool in tools:
            for name, schema in tool.input_schema.get("properties", {}).items():
                if schema.get("type") == "array":
                    assert "[" in schema.get("description", ""), (
                        f"{tool.name}.{name} is an array with no literal example"
                    )

    def test_read_only_annotations_leave_the_false_case_hints_unset(self, tools):
        # The spec defines destructiveHint and idempotentHint only for the
        # readOnlyHint=False case, so setting them here would publish a claim about a
        # case that cannot arise.
        for tool in tools:
            assert tool.annotations.read_only_hint is True
            assert tool.annotations.destructive_hint is None
            assert tool.annotations.idempotent_hint is None

    def test_open_world_hint_is_false_while_nothing_fetches(self, tools):
        # It becomes true in episode 2, when the network arrives. Pinned now so that
        # change is a deliberate edit to a failing test rather than an oversight.
        for tool in tools:
            assert tool.annotations.open_world_hint is False

    def test_output_schema_is_published(self, tools):
        # Returning a raw dict publishes an empty schema, so a caller has to invoke
        # the tool once to learn what comes back.
        for tool in tools:
            assert tool.output_schema
            assert tool.output_schema.get("$defs"), "no models in the output schema"


class TestASuccessfulRead:
    def test_reports_citations_and_a_hash(self, call):
        (call.root / "m.md").write_text(
            "see https://docs.claude.com/x", encoding="utf-8"
        )
        result = call("m.md")
        assert result["cited_urls"] == ["https://docs.claude.com/x"]
        assert len(result["sha256"]) == 64

    def test_what_it_does_not_show_is_populated_on_SUCCESS(self, call):
        # The whole design goal. A successful result that is silent about its own
        # coverage is indistinguishable from a complete one, which is the failure this
        # package exists to prevent -- so the field is required on the success path,
        # not only on refusals.
        (call.root / "m.md").write_text("x", encoding="utf-8")
        not_shown = call("m.md")["diagnostics"]["what_it_does_not_show"]
        assert "fetched" in not_shown.lower()
        assert len(not_shown) > 80

    def test_provenance_says_no_network_was_used(self, call):
        (call.root / "m.md").write_text("x", encoding="utf-8")
        assert "no network" in call("m.md")["diagnostics"]["provenance"]["source"]

    def test_material_citing_nothing_warns_but_still_succeeds(self, call):
        (call.root / "m.md").write_text("no links here", encoding="utf-8")
        result = call("m.md")
        assert result["cited_urls"] == []
        assert result["diagnostics"]["warnings"], "no warning for an uncheckable file"
        # It is a finding about the material, so it must not arrive as a refusal.
        assert "error" not in result

    def test_an_empty_warnings_list_does_not_mean_unqualified(self, call):
        # Pins the sentence the Diagnostics model promises. An empty `warnings` plus a
        # populated `what_it_does_not_show` is the normal successful shape, and a
        # caller treating empty warnings as "nothing to say" is the misread.
        (call.root / "m.md").write_text("see https://a.example/b", encoding="utf-8")
        result = call("m.md")
        assert result["diagnostics"]["warnings"] == []
        assert result["diagnostics"]["what_it_does_not_show"]


class TestRefusalsArriveAsResults:
    @pytest.mark.parametrize(
        "path, expected",
        [
            ("", "invalid_input"),
            ("missing.md", "not_found"),
            ("../escape.md", "outside_root"),
            ("/etc/passwd", "outside_root"),
        ],
    )
    def test_refusal_is_a_payload_not_an_exception(self, call, path, expected):
        # An agent formats whatever it is handed. A refusal raised as a transport
        # error gets summarised as "the tool failed" and the remedy is lost.
        result = call(path)
        assert result["error"] == expected
        assert result["guidance"]

    def test_a_refusal_says_nothing_was_read(self, call):
        # The specific misread this prevents: recording a failed call as a file that
        # cited no documentation, which is a clean-looking zero.
        not_shown = call("missing.md")["diagnostics"]["what_it_does_not_show"]
        assert "nothing was read" in not_shown.lower()
