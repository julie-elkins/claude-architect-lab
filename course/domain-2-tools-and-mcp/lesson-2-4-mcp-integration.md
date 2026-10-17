# Lesson 2.4 — Wiring a server in, and what a populated `/mcp` does not prove

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.4:** Integrate MCP servers into Claude Code and agent workflows.

Lab artifact: Course Doctor's server wired at project scope, with its credential supplied
by the environment rather than written down.

## What you will be able to do afterwards

Configure a server at the right scope, pass it a secret without committing one, and say
what a server appearing in `/mcp` does and does not tell you.

## Why the exam cares

The guide names three things precisely: project-level `.mcp.json` for shared team tooling
against user-level `~/.claude.json` for personal and experimental servers, environment
variable expansion for credentials, and that **tools from all configured servers are
discovered at connection time and available simultaneously.**

That last one is the setup for a question. If every server's tools are live at once, then
adding servers is not free — it is Domain 2's own `tool_choice` problem arriving by the
back door, which lesson 2.3 covers.

## Fundamentals

**Client and server.** The client — Claude Code — connects to a server, asks what tools
it has, and calls them. The server does the work. *Why it matters here:* configuration is
entirely about telling the client where servers are. *Depth:* the protocol spec at
`modelcontextprotocol.io`.

**Transport.** How the two talk: `stdio` spawns a local process and speaks over its pipes;
`http` and `sse` reach a URL. *Why it matters here:* it decides which config fields apply
— `command` and `args` for stdio, `url` and `headers` for the rest. *Depth:* same spec.

**Environment variables.** Named values supplied by the shell rather than written in a
file. *Why it matters here:* the whole secret-handling answer. *Depth:* the twelve-factor
config chapter.

**Capability discovery.** Asking a server what it offers rather than being told in
advance — `tools/list`, `prompts/list`, `resources/list`. *Why it matters here:* it is why
a server's tool list can be present without the server being connected. *Depth:* the spec.

**Scope.** Who a configuration applies to. *Why it matters here:* same three-way split as
Domain 3, different file. *Depth:* lesson 3.1.

## The idea, before any files

**Who needs this server?** The team gets `.mcp.json`, committed. You alone get the user
or local scope in `~/.claude.json`. The guide frames the second as the experimental slot —
how you trial a server without pushing it on anyone.

**Where does the secret live?** Never in the file. The file names a variable; the
environment supplies the value. `.mcp.json` is committed, so a literal key there is a
published key, and rotating it becomes the cheapest part of a bad afternoon.

**What does the server's presence actually mean?** This is the question this lesson exists
for, and the answer is less than you would assume. See step 3.

## The build

### Step 1 — project scope, with the secret by reference

`.mcp.json` at the repository root:

```json
{
  "mcpServers": {
    "course-doctor": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "-m", "course_doctor.server"],
      "env": {
        "COURSE_DOCTOR_ROOT": "${CLAUDE_PROJECT_DIR}"
      }
    }
  }
}
```

Expansion works in `command`, `args`, `env`, `url` and `headers`, in two forms:
`${VAR}`, and `${VAR:-default}` which falls back when the variable is unset.

Three scopes, and they are easy to confuse because two share one file: **project** is
`.mcp.json` at the root and is shared via version control; **user** is `~/.claude.json`
globally and applies to all your projects; **local** is also `~/.claude.json` but stored
under this project's path, so it is this project only and not shared.

### Step 2 — the credential rule, and its boundary

For a **remote** server's `url` and `headers`, certain credential variables deliberately
read as **empty** rather than expanding:

> "Claude Code reads credential variables from your environment as empty rather than
> expanding them. This keeps a project's `.mcp.json` or a plugin from sending your Claude
> Code or cloud provider credentials to a server it names."

Covered: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `AWS_BEARER_TOKEN_BEDROCK`,
`HTTPS_PROXY`, `NPM_TOKEN` and others your environment carries.

**And here is the part to actually remember: your own names are not covered.** `API_KEY`
and `MY_CUSTOM_TOKEN` expand normally. So "credentials are protected in `.mcp.json`" is
the wrong lesson. The protection is specifically against a config file exfiltrating *the
credentials Claude Code itself uses*. Your service's token is yours to be careful with.

### Step 3 — what the server's presence proves

```
/mcp
```

Two documented behaviours make this weaker evidence than it looks.

**An unset variable with no default does not stop the server loading.** Claude Code
reports a missing-variable warning and uses the unexpanded `${VAR}` text as-is. So the
server registers, looks configured, and fails when a tool is first called — mid-task,
not at startup.

