# Build to Pass: Claude Certified Architect – Foundations (CCAR-F)

A hands-on course and lab for the **Claude Certified Architect – Foundations** certification.
Five episodes, one per exam domain. You finish with a working system, not a set of notes.

I hold this credential. I also build certification exams for a living, which is why this course
is organised around the published blueprint and its anti-patterns rather than around a feature
tour.

Anthropic's Partner Academy courses cover the concepts. **This course builds the system.**

---

## Why "build to pass"

The exam guide says what it is measuring, and it is not recall:

> Candidates must demonstrate not only conceptual knowledge but practical judgment about
> architecture, configuration, and tradeoffs in production deployments.

Scenario-based, judgment-weighted exams are hard to study for by reading, because the question
is rarely "what does this feature do" and usually "which of these four defensible choices is
right here." The way to get fluent in tradeoffs is to make them. So each episode teaches one
domain by building one working piece of the same system.

## The exam, from the published exam guide

| | |
|---|---|
| Exam code | CCAR-F |
| Items | 60, multiple-choice and multiple-response (each item states how many to select) |
| Structure | 4 scenarios, drawn at random from a published bank of 6 |
| Time | 120 minutes |
| Passing score | 720 scaled, on a range of 100–1,000 |
| Fee | $125 USD |
| Validity | **12 months** from the date the credential is awarded |
| Score report | Pass/fail with scaled score, plus percent-correct by domain |

Two things worth knowing before you book. The credential is **valid for 12 months**, which is
shorter than most cloud certifications and should shape when you sit it. And the score report
gives you percent-correct **per domain** — useful diagnostics, but those section percentages do
not determine pass or fail. Only the total scaled score does.

## The course

**Twenty-nine lessons, one per task statement in the published exam guide.** The guide
names what it measures, objective by objective, and exam items are written against those
objectives — so a chapter structure invented on top would be a second thing to keep in
sync, and the first time it drifted a lesson would teach something the exam does not test.

**Read in the order below.** It is dependency order, not exam-weight order: the tools
have to exist before the loop that calls them, and the loop before the output it shapes.
Domain 1 is the largest slice of the exam and still cannot come first.

Each lesson is a single file you read start to finish: what you will be able to do
afterwards · why the exam cares · **fundamentals** (skippable — glosses for a newcomer,
a refresh for a senior) · the build, with real commands · **tips** the documentation does
not tell you · the published anti-pattern · what the lesson does not cover · sources.

**Prefer one long page? [Read the whole course as a single document](GUIDE.md).** It is
generated from the lessons below by `scripts/build_guide.py`, and the test suite fails if
it goes stale, so it cannot quietly disagree with them.

**Status: 6 of 29 written — Domain 3 is complete.** A lesson is a link only when it exists. Nothing below is a
stub — fifteen empty files read as abandoned work, where a listed objective reads as a
plan and stops one being quietly dropped.

### Domain 3 — Claude Code Configuration & Workflows · 20%

