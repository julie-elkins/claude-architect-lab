# Lesson 2.3 — Fewer tools, and forcing the first one

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.3:** Distribute tools appropriately across agents and configure tool
choice.

Lab artifact: Course Doctor's tools scoped per agent role, with one extraction forced to
run first.

## What you will be able to do afterwards

Decide which agent in a system should hold which tools, and say what `tool_choice` buys
in each of its three settings.

## Why the exam cares

The guide gives a number, which is unusual enough to be worth noticing: **giving an agent
access to too many tools — "18 instead of 4-5" — degrades tool selection reliability by
increasing decision complexity.**

That single figure is the heart of the task statement, and it has a direct consequence for
lesson 2.4: if every configured MCP server's tools are live simultaneously, then adding
servers quietly moves you toward the eighteen.

The second half is `tool_choice`, and the guide names three settings precisely. Expect an
item where the right answer is forcing a specific tool and the tempting one is a firmer
instruction.

## Fundamentals

**Decision complexity.** The cost of choosing grows with the number of options. *Why it
matters here:* it is the stated mechanism — more tools, less reliable selection. *Depth:*
any treatment of choice overload; the effect transfers.

**Specialisation.** Giving a component only what its role needs. *Why it matters here:*
the guide observes agents with tools outside their specialisation tend to misuse them.
*Depth:* single responsibility again, one level up.

**Scoped access.** Permission narrowed to a role rather than granted globally. *Why it
matters here:* this is least privilege applied to an agent's toolbox. *Depth:* RBAC
literature.

**Forced dispatch.** Requiring a specific call rather than letting the model choose. *Why
it matters here:* that is `tool_choice` with a named tool, and it is a guarantee where a
prompt is a request. *Depth:* Domain 4 TS 4.3, which uses the same mechanism for
structured output.

## The idea, before any configuration

**Give each agent the tools its role needs and nothing else.** The guide's own example of
the failure is a synthesis agent attempting web searches — not because it is broken, but
because the tool was there.

**Then handle the high-frequency exception deliberately.** A pure separation forces every
cross-role need through the coordinator, which is a round trip. The guide's answer is a
*scoped cross-role tool*: give the synthesis agent a narrow `verify_fact` and route the
complex cases through the coordinator anyway. One tool, one purpose, not a general
capability.

**Replace generic tools with constrained ones.** The guide's example is swapping
`fetch_url` for `load_document` that validates document URLs. Same job, smaller blast
radius, and a description you can write precisely — which loops straight back to 2.1.

**And when order matters, force it.** If metadata extraction must happen before
enrichment, a prompt asking for that order has a non-zero failure rate. `tool_choice`
naming the tool does not.

## The build

### Step 1 — scope by role

Course Doctor's roles and their tools:

```
coordinator   : Task, read_manifest                      (delegates; does not fetch)
reader        : read_material_file                       (reads; does not fetch)
fetcher       : fetch_source                             (fetches; does not judge)
synthesiser   : write_findings, verify_claim             (judges; narrow cross-role tool)
```

Four roles, two to three tools each — inside the guide's 4–5 band rather than near its
eighteen. The synthesiser's `verify_claim` is the deliberate scoped exception: it is
high-frequency, and routing every instance through the coordinator would double the
traffic for no judgement gain.

### Step 2 — the three `tool_choice` settings

| Setting | Meaning |
|---|---|
| `"auto"` | The model may call a tool **or return text instead**. |
| `"any"` | The model **must** call a tool, but chooses which. |
| `{"type": "tool", "name": "..."}` | The model must call **that** tool. |

Read the first row again, because it is where the exam item lives: under `auto`, "please
always use the tool" is a request the model can decline by answering in prose. If you need
structured output rather than a sentence, `any` guarantees a tool call.

### Step 3 — force the one that must go first

```python
tool_choice = {"type": "tool", "name": "extract_metadata"}
```

The guide's own case: force `extract_metadata` so it runs before enrichment, then handle
the subsequent steps in follow-up turns. The forcing applies to one turn; the sequence is
built from turns.

### Step 4 — count before you add a server

Every configured MCP server's tools are available at once. So the audit is: list what each
agent can actually see, and if the number has drifted toward the teens, the fix is
narrowing per role — not better prompting.

## Tips

Things the documentation does not tell you.

**`tool_choice: "auto"` plus "always call the tool" is not a guarantee, and it fails
intermittently.** It works most of the time, which is worse than failing always, because
you will ship it.

**An agent misusing a tool outside its specialisation is a configuration finding, not a
prompt finding.** The guide's framing is that agents *tend* to misuse such tools. Removing
the tool is one line; teaching the agent not to reach for it is an ongoing argument.

**Forcing a tool constrains one turn, not a sequence.** If you need A then B, that is a
forced call followed by another turn — not one call with a plan in it.

**The 4–5 versus 18 figure is the most quotable thing in this domain.** It is also a
*modelling* claim in the guide rather than a measurement you can reproduce, so quote it as
the guide's number rather than as physics.

**A scoped cross-role tool beats both purity and generosity.** Full separation costs round
trips; shared access costs misuse. One narrow tool for the frequent case, coordinator for
the rest.

## The anti-pattern

From the guide's objectives:

> **Giving one agent access to too many tools** — 18 where 4–5 would do — degrading
> selection reliability.

> **Agents holding tools outside their specialisation**, which they tend to misuse.

And the `tool_choice` form, which is the same shape as every other failure in this course:

> **Relying on an instruction where a setting would guarantee it.**

A prompt asking the model to always call a tool, under `auto`, is context. `any` is a
control. On exam day, when one option is firmer wording and another is a configuration
value, the configuration is the answer.

## What this lesson does not cover

- **Tool descriptions** — lesson 2.1, and the first thing to fix if selection is
  unreliable *within* a small tool set.
- **MCP server configuration and scoping** — lesson 2.4.
- **Coordinator and subagent architecture** — Domain 1 TS 1.2 and 1.3. Here distribution
  is a configuration decision, not a system design.
- **Using `tool_choice` for structured output** — Domain 4 TS 4.3, same mechanism,
  different purpose.
- **Built-in tools** — lesson 2.5.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.3.

| Claim | Source |
|---|---|
| Too many tools (18 instead of 4-5) degrades tool selection reliability by increasing decision complexity | EG §6, TS 2.3 |
| Agents with tools outside their specialisation tend to misuse them, e.g. a synthesis agent attempting web searches | EG §6, TS 2.3 |
| Scoped tool access: only the tools a role needs, with limited cross-role tools for high-frequency needs | EG §6, TS 2.3 |
| `tool_choice` options are `"auto"`, `"any"`, and forced selection `{"type": "tool", "name": "..."}` | EG §6, TS 2.3 |
| Under `"auto"` the model may return text instead of calling a tool | EG §6, TS 4.3 |
| `"any"` guarantees the model calls a tool rather than returning conversational text | EG §6, TS 2.3 |
| Forcing a specific tool to run first, e.g. `extract_metadata` before enrichment, then processing subsequent steps in follow-up turns | EG §6, TS 2.3 |
| Replacing generic tools with constrained alternatives, e.g. `fetch_url` with `load_document` that validates document URLs | EG §6, TS 2.3 |
| Providing a scoped cross-role tool such as `verify_fact` for the synthesis agent while routing complex cases through the coordinator | EG §6, TS 2.3 |
| Tools from all configured MCP servers are available simultaneously | EG §6, TS 2.4 |
