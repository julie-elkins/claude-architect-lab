# Recall sheet — the half you cannot reason out

**⚠ The lessons are authoritative. This page restates them and nothing more.** If this
sheet and a lesson disagree, the lesson is right and this file is stale — report it.

## Why this page exists

Every other page here teaches judgment, because most of this exam rewards it: given a
requirement, choose the design. Judgment is what a course can actually build.

But a closed-book exam also asks which file lives where, which flag does what, and what a
particular enum value means. **You cannot derive those.** They are conventions somebody
chose, and either you have them or you do not — no amount of architectural instinct
recovers the name of a frontmatter field.

So this page is the recall surface, and it is deliberately the thinnest page in the
repository: **no explanations, no reasoning, no new facts.** Every row restates something a
lesson already teaches and already cites, and links to that lesson. Read the lesson to
understand a row; read the row to remember it.

**What this page is not.** It is not a prediction of what is on the exam. No item count,
no weighting and no "expect this" appears here — the guide publishes domain weights and
nothing finer, and anything more specific would be guesswork dressed as preparation. It is
also not a substitute for the lessons: a sheet of conventions with the reasoning stripped
out is exactly the material that gets you to 700.

**Use it twice.** Once a week early, to find out which rows you cannot produce from
memory — those are your gaps, and they are cheap to close. Then once the night before,
when there is no time left to learn anything that needs understanding.

---

## Where a file lives

| Path | What it is | Lesson |
|---|---|---|
| `CLAUDE.md` | Instructions you write. Context, not enforcement | [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| `.claude/rules/` | Topic files carrying a `paths` glob, loaded conditionally | [lesson 3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) |
| `.claude/skills/<name>/SKILL.md` | A skill: a directory, so it can carry supporting files | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `.claude/commands/<name>.md` | A custom command: one file, the legacy form of the same `/name` | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `.mcp.json` | Project MCP servers, checked in with the project | [lesson 2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) |

**Loading order, and the part people get backwards:** `CLAUDE.md` files *above* the working
directory load at launch; files in *subdirectories* load on demand. See
[lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md).

## Frontmatter fields, by file

| Field | Where it goes | What it does | Lesson |
|---|---|---|---|
| `paths` | `.claude/rules/` file | Glob deciding when the rule loads. The only field read | [lesson 3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) |
| `context: fork` | a skill | Runs it in a subagent that cannot see your conversation | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `allowed-tools` | a skill | **Pre-approves.** Removes the prompt; does not restrict | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `tools` | a subagent | Allowlist of what that subagent may have | [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |

## The three reach fields, which are not three names for one thing

| Field | Direction | Lesson |
|---|---|---|
| `allowed-tools` (skill), `allowedTools` (SDK) | Pre-approve. Removes the prompt for tools it would have used anyway | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `disallowed-tools` | Restrict. Removes tools from the pool. **This is the only one that restricts** | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| `tools` (subagent frontmatter) | Allowlist for a subagent — and a background subagent has entries stripped from it anyway | [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |

## Flags for a non-interactive run

| Flag | Effect | Lesson |
|---|---|---|
| `-p` / `--print` | Runs non-interactively, for a pipeline | [lesson 3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| `--output-format` | `text`, `json` or `stream-json` | [lesson 3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| `--json-schema` | Enforces a shape on the output in CI | [lesson 3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| `--fork-session` | With `--continue`: copies the conversation to a new session id | [lesson 1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) |

## Values worth knowing cold

| Name | Values, and the catch | Lesson |
|---|---|---|
| `tool_choice` | `"auto"` may return text instead of calling; `"any"` must call one and picks; `{"type": "tool", "name": "…"}` must call that one | [lesson 2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) |
| `stop_reason` | Two altitudes. Messages API distinguishes `tool_use` from `end_turn`; on the SDK result, `end_turn`, `max_tokens`, `refusal` | [lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) |
| `max_turns` | Counts **tool-use turns only** | [lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) |
| `PreToolUse` | Can block a call or rewrite its input | [lesson 1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |
| `PostToolUse` | Can rewrite the result and **cannot prevent anything** — the call already ran | [lesson 1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |

## Where the default is the opposite of the guess

The highest-value rows on this page. Each one is a convention whose default surprises
people, which is exactly what makes it answerable in one line and worth a question.

| The thing | The default | Lesson |
|---|---|---|
| A rule file with invalid YAML | Loads **unconditionally** — it does not silently vanish | [lesson 3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) |
| A user rule against a project rule | **No precedence either way.** Neither overrides the other, so keep them consistent | [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| A project `CLAUDE.md` under a parent one | Does **not** suppress the parent. Both load | [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| An `@` import | Not a literal `@import`, and it **does not reduce context cost** — imports load at launch too | [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| Plan mode in an interactive terminal with bypass permissions available | **Not enforced.** It is a control in headless `-p`, Agent SDK and the VS Code chat panel, and an instruction here | [lesson 3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) |
| A hook that crashes, times out or is missing | **Non-blocking.** The action proceeds | [lesson 1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |
| A subagent's inherited context | Inherits **nothing** unless you forked the conversation into it | [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |
| A background subagent's tools | Built-in tools are **stripped**, inherited or listed | [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |
| Compaction | Replaces older history with a summary, so early instructions may not survive — `CLAUDE.md` is re-injected every request | [lesson 5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) |

## Three terms the course deliberately keeps apart

Not conventions, but they cost marks the same way — each is one word covering more than one
mechanism, and [GLOSSARY.md](GLOSSARY.md) is the full treatment.

- **`fork`** means three things: forking a session, forking a conversation into a subagent,
  and `context: fork` on a skill. The second inherits everything; the third inherits
  nothing.
- **The `Task` tool and the `Agent` tool** are the same tested objective under two names —
  the guide uses one, current documentation the other.
- **Structured outputs against tool-use-as-schema** are both real. **The exam tests tool
  use with a JSON schema.**

## Sources

**No row here is a new claim.** Every one restates a lesson that carries its own citation —
exam-guide section or documentation URL with a read date — and links to it, so this page
adds nothing to verify and nothing that can be verified independently of the lessons.

**The honest limit, stated because this page's shape invites the error.**
`scripts/check_citations.py` reads the lessons in the build manifest, not the pages at the
repository root, so nothing mechanically citation-checks this file. What *is* checked:
`tests/test_guide.py` asserts every lesson this page links to exists, and that each row's
term still appears in the lesson it points at. That catches a renamed flag or a deleted
lesson. **It cannot catch a row whose meaning drifted while its wording stayed** — the same
limit `scripts/check_production.py` carries for the episode scripts, and the reason the
warning at the top of this page is a warning rather than a note.

See [SOURCES.md](SOURCES.md) for what this course treats as a source, and
[VERIFICATION.md](VERIFICATION.md) for which cited pages have been re-read verbatim.
