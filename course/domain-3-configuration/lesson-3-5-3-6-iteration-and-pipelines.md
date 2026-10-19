# Lesson 3b — Iterating on purpose, and reviewing without yourself

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
Covers **TS 3.5** (iterative refinement techniques for progressive improvement) and
**TS 3.6** (integrate Claude Code into CI/CD pipelines). Episode 1 covers TS 3.1
through 3.4; these two complete the domain.

Written lesson. Lab artifact: Course Doctor gains a non-interactive invocation that
emits schema-valid JSON.

## What you will be able to do afterwards

Get a better result on the second attempt for a stated reason rather than by
rephrasing, and run the same agent in a pipeline where its output is parsed by a
machine instead of read by you.

## Why the exam cares

These two are a third of Domain 3 and they are the two that look least like
configuration, so they get skipped.

They also share a single idea, which is the reason to teach them together: **the
quality of what you get back is set by what you put in front of the model, not by how
firmly you ask.** TS 3.5 is that idea applied to your own iteration. TS 3.6 is the same
idea applied when there is no human in the loop to iterate at all.

Expect judgment items. "A reviewer's prose instructions produce inconsistent severity
classifications. What is the most effective fix?" has four plausible options, and the
tempting one — write firmer instructions — is the wrong answer the guide names.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

Skip what you know. Here so a newcomer has somewhere to go and a senior gets a
one-line refresh.

**Few-shot examples.** Showing two or three worked input/output pairs instead of
describing the transformation. *Why it matters here:* the guide states concrete
examples are the most effective way to communicate an expected transformation when
prose is interpreted inconsistently. This is Domain 4's central subject and it arrives
here first. *Depth:* Domain 4, TS 4.2.

**Test-driven development.** Write the failing test first, then make it pass. *Why it
matters here:* TS 3.5 names test-driven iteration explicitly — write the suite
covering expected behaviour, edge cases and performance, then iterate by *sharing the
failures*. The test output is the specific feedback that prose cannot be. *Depth:* any
TDD treatment; the mechanics transfer unchanged.

**Non-interactive execution.** Running a program with no terminal attached, so nothing
can answer a prompt. *Why it matters here:* this is what `-p` is for, and it is why an
interactive invocation in CI hangs rather than fails. *Depth:* the distinction between
a login shell and a batch job — `ssh host command` versus `ssh host`.

**JSON Schema.** A machine-readable description of what a JSON document must contain.
*Why it matters here:* `--json-schema` is how a CI step gets output it can parse
rather than prose it has to scrape. *Depth:* `json-schema.org`; Domain 4 TS 4.3 treats
it as a subject.

**Reviewer independence.** The idea that the author of a thing is the worst person to
check it. *Why it matters here:* the guide states that a session which generated code
is less effective at reviewing its own changes than an independent instance. This is
the same reason human code review exists, and it is the most transferable idea in the
lesson. *Depth:* Domain 4 TS 4.6 covers multi-instance review architectures.

**Idempotence.** An operation that can be run twice with the same result as once.
*Why it matters here:* a CI step that re-runs on every push must not post the same
finding twice, which is why prior findings go into context. *Depth:* REST method
semantics explain it cleanly.

## The idea, before any commands

**For iteration: replace the adjective with an artifact.**

The instinct when a result is wrong is to describe the problem better. The guide says
the opposite works: give a concrete input and the output you expected. Two or three
pairs beats a paragraph, because a paragraph can be read several ways and a pair
cannot.

The same move in three forms, all named in TS 3.5:

- A **worked example** instead of a description of the transformation.
- A **failing test** instead of a description of the bug.
- An **interview** — have Claude ask you questions before implementing — instead of a
  description of the requirements, when you are in a domain unfamiliar enough that you
  do not yet know what you have left out.

And one decision that is genuinely a judgment call: **when problems interact, put them
all in one message; when they are independent, fix them one at a time.** Interacting
fixes applied sequentially fight each other, and each round undoes the last.

**For pipelines: the human is not there, so the contract has to be explicit.**

Three things change when nobody is watching. There is no one to answer a prompt, so
interactive mode hangs. There is no one to read prose, so output has to be parseable.
And there is no one to notice that the reviewer and the author are the same session —
which the guide calls out as a real degradation, not a stylistic preference.

## The build

### Part one — iterate with artifacts

Course Doctor's drift report is returning inconsistent severities. The tempting fix:

```
"Be more conservative about what you flag as high severity."
```

The guide specifically names this shape as ineffective — "be conservative" and "only
report high-confidence findings" do not improve precision. Replace it with examples:

```
Example 1
  input:  a lesson citing a quota of 10 GB; the doc now says 20 GB
  output: severity HIGH, reason "numeric claim contradicted by current doc"

Example 2
  input:  a lesson citing a console path that has been renamed
  output: severity MEDIUM, reason "navigation changed, concept intact"

Example 3
  input:  a lesson whose cited page 404s
  output: severity UNKNOWN, reason "could not verify; not evidence of error"
```

