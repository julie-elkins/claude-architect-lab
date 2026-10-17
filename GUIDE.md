# Build to Pass — Claude Certified Architect – Foundations

**This file is generated. Do not edit it.**

It is the whole written course in one document, assembled from the per-lesson files
under `course/` by `scripts/build_guide.py`. Edit the lesson, then run:

```
python3 scripts/build_guide.py
```

The test suite checks this file against the lessons, so a stale guide fails the build
rather than quietly disagreeing with the course.

Lessons are in **dependency order**, not exam-weight order. See the
[repository README](README.md) for the exam details, the full 29-task-statement outline
including what is not yet written, how the course is sourced, and how to run the lab.

---

## Contents

- **TS 3.1** — Lesson 3.1 — Where an instruction lives decides who gets it
- **TS 3.5 and 3.6** — Lesson 3b — Iterating on purpose, and reviewing without yourself

---

# Lesson 3.1 — Where an instruction lives decides who gets it

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.1:** Configure CLAUDE.md files with appropriate hierarchy, scoping,
and modular organization.

Lab artifact: the Course Doctor repository gets its instructions, split so that only the
relevant ones load.

## What you will be able to do afterwards

Diagnose why a teammate is not getting an instruction you wrote, and put it at the level
that fixes it — without guessing.

And one thing more important than any of the file paths: say, correctly, what a
`CLAUDE.md` can and cannot make happen.

## Why the exam cares

