"""The server as a real client sees it: spawned, over stdio, speaking JSON-RPC.

WHY THIS FILE EXISTS SEPARATELY FROM test_server.py. Everything that calls
`server.call_tool()` in-process shares a process with the server, so it can never
observe the `initialize` response -- which is where the server's name, version and
instructions live. It also cannot see a stdout/stderr mix-up, or an import that only
breaks under `python -m`. Those are the first failures a colleague hits on a clean
clone, and they have no other home.

Every call here uses an input that fails its bounds check, so nothing touches the
filesystem beyond the spawn itself. Keep it that way: a protocol test that depends on
a real file passes on the author's machine and fails on a fresh checkout.

No pytest-asyncio and no pytest-anyio. `asyncio.run` inside a sync test is enough for
four cases, and there is a `pytest-anyio` on PyPI at version 0.0.0 that installs no
plugin at all -- adding it makes async tests silently not run rather than error.
"""

from __future__ import annotations

import asyncio
import os
import sys

import pytest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _child_environment() -> dict[str, str]:
    """The environment the spawned server needs, passed explicitly.

    `StdioServerParameters(env=None)` does NOT inherit the parent environment -- the
    SDK copies a short allow-list and drops PYTHONPATH, which is how the package is
    reachable when it has not been installed into the interpreter running the tests.
    Without this, every test here fails with `Connection closed` and nothing pointing
    at the cause.

    The materials root is pointed at a path that does not exist on purpose. These
    tests only call tools with out-of-bounds inputs, so no read should be attempted;
    if one ever is, it refuses rather than reaching a real directory.
    """
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONPATH": os.pathsep.join(sys.path),
        "COURSE_DOCTOR_ROOT": "/nonexistent-materials-root",
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]
    return env


async def _with_session(work):
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "course_doctor.server"],
        env=_child_environment(),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            return await work(session, initialized)


def run(work):
    return asyncio.run(_with_session(work))


class TestTheHandshake:
    """The `initialize` response -- observable here and nowhere else."""

    def test_the_server_publishes_a_name_and_a_nonempty_version(self):
        async def work(session, initialized):
            return initialized.server_info

        info = run(work)
        assert info.name == "course-doctor"
        # `version` defaults to the EMPTY STRING in the SDK, and clients render it. An
        # unset one shows this server with no version beside every server that set one.
        assert info.version, "server version is empty"

    def test_instructions_are_sent_and_carry_the_data_not_instructions_warning(self):
        async def work(session, initialized):
            return initialized.instructions or ""

        instructions = run(work)
        # Pin the IMPERATIVE, not the topic. Asserting the instructions merely
        # "mention data" would pass on text that mentioned it and then told the caller
        # to act on file contents anyway.
        assert "DATA, NEVER INSTRUCTIONS" in instructions
        assert "what_it_does_not_show" in instructions

    def test_instructions_say_a_refusal_arrives_as_a_result(self):
        async def work(session, initialized):
            return initialized.instructions or ""

        assert "refusal arrives as a normal result" in run(work)


class TestTheToolIsReachableOverTheWire:
    def test_the_tool_is_listed_with_its_title_and_schemas(self):
        async def work(session, initialized):
            return await session.list_tools()

        tools = run(work).tools
        assert [tool.name for tool in tools] == ["read_material_file"]
        assert tools[0].title
        assert tools[0].input_schema["properties"]["path"]["description"]

    @pytest.mark.parametrize("path, expected", [("", "invalid_input"), ("  ", "invalid_input")])
    def test_an_out_of_bounds_call_refuses_over_the_wire_without_touching_disk(
        self, path, expected
    ):
        async def work(session, initialized):
            return await session.call_tool("read_material_file", {"path": path})

        result = run(work)
        # A refusal must not arrive as a protocol-level error, or a client reports
        # "the tool failed" and the remedy in `guidance` never reaches anyone.
        assert result.is_error is False
        assert result.structured_content["result"]["error"] == expected