**A tool list can come from a cache rather than a connection.** A remote server you have
used before can show a status like `cached 2h ago · connects on first use · 5 tools`.
The tools appear immediately; the server is contacted when one is called.

So a populated `/mcp` tells you *a tool list exists*. It does not tell you the server is
reachable, authenticated, or currently working. **Call something.**

### Step 4 — expose a catalogue instead of making it guess

The guide names MCP **resources** as a way to expose content catalogues — issue
summaries, documentation hierarchies, database schemas — specifically to reduce
exploratory tool calls. An agent that can read a list of what exists does not need three
calls to discover it.

## Tips

Things the documentation does not tell you.

**A missing environment variable produces a mid-task failure, not a startup failure.**
The warning scrolls past, the server registers, and the break arrives when the tool is
called. If a server works for you and not a colleague, compare exported variables before
anything else — and check the shell you launched from, not the dotfile you think sets it.

**`${VAR:-default}` is the fix for the above and nearly free.** A default that is wrong
but present fails loudly at call time with a sensible message, where an unexpanded
`${VAR}` fails strangely.

**Both scopes are live at once, so a personal server can silently duplicate a team one.**
That is intended — it is how you trial a replacement — but two entries doing the same job
is a normal-looking state rather than an error, and you will debug the wrong one.

**An organisation `ask` control cannot be allowed away.** On claude.ai connectors, a tool
set to `ask` prompts on **every** call, in `acceptEdits`, `auto` and even
`bypassPermissions`, never offers to remember your choice, and an allow rule matching the
tool does not skip the prompt. A tool set to `blocked` is filtered out before Claude sees
it at all. If a tool prompts no matter what you configure, stop editing your settings.

**`timeout` is per-server and overrides the global.** Worth setting on a server whose
work is genuinely slow, rather than raising the global timeout for all of them.

## The anti-pattern

From the guide's objectives:

> **A secret written literally into a committed file.**

And the one this lesson adds, which the caching and warning behaviour hand you:

> **Reading a populated server list as a working server.**

Same shape as every other failure in this course: the absence of an error read as
evidence that nothing is wrong. A cached tool list and a live connection render
identically, and a server with an unexpanded variable looks exactly like one configured
correctly until something calls it.

The guide also names a third, worth knowing because it is counterintuitive:

> **Writing a custom server for a standard integration.**

Its stated preference is existing community servers for standard systems, with custom
servers reserved for team-specific workflows.

## What this lesson does not cover

- **Writing a server.** Lessons 2.1 and 2.2 are the tool surface and its error shapes.
- **Too many tools at once.** Lesson 2.3 — and it is the direct consequence of every
  server's tools being live simultaneously.
- **OAuth flows** for remote servers. Real, and not in this task statement's objectives.
- **MCP resources in depth.** Named here because the guide names them; the protocol
  detail is out of scope for Foundations.
- **Built-in tools** — lesson 2.5.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.4.

| Claim | Source |
|---|---|
| Project-level `.mcp.json` for shared team tooling vs user-level `~/.claude.json` for personal/experimental | EG §6, TS 2.4 |
| Environment variable expansion in `.mcp.json`, e.g. `${GITHUB_TOKEN}`, for credentials without committing secrets | EG §6, TS 2.4 |
| Tools from all configured servers are discovered at connection time and available simultaneously | EG §6, TS 2.4 |
| MCP resources expose content catalogues to reduce exploratory tool calls | EG §6, TS 2.4 |
| Prefer existing community servers for standard integrations; reserve custom ones for team-specific workflows | EG §6, TS 2.4 |
| Three scopes: local and user both in `~/.claude.json`, project in `.mcp.json` at the root | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| `${VAR}` and `${VAR:-default}` expand in `command`, `args`, `env`, `url`, `headers` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| Credential variables read as EMPTY in a remote server's `url` and `headers`; `ANTHROPIC_API_KEY`, `AWS_BEARER_TOKEN_BEDROCK`, `NPM_TOKEN` and others covered — `API_KEY` and `MY_CUSTOM_TOKEN` are NOT | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| An unset variable with no default still loads the server, warns, and uses the literal `${VAR}` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| Discovery happens via `tools/list`, `prompts/list`, `resources/list` after connection | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| A cached server can show `cached 2h ago · connects on first use · 5 tools` and connects on first call | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| An organisation `ask` control prompts every call in all permission modes, never remembers, and is not skipped by an allow rule; `blocked` filters the tool out before Claude sees it | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| `timeout` is a per-server tool execution timeout overriding `MCP_TOOL_TIMEOUT` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