Three pairs, and the third is doing the most work — it demonstrates the
ambiguous case, which is what the guide says few-shot examples are for.

Then the test-driven form. Write the assertion first:

```
./scripts/run-tests.sh 2>&1 | tail -20
```

Share the failure text, not a description of it. The test output names the expected
value, the actual value and the line — three facts your paragraph would have
approximated.

### Part two — run it with no human in it

Non-interactive, with machine-readable output:

```
claude -p "Check the lessons in course/ against their cited sources" \
  --output-format json \
  --json-schema schema/findings.json
```

Three flags, three jobs. `-p` (`--print`) runs without an interactive session, so
nothing waits for input. `--output-format json` makes the result parseable.
`--json-schema` constrains it to a shape your pipeline already knows how to read, so a
later step can post findings as inline comments without scraping prose.

Three more flags decide what happens when the run misbehaves, and all three are
documented and print-mode only:

```
claude -p "..." --max-turns 10 --max-budget-usd 2.00 --permission-prompts none
```

`--max-turns` limits agentic turns and **exits with an error** when the limit is
reached. `--max-budget-usd` stops the run once estimated spend reaches the amount —
note *estimated*, against a client-side figure that can differ from your bill, and
spend can pass the cap, so leave headroom. `--permission-prompts none` says nobody can
answer, so Claude Code denies prompts rather than waiting on them.

That last one matters more than it looks. By default in print mode, prompts go to the
Agent SDK host or a `--permission-prompt-tool`. If neither exists, you want the denial
rather than the wait.

### The security fact this lesson has to carry

A `-p` run is not a sandbox, and the documentation says so plainly:

