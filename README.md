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

## The blueprint, and where each domain is taught

| Domain | Content domain | Exam weight | Episode |
|---|---|---|---|
| 3 | Claude Code Configuration & Workflows | 20% | [1 — Configuration](course/episode-01-claude-code-configuration/) |
| 2 | Tool Design & MCP Integration | 18% | 2 — The MCP server |
| 1 | Agentic Architecture & Orchestration | **27%** | 3 — The loop and subagents |
| 4 | Prompt Engineering & Structured Output | 20% | 4 — Structured output |
| 5 | Context Management & Reliability | 15% | 5 — Reliability and the honest report |

**The episodes run in dependency order, not weight order.** The tools have to exist before the
loop that calls them, and the loop before the output it shapes. Domain 1 is the largest slice of
the exam and gets the longest episode, but it cannot come first.

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

## Status: episode 1 of 5 is built

The scaffold and the first tool exist and run. **41 tests, 0 skips.**

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
