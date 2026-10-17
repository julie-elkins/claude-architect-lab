# Glossary

Terms this course uses across more than one lesson, with the senses kept apart.

Most of these are here because **the same word means different things in different
lessons** — not through sloppiness, but because the product and the exam guide both reuse
them. Each entry says which sense belongs where, and what confusing them costs.

---

## fork

**Three distinct things, and they are the most confusable terms in the course.**

- **Fork a session** — `claude --continue --fork-session`, or `/branch` inside a session.
  Copies the conversation to a new session id, leaves the original intact.
  [lesson 1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md)
- **Fork a conversation into a subagent** — `/subtask`. A subagent that inherits the
  *entire* conversation instead of starting fresh.
  [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md)
- **`context: fork` on a skill** — runs the skill in an isolated subagent that does **not**
  see your conversation history.
  [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md)

**What confusing them costs:** the second inherits everything and the third inherits
nothing. Using a conversation-fork as a reviewer reproduces exactly the reasoning context
you were trying to remove — see
[lesson 4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md).
Also: `/branch` keeps your session permission grants because it stays in the same process;
`--fork-session` starts a new process and you re-approve.

## subagent

A separate agent with its own context window.
[1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md),
[1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md)

A **non-fork** subagent starts fresh: no conversation history, no prior file reads, only a
delegation message. A **background** subagent keeps a restricted tool set — Claude Code
*"removes every other built-in tool… whether inherited or listed in the `tools` field"* —
so a tool you granted can be absent.

## Task tool / Agent tool

**A naming conflict the course records rather than resolves.** The exam guide names the
**`Task`** tool and the requirement that `allowedTools` include `"Task"` to spawn
subagents. The current documentation names the **`Agent`** tool, and the tools reference
has no `Task` row. The tested objective — a coordinator cannot spawn without the spawning
tool in its allowed list — holds under either name.
[lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md)

## turn

One round trip: the model produces output including tool calls, the tools run, the results
feed back. The loop ends when output contains no tool calls.
[lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md)

`max_turns` counts **tool-use turns only**, and hitting it returns a result with subtype
`error_max_turns` — not a normal result with less in it.

## stop_reason

**Two layers, and the exam guide and the SDK docs describe different ones.** At the
Messages API level it distinguishes `tool_use` (the model wants a tool run) from `end_turn`
(finished) — which is what the guide describes. On the SDK's *result*, common values are
`end_turn`, `max_tokens` and `refusal`, and loop termination is described through the
no-tool-calls condition instead. Same mechanism, different altitude.
[lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md)

Also load-bearing in [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md):
check it before parsing, because on a refusal or a truncation the payload will not match
your schema.

## context

Three senses, all in play:

- **The context window** — everything loaded, which accumulates across turns and does not
  reset. [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md),
  [5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md)
- **Context versus control** — information that *informs* a decision against a mechanism
  that *prevents* an action. The distinction behind theme 1.
  [3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md)
- **Context passed to a subagent** — what you put in its prompt, because it inherits
  nothing. [1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md)

## instructions, rules, memory

- **`CLAUDE.md`** — instructions you write. Load at launch from the hierarchy above the
  working directory; subdirectory files load on demand. Context, not enforcement.
- **`.claude/rules/`** — topic files with a `paths` glob, loading only when a matching file
  is in play. `paths` is the only field read; **invalid YAML means the rule loads
  unconditionally.**
- **Auto memory** — notes Claude writes itself across sessions.
- **`@path/to/import`** — not a literal `@import`; pulls another file in at launch.
  **Organises, does not reduce context cost**, because imported files load at launch too.

[3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md),
[3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md)

## skill / slash command

A **skill** is a directory at `.claude/skills/<name>/SKILL.md` with frontmatter, able to
carry supporting files, reloading live during a session. A **custom command** is a single
file at `.claude/commands/<name>.md` — the legacy form, same `/name`, no live reload, no
plugin support. Both are invocable as `/name`.
[lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md)

## allowed-tools / disallowed-tools / tools

**The distinction that costs people reach they did not intend.**

- **`allowed-tools`** (skill) and **`allowedTools`** (SDK) **pre-approve** — they remove the
  prompt for tools the thing would have used anyway. They do **not** restrict.
- **`disallowed-tools`** removes tools from the pool. This is the one that restricts.
- **`tools`** (subagent frontmatter) is an allowlist of what the subagent may have — and a
  background subagent has entries stripped from it anyway.

[3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md),
[1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md),
[2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md)

## hook

Code that runs at a lifecycle point. `PreToolUse` can block a call (exit 2, or
`permissionDecision`) or rewrite its input; `PostToolUse` can rewrite the result and
**cannot prevent anything** — the call already ran.

**Default on failure is non-blocking**: a missing script, a timeout or a crash lets the
action proceed. `onFailure: "block"` changes that.
[lesson 1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md)

## plan mode

Claude researches and proposes without editing. **Enforced** in headless `-p` runs, Agent
SDK sessions and the VS Code chat panel. **Not enforced** in an interactive terminal with
bypass permissions available, where it remains an instruction.
[lesson 3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md)

## tool_choice

`"auto"` — the model may call a tool **or return text**. `"any"` — must call one, chooses
which. `{"type": "tool", "name": "…"}` — must call that one. The first row is where the
exam item lives.
[2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md),
[4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md)

## confidence

**Ruled out as a filter; valid as a routing signal.** Not a contradiction —
uncalibrated it is a word, and "only report high-confidence findings" is named as failing
([4.1](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md)) as is
sentiment- or confidence-based escalation
([5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md)). Calibrated
against labelled outcomes it routes review attention
([4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md),
[5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md)).

## empty result versus access failure

A query that succeeded and matched nothing, against an operation that did not happen. Both
are "no data" and they call for opposite responses. They need **different types**, not one
type with a flag, because a flag survives one hop and gets dropped at the next.
[2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md),
[5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md)

## calibration

Whether a stated confidence matches observed accuracy — things marked 90% confident being
right about 90% of the time. Measured against a **labelled validation set**, not asserted.
[lesson 5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md)

## stratified random sampling

Sampling randomly *within* defined strata rather than across the whole population, so a
rare-but-important segment is actually represented. The guide's instruction is to sample
the **high-confidence** population — the one nobody will otherwise look at.
[lesson 5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md)

## attention dilution

One pass asked to hold too many concerns, so each gets less — the stated reason to split
per-item local analysis from a cross-item integration pass.
[1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md),
[4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md)

## prompt chaining versus adaptive decomposition

A **fixed sequence** where each step feeds the next, against **generating the next subtask
from what the last one found.** The discriminator is whether you know the steps before
starting.
[lesson 1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md)

## structured outputs versus tool-use-as-schema

The exam guide teaches **tool use with a JSON schema** as the way to guarantee shape. The
current API also has a dedicated **structured outputs** feature using constrained decoding
(`output_config.format`, `strict: true`). Both are real; the exam tests the former.
[lesson 4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md)

## OBSERVED versus cited

A convention in [SOURCES.md](SOURCES.md), not a product term. **Cited** means traced to the
exam guide or a documentation URL with a read date. **OBSERVED** means measured by running
something on one version — a weaker claim, labelled as such rather than presented as a
documented contract.

## compaction, `/clear`, summarisation

**Compaction** replaces older history with a summary when the window fills, so early
instructions may not survive — which is why persistent rules belong in `CLAUDE.md`, which
is re-injected every request. **`/clear`** starts empty. **Progressive summarisation** is
the risk that numbers, dates and stated expectations get condensed into vague prose.
[1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md),
[5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md),
[5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md)