> **"Without `--bare`, a `-p` session runs the hooks in a project's
> `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder
> you've never trusted. A `-p` session shows no workspace trust dialog and no per-server
> approval prompt."**

Read that against a CI pipeline reviewing a pull request from a fork. The repository under
review supplies the hooks that run and the MCP servers that connect, and nothing prompts.

`--bare` is the mitigation: it skips auto-discovery of hooks, skills, custom commands,
subagents, plugins, MCP servers, auto memory **and `CLAUDE.md`**. The docs call it *"the
recommended mode for scripted and SDK calls"* and say it *"will become the default for
`-p` in a future release."*

**Which creates a tension worth naming, because both sides are right.** The exam guide's
TS 3.6 objective is that `CLAUDE.md` supplies project context to a CI-invoked run — and it
does, *without* `--bare`. The documentation recommends `--bare` for CI, which skips
`CLAUDE.md`. If you want both the isolation and the context, pass it explicitly:
`--append-system-prompt-file` for instructions, `--settings` and `--mcp-config` for the
rest. For the exam, answer the guide. For a pipeline running untrusted code, read the
quote above twice.

**And `CLAUDE.md` is how the CI run learns about your project** — testing standards,
fixture conventions, review criteria. A CI-invoked run has no conversation history to
draw on, so whatever is not in the repository's instructions is not available to it.
That is the same hierarchy from episode 1, doing its most load-bearing work in the
place you cannot watch.

Then the part people get wrong. **Do not have the session that generated the code
review it.** Run the review as an independent invocation with no prior context. And
when re-running after new commits, include the previous findings in context with an
instruction to report only new or still-unaddressed issues — otherwise every push
posts the same comments again.

## Tips

Things that cost somebody an hour. None is in the documentation.

**A missing `-p` in CI costs you the whole timeout, not a fast failure.** Without print
mode there is no one to answer a permission prompt, and the job's error names the
timeout rather than the flag. If a step takes exactly as long as your timeout setting,
suspect the invocation before anything else — and pass `--permission-prompts none` so a
prompt becomes a denial instead of a wait.

**"Be more conservative" is the instruction that feels like a fix and is not.** It
reads as a tightening and changes nothing measurable. The guide names it. When you
catch yourself adding an adverb to a prompt, you want an example instead.

**Redirect stderr or you lose the only useful line.** `> log.txt` saves stdout and
leaves the traceback on a stream nobody captured. `2>&1` is four characters.

**Re-running a review without the prior findings duplicates every comment.** The second
run has no memory of the first, so it is not repeating itself — it is seeing the
repository for the first time, again. Feeding yesterday's findings in is what makes it
incremental.

**The third few-shot example is the one that earns its place.** Two examples show the
format. The third, covering the ambiguous case, is what lets the model generalise
rather than pattern-match — which is the difference the guide is pointing at.

## The anti-pattern

The guide names these explicitly, and the shapes to recognise are:

> **Firmer prose where a concrete example is needed.**

"Be conservative", "only report high-confidence findings", "be more careful about
severity" — all named as failing to improve precision compared to specific categorical
criteria. On exam day, if one option is an adverb and another is an input/output pair,
the pair is the answer.

> **Self-review in the generating session.**

Asking the same instance to check its own work, or reaching for a "review your output
carefully" instruction, instead of an independent instance with no reasoning context.
The failure is not that the model is careless; it is that it retains the reasoning that
produced the thing and is therefore unlikely to question it.

> **Sequential fixes for interacting problems.**

Fixing three issues one at a time when each change affects the others, so every round
partially undoes the last. The published distinction is interacting versus independent,
and it decides the batching.

## What this lesson does not cover

- **Few-shot prompting as a subject.** Introduced here because TS 3.5 depends on it;
  Domain 4 TS 4.2 is where it is taught properly.
- **JSON Schema design.** Same — used here, taught in Domain 4 TS 4.3.
- **Multi-instance review architecture.** The *why* is here because TS 3.6 names it;
  the architecture is Domain 4 TS 4.6.
- **Batch processing.** Adjacent and tempting to bolt on. It is Domain 4 TS 4.5, and
  the Message Batches API has its own latency and tool-calling constraints.
- **A specific CI provider's syntax.** The task statement is Claude Code in a pipeline,
  not any one pipeline. The flags transfer; the YAML does not.
- **Cost figures.** None appear here. Any number would be one person's usage.

## Sources

CCAR-F exam guide **Version 1.0, effective July 2026**, §6:

| Claim | Source |
|---|---|
| Concrete input/output examples beat prose when prose is read inconsistently | EG §6, TS 3.5 |
| "Be conservative" style instructions fail to improve precision | EG §6, TS 3.5 and TS 4.1 |
| Test-driven iteration: suite first, then share failures | EG §6, TS 3.5 |
| The interview pattern surfaces unanticipated considerations | EG §6, TS 3.5 |
| Interacting issues in one message; independent issues sequentially | EG §6, TS 3.5 |
| `-p` / `--print` runs Claude Code non-interactively in pipelines | EG §6, TS 3.6 |
| `--output-format json` and `--json-schema` enforce structured output in CI | EG §6, TS 3.6 |
| CLAUDE.md supplies project context to a CI-invoked run | EG §6, TS 3.6 |
| A session that generated code is less effective at reviewing its own changes | EG §6, TS 3.6 |
| Including prior findings avoids duplicate PR comments on re-run | EG §6, TS 3.6 |
| `-p` / `--print`: "Print response without interactive mode" | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--output-format` takes `text`, `json`, `stream-json`; print mode only | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--json-schema` returns validated JSON matching a schema; print mode only | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--max-turns` limits agentic turns and exits with an error at the limit | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--max-budget-usd` stops on ESTIMATED spend; spend can pass the cap | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--permission-prompts none` denies prompts when nobody can answer | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--permission-prompts none` denies anything that would prompt unless a `PermissionRequest` hook allows it, tells Claude not to retry, and removes tools needing a person such as `AskUserQuestion`; denials appear as `permission_denied` and in `permission_denials` | [headless docs](https://code.claude.com/docs/en/headless), read 2026-10-17 |
| `--bare` is "the recommended mode for scripted and SDK calls" and "will become the default for `-p` in a future release" | [headless docs](https://code.claude.com/docs/en/headless), read 2026-10-17 |
| Without `--bare`, a `-p` run loads hooks, skills, commands, subagents, plugins, MCP servers, auto memory and CLAUDE.md as an interactive session would | [headless docs](https://code.claude.com/docs/en/headless), read 2026-10-17 |
| "Without `--bare`, a `-p` session runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted" — with no trust dialog and no per-server approval prompt | [headless docs](https://code.claude.com/docs/en/headless), read 2026-10-17 |

**Official documentation links — REQUIRED BEFORE PUBLICATION, not yet fetched.** Each
needs a URL and a read date, and per this repo's rule a live link is not a verified
claim: the page has to still say what the row claims. Deliberately left unfilled rather
than written from memory, which is the failure this course is about.

- [x] **CLI reference** — `-p`/`--print`, `--output-format`, `--json-schema`,
      `--max-turns`, `--max-budget-usd`, `--permission-prompts`. Fetched and quoted
      2026-10-17: https://code.claude.com/docs/en/cli-reference
- [x] **`/docs/en/headless`** — fetched 2026-10-17. `--permission-prompts none`, bare
      mode, and the untrusted-folder behaviour now cited in the lesson.
- [x] **CLAUDE.md in a `-p` run** — confirmed 2026-10-17 from `/docs/en/headless`:
      without `--bare`, a `-p` run "discovers and loads them as an interactive session
      would, including anything configured in the working directory or `~/.claude`."
      So the guide's CI-context objective holds, and `--bare` is what turns it off.
- [~] **Independent review instances** — the rationale is the exam guide's (TS 3.6 and
      TS 4.6) and is **not stated in the documentation.** What the docs do is demonstrate
      the pattern: `gh pr diff "$1" | claude -p --append-system-prompt "You are a security
      engineer. Review for vulnerabilities."` — a fresh instance reviewing a diff it did
      not produce. Recorded as pattern-demonstrated, rationale-uncited, rather than
      closed.

Everything in **Tips** is `OBSERVED`, not cited — behaviour measured on one version,
a weaker claim than a documentation URL, labelled as such per the existing convention.