| | Task statement | |
|---|---|---|
| 3.1 | Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization | [read](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| 3.2 | Create and configure custom slash commands and skills | [read](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| 3.3 | Apply path-specific rules for conditional convention loading | [read](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) |
| 3.4 | Determine when to use plan mode vs direct execution | [read](course/domain-3-configuration/lesson-3-4-plan-mode.md) |
| 3.5 | Apply iterative refinement techniques for progressive improvement | [read](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| 3.6 | Integrate Claude Code into CI/CD pipelines | [read](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |

### Domain 2 — Tool Design & MCP Integration · 18%

| | Task statement | |
|---|---|---|
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries | planned |
| 2.2 | Implement structured error responses for MCP tools | planned |
| 2.3 | Distribute tools appropriately across agents and configure tool choice | planned |
| 2.4 | Integrate MCP servers into Claude Code and agent workflows | planned |
| 2.5 | Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively | planned |

### Domain 1 — Agentic Architecture & Orchestration · 27%

| | Task statement | |
|---|---|---|
| 1.1 | Design and implement agentic loops for autonomous task execution | planned |
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns | planned |
| 1.3 | Configure subagent invocation, context passing, and spawning | planned |
| 1.4 | Implement multi-step workflows with enforcement and handoff patterns | planned |
| 1.5 | Apply Agent SDK hooks for tool call interception and data normalization | planned |
| 1.6 | Design task decomposition strategies for complex workflows | planned |
| 1.7 | Manage session state, resumption, and forking | planned |

### Domain 4 — Prompt Engineering & Structured Output · 20%

| | Task statement | |
|---|---|---|
| 4.1 | Design prompts with explicit criteria to improve precision and reduce false positives | planned |
| 4.2 | Apply few-shot prompting to improve output consistency and quality | planned |
| 4.3 | Enforce structured output using tool use and JSON schemas | planned |
| 4.4 | Implement validation, retry, and feedback loops for extraction quality | planned |
| 4.5 | Design efficient batch processing strategies | planned |
| 4.6 | Design multi-instance and multi-pass review architectures | planned |

### Domain 5 — Context Management & Reliability · 15%

| | Task statement | |
|---|---|---|
| 5.1 | Manage conversation context to preserve critical information across long interactions | planned |
| 5.2 | Design effective escalation and ambiguity resolution patterns | planned |
| 5.3 | Implement error propagation strategies across multi-agent systems | planned |
| 5.4 | Manage context effectively in large codebase exploration | planned |
| 5.5 | Design human review workflows and confidence calibration | planned |

**Domain 3 is written in full.** Its video script lives at
[course/domain-3-configuration/production/](course/domain-3-configuration/production/) —
a **production asset** covering TS 3.1 through 3.4 as narration, kept because the video
is planned. It is not the course. Domain 2 is next.

## The lab: Course Doctor

One system, built across the five episodes: an agent that checks a set of training materials
against live documentation and reports **what went stale, what it could not check, and what
needs a human.**

It needs all five domains honestly — MCP tools to fetch and compare, a coordinator with
subagents to fan out across sections, a JSON schema to make the findings machine-checkable,
and context discipline to keep provenance attached to every claim.

The design rule it is built around: **silence reads as healthy.** When a fetch fails or a
permission check refuses, most tools return a report that looks clean, and that is how you end
up trusting a green result over a broken run. So every finding carries what it does not cover,
and `unchecked` is a state this tool is not allowed to collapse into `fine`.

I built the machine-learning version of this detector first, in
[driftwood](https://github.com/julie-elkins/driftwood), and **published the result that it lost
to a baseline that flags nothing at all** — F1 0.364 against 0.448. This is the version that
works, and it works because detection is deterministic and only the judgment is delegated to a
model. The negative result is why the design looks like this.

## How this course is sourced, and why that matters here

Everything taught here comes from one of two places: the **published CCAR-F exam guide**, or
the **public Claude documentation**. Every lesson claim is traced to its source in
[SOURCES.md](SOURCES.md), by exam-guide section or by URL.

Nothing in this course comes from sitting the exam. Exam content — questions, answer options,
and the scenarios as presented in the exam itself — is confidential under the non-disclosure
agreement every candidate accepts, and it stays that way. The six scenarios discussed here are
discussed because **Anthropic publishes them in the exam guide.**

That boundary is not a limitation on this course. It is the reason you can trust it. A prep
course that cannot say where its content came from is a course that might be built from somebody
else's leaked exam, and that is worth less than nothing to you — a braindump teaches you the
form of last quarter's questions instead of the judgment the exam is actually measuring.

## The part most prep leaves out: the anti-patterns

The exam guide names wrong answers explicitly. Under Domain 1, for example, it lists avoiding
"parsing natural language signals to determine loop termination" and "setting arbitrary
iteration caps as the primary stopping mechanism."

Read that as the gift it is. Well-built multiple-choice distractors are not random — they are
the plausible mistakes a competent person actually makes. So a published list of anti-patterns
is a published list of the shapes the wrong answers take. Every episode here teaches the
anti-patterns alongside the pattern, and names which domain they sit in.

## The lab: status

The scaffold and the first tool exist and run. **41 tests, 0 skips.** Lesson status is in the course outline above.

```
course/               per-episode script and slides, as plain markdown
src/course_doctor/    the tool: library, output models, MCP server
tests/                bounds, adapter, and a real stdio protocol test
.claude/rules/        path-specific rules, loaded only on matching files
.claude/skills/       check-sources, which runs forked
.mcp.json             how the server gets wired in
SOURCES.md            every lesson claim traced to a published source
```

Each episode's directory holds the script and the deck, so you can read the course without
watching it.

## Running it

Python 3.12 or newer. The system `python3` on a Mac is older, so nothing runs against it.

```
uv venv --python 3.12
uv pip install -e '.[test]'
./scripts/run-tests.sh
```

Then point Claude Code at the server:

```
claude --mcp-config .mcp.json
```

**Use `./scripts/run-tests.sh` rather than bare `pytest`.** Several tests here prove an
*absence* — that a path escape is refused, that nothing is read on a refusal, that no URL is
fetched. An absence test that never runs looks exactly like one that passed, so the script pins
the collected count and fails on any skip. It is the only thing that does.

## Not affiliated with Anthropic

This is independent material. I am not speaking for Anthropic, and nothing here is an official
preparation resource. The authoritative source for what is on the exam is always the exam guide
on the Anthropic Partner Academy certification page, which supersedes anything written here.
Exam details change; this README records what the guide said at the version noted in
[SOURCES.md](SOURCES.md).