The guide puts this first in the domain, and its own stated skill is **"diagnosing
configuration hierarchy issues (e.g., a new team member not receiving instructions
because they're in user-level rather than project-level configuration)."**

Read that carefully, because it tells you the shape of the question. You will not be
asked to recite file paths. You will be given a symptom — someone is not getting a rule
— and asked which level it belongs at. The test is never "how important is this rule."
It is **"who does it apply to."**

Get it backwards and nothing errors. It applies to the wrong people, silently, which is
why it makes a good exam item and a bad afternoon.

## Fundamentals

Skip what you know. Here so a newcomer has somewhere to go and a senior gets the
one-line refresh.

**Configuration scope.** Whether a setting belongs to you, to this project, or to your
organisation. *Why it matters here:* scope is the entire subject of this task statement,
and nearly every mistake in it is a scope mistake. *Depth:* any tool with both a home
dotfile and a committed config — `git`, `ssh`, `editorconfig` — resolves the same way.

**Context versus control.** A *control* prevents an action. *Context* informs a
decision. *Why it matters here:* this is the distinction the lesson turns on, and the
documentation states it outright — see the build. *Depth:* `/docs/en/hooks-guide`, which
is where the controls live.

**Version control hygiene.** Which files belong in the repository, which belong only on
your machine, and which belong in neither. *Why it matters here:* it is what makes the
user/project split meaningful rather than cosmetic. *Depth:* `git`'s own `.gitignore`
documentation.

**Glob patterns.** `*`, `**` and `?` matching file paths; `src/**/*.py` is every Python
file at any depth under `src`. *Why it matters here:* `.claude/rules/` files select the
files they apply to with a glob. *Depth:* `man 7 glob`. Lesson 3.3 is the full treatment.

**Monolith versus modules.** One large instruction file against several focused ones
loaded as needed. *Why it matters here:* the guide names `.claude/rules/` as the
alternative to a monolithic `CLAUDE.md`, and the reason is token cost rather than
tidiness. *Depth:* Domain 5, where context budget is the subject.

## The idea, before any files

Three questions, in this order.

**Who does this apply to?** Only you, or everyone who clones the repository? That single
question picks the level, and it is the one the exam asks.

**Is it context, or is it a control?** This is the distinction that catches people, and
the documentation is unusually blunt about it:

> "Claude treats them as context, not enforced configuration. **To block an action
> regardless of what Claude decides, use a PreToolUse hook instead.**"

So a line in `CLAUDE.md` saying *never force-push* is a request. A hook is a refusal.
Writing the request and believing you installed the refusal is the most expensive
mistake available in this domain, and it fails quietly — nothing blocks, because nothing
was ever configured to block.

**When does it need to load?** Everything loaded costs context, and context spent is
unavailable for the work. An instruction that matters only when editing test files
should not load while you edit the API.

## The build

### Step 1 — the project instruction file

```
mkdir course-doctor && cd course-doctor
git init
printf '# Course Doctor\n\nPython 3.12+. Tests live in tests/.\n' > CLAUDE.md
```

Project instructions go at `./CLAUDE.md` or `./.claude/CLAUDE.md`. Either is the
project level; both are committed; everyone who clones gets them.

### Step 2 — know what loads, and when

Two behaviours to hold, because they are the ones the symptom questions rest on.

**Files in the hierarchy above your working directory load at launch. Files in
subdirectories load on demand.** So a `CLAUDE.md` three directories up is already in
context when the session starts, and one in `src/api/` arrives only when you touch
something there.

**A project file does not suppress a parent one — they combine.** This is worth
verifying yourself rather than believing, and it is verifiable: put a line in a parent
directory's `CLAUDE.md`, start a session in the child, and look. Both load.

### Step 3 — split the monolith

As the instruction file grows, move topic-specific material into `.claude/rules/`:

```
mkdir -p .claude/rules
```

A rules file carries frontmatter naming the paths it applies to, so it loads only when a
matching file is in play. `paths: ["tests/**/*"]` keeps your testing conventions out of
context while you are editing something else. Lesson 3.3 is the full treatment; what
matters here is that it is the documented alternative to one large file.

The guide also names **`@import`** for referencing external files to keep `CLAUDE.md`
modular — importing a standards file into each package's instructions. See the sources
note below: that syntax is in the exam guide and I have not yet located it in the
documentation, so it is listed as an objective and not yet taught here.

### Step 4 — look at what actually loaded

```
/memory
```

Browse and open the instruction files the session is working from. And `/status` is
worth a look for a different reason: **if an instruction file is over the recommended
length you get a warning at startup and in `/status`, and you also get one when several
files that are each fine add up past a combined limit.** Each `CLAUDE.md`, each rules
file and each `@path` import counts separately toward that.

That is a real failure mode: no single file looks wrong, and together they are too much.

## Tips

Things the documentation does not tell you.

**There is no precedence between user and project rules, and this is the one to
remember.** The documentation says it plainly: *"Neither set overrides the other: if a
user rule and a project rule conflict, Claude may follow either one, so keep the two
consistent."* Everyone assumes the more specific level wins. It does not. If you have a
conflict, you do not have a precedence puzzle — you have a bug, and the fix is to remove
the conflict.

**A rule on one laptop is a personal habit, not a team convention.** The next person
does not inherit it, and you will not find out until their work diverges from yours for
reasons neither of you can see.

**Your own preferences in the project file get imposed on everyone who clones.** The
mirror of the mistake above, and the more annoying one to be on the receiving end of.

**A subdirectory instruction file is the hardest one to find later.** When something is
applying and you cannot see where it came from, you check the project file first and a
nested one last. Knowing they exist is most of the fix.

**Four short files can breach the limit that none of them breaches alone.** The combined
warning is easy to miss at startup. `/status` is where you look on purpose.

## The anti-pattern

From the guide's own skill statement for this task statement, the named failure is:

> **A new team member not receiving instructions because they are in user-level rather
> than project-level configuration.**

And the broader shape, which the documentation's own wording hands you:

> **Treating context as if it were a control.**

An instruction file asks. A hook prevents. If what you need is a guarantee — a
destructive command refused, a prerequisite enforced — then `CLAUDE.md` is the wrong
tool no matter how firmly it is worded, and on exam day an option offering a hook will
beat an option offering stronger instructions.

## What this lesson does not cover

- **`.claude/rules/` frontmatter and glob semantics in depth** — lesson 3.3.
- **Skills and slash commands** — lesson 3.2.
- **Hooks.** Named here because the context/control distinction is meaningless without
  them, taught in Domain 1 TS 1.5.
- **Auto memory.** Claude writes its own notes alongside the instructions you write.
  Adjacent, real, and not in this task statement's objectives.
- **`AGENTS.md`.** The documentation says Claude Code can read it in place of or
  alongside project instructions, with a table per file combination. Not in the exam
  guide's objectives for TS 3.1, so it is out of scope here — and I have an unresolved
  note claiming a `CLAUDE.md` suppresses it entirely, which that table may contradict.
  Unresolved is recorded as unresolved.
- **`@import`** — an objective, not yet traced to documentation. See sources.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.1.

| Claim | Source |
|---|---|
| The hierarchy is user-level, project-level, and directory-level | EG §6, TS 3.1 |
| User-level instructions are not shared with teammates via version control | EG §6, TS 3.1 |
| `@import` references external files to keep CLAUDE.md modular | EG §6, TS 3.1 |
| `.claude/rules/` organises topic-specific rules as an alternative to a monolithic CLAUDE.md | EG §6, TS 3.1 |
| Diagnosing hierarchy issues is a tested skill, with the new-team-member symptom named | EG §6, TS 3.1 |
| `/memory` browses and opens the instruction files in use | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Project instructions live at `./CLAUDE.md` or `./.claude/CLAUDE.md` | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Files above the working directory load at launch; subdirectory files load on demand | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| "Neither set overrides the other: if a user rule and a project rule conflict, Claude may follow either one" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Over-length warning at startup and in `/status`; separate combined-length warning; each CLAUDE.md, rules file and `@path` import counts separately | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |

**Outstanding, and stated rather than papered over:**

- [ ] **`@import` syntax.** The exam guide lists it under TS 3.1. Searched the memory
      documentation on 2026-10-17 and did not find it. It may be on another page, named
      differently, or the guide and the docs may disagree. **Not taught until resolved** —
      teaching a syntax from memory is the failure this course is about.
- [ ] The `AGENTS.md` per-combination table, for the scope note above.

**Verified by running it, 2026-10-13**, and now corroborated by the documentation above —
recorded as `OBSERVED` first and upgraded rather than quietly restated:

- A project `CLAUDE.md` does **not** suppress a parent one. Both loaded together.

---

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

## Fundamentals

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

**Official documentation links — REQUIRED BEFORE PUBLICATION, not yet fetched.** Each
needs a URL and a read date, and per this repo's rule a live link is not a verified
claim: the page has to still say what the row claims. Deliberately left unfilled rather
than written from memory, which is the failure this course is about.

- [x] **CLI reference** — `-p`/`--print`, `--output-format`, `--json-schema`,
      `--max-turns`, `--max-budget-usd`, `--permission-prompts`. Fetched and quoted
      2026-10-17: https://code.claude.com/docs/en/cli-reference
- [ ] `/docs/en/headless` — "Turn off permission prompts in unattended runs", and bare
      mode. Named by the CLI reference; not yet fetched.
- [ ] CLAUDE.md and memory documentation, for the CI-context mechanism —
      https://code.claude.com/docs/en/memory (fetched 2026-10-17 for Domain 3 facts;
      the CI-context claim specifically is not yet confirmed from it)
- [ ] Any documented guidance on independent review instances

Everything in **Tips** is `OBSERVED`, not cited — behaviour measured on one version,
a weaker claim than a documentation URL, labelled as such per the existing convention.

---
