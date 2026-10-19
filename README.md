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

## Certification program update: December 7, 2026

Anthropic has announced that **the Associate – Foundations, Developer – Foundations, and
Architect – Professional exams will include updated content from December 7, 2026**, with
updated exam guides available **November 17, 2026**. If you are testing on or after
December 7 for one of those three, prepare from the updated guide.

**Architect – Foundations — the exam this course prepares for — is not named in that
announcement.** Three of the four certifications are listed and CCAR-F is not one of them.

Two consequences, stated plainly:

- **This course is built against the guide that remains current for its exam.** Version 1.0,
  effective July 2026, is what every claim here cites, and the announcement does not
  supersede it for CCAR-F.
- **Any study material covering all four certifications will be stale for three of them on
  December 7.** That is worth knowing if you are using more than one source.

When the updated guides publish on November 17, this course will be re-checked against
them regardless — if CCAR-F's guide moves at all, the version string in
[SOURCES.md](SOURCES.md) changes and every claim traced to a section gets re-read. The
guide's own §18 records its version history, and this repository records which version it
was written against.

**Verify this yourself before relying on it.** The announcement above is quoted from the
Anthropic Partner Academy certification pages; the authoritative source is those pages, not
this README, and an announcement can be revised.

## The exam, from the published exam guide

| Item | Detail |
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

**Five ways in, depending on what you want.**

- **[STUDY-PATH.md](STUDY-PATH.md)** — start here if you have a date booked. Plans for a
  week, a weekend and an evening, and the one thing to decide before you book.
- **[GUIDE.md](GUIDE.md)** — the whole course as one scrollable document. Generated from
  the lessons below, with a test that fails if it goes stale, so it cannot quietly
  disagree with them.
- **[SCENARIOS.md](SCENARIOS.md)** — the six published scenarios and which lessons each
  needs. This is how the exam presents the material; the table below is how the blueprint
  organises it.
- **[THEMES.md](THEMES.md)** — four ideas that recur across domains. Read it last; it is
  the most useful thing to hold on exam day and it means little before you have seen the
  instances.
- **[RECALL.md](RECALL.md)** — the conventions you cannot reason your way to: which file
  lives where, which flag does what, which enum value means what, and **nine places where
  the default is the opposite of the guess.** Every row restates a lesson and links to it;
  no row is a new claim. Use it to find your gaps early, and again the night before.

Four more pages, all straight from the parts of the guide nobody reads:

- **[SCOPE.md](SCOPE.md)** — the appendix. What may appear, what is explicitly tested, and
  **sixteen topics the guide says will not appear at all.** The out-of-scope list is the
  cheapest thing in this repository: it tells you what to stop studying.
- **[EXAM-DAY.md](EXAM-DAY.md)** — registration, Pearson VUE, ID rules, retake waiting
  periods, how the 720 was set, and the renewal that is free **only if you are on time.**
- **[GLOSSARY.md](GLOSSARY.md)** — the words that mean different things in different
  lessons. "Fork" means three.
- **[FUNDAMENTALS.md](FUNDAMENTALS.md)** — what this exam sits on top of, and a readiness
  check. Start here if you are not sure the course is pitched at you. It also explains why
  the familiar ladder — data engineering, then ML, then AI — **is not this exam's**:
  fine-tuning, embeddings, RLHF and model internals are all explicitly out of scope, so the
  stack underneath CCAR-F is software engineering and DevOps, then distributed systems, then
  model behaviour in production.

**Status: 29 of 29 written. All five domains complete.** A lesson is a link only when it exists. Nothing below is a
stub — fifteen empty files read as abandoned work, where a listed objective reads as a
plan and stops one being quietly dropped.

### Domain 3 — Claude Code Configuration & Workflows · 20%

| TS | Task statement | Lesson |
|---|---|---|
| 3.1 | Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization | [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) |
| 3.2 | Create and configure custom slash commands and skills | [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) |
| 3.3 | Apply path-specific rules for conditional convention loading | [lesson 3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) |
| 3.4 | Determine when to use plan mode vs direct execution | [lesson 3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) |
| 3.5 | Apply iterative refinement techniques for progressive improvement | [lesson 3.5](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| 3.6 | Integrate Claude Code into CI/CD pipelines | [lesson 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |

### Domain 2 — Tool Design & MCP Integration · 18%

| TS | Task statement | Lesson |
|---|---|---|
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries | [lesson 2.1](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) |
| 2.2 | Implement structured error responses for MCP tools | [lesson 2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) |
| 2.3 | Distribute tools appropriately across agents and configure tool choice | [lesson 2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) |
| 2.4 | Integrate MCP servers into Claude Code and agent workflows | [lesson 2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) |
| 2.5 | Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively | [lesson 2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md) |

### Domain 1 — Agentic Architecture & Orchestration · 27%

| TS | Task statement | Lesson |
|---|---|---|
| 1.1 | Design and implement agentic loops for autonomous task execution | [lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) |
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns | [lesson 1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) |
| 1.3 | Configure subagent invocation, context passing, and spawning | [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |
| 1.4 | Implement multi-step workflows with enforcement and handoff patterns | [lesson 1.4](course/domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md) |
| 1.5 | Apply Agent SDK hooks for tool call interception and data normalization | [lesson 1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |
| 1.6 | Design task decomposition strategies for complex workflows | [lesson 1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md) |
| 1.7 | Manage session state, resumption, and forking | [lesson 1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) |

### Domain 4 — Prompt Engineering & Structured Output · 20%

| TS | Task statement | Lesson |
|---|---|---|
| 4.1 | Design prompts with explicit criteria to improve precision and reduce false positives | [lesson 4.1](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md) |
| 4.2 | Apply few-shot prompting to improve output consistency and quality | [lesson 4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) |
| 4.3 | Enforce structured output using tool use and JSON schemas | [lesson 4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) |
| 4.4 | Implement validation, retry, and feedback loops for extraction quality | [lesson 4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) |
| 4.5 | Design efficient batch processing strategies | [lesson 4.5](course/domain-4-prompting-and-output/lesson-4-5-batch-processing.md) |
| 4.6 | Design multi-instance and multi-pass review architectures | [lesson 4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md) |

### Domain 5 — Context Management & Reliability · 15%

| TS | Task statement | Lesson |
|---|---|---|
| 5.1 | Manage conversation context to preserve critical information across long interactions | [lesson 5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) |
| 5.2 | Design effective escalation and ambiguity resolution patterns | [lesson 5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md) |
| 5.3 | Implement error propagation strategies across multi-agent systems | [lesson 5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) |
| 5.4 | Manage context effectively in large codebase exploration | [lesson 5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) |
| 5.5 | Design human review workflows and confidence calibration | [lesson 5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) |

**All twenty-nine lessons are written.** The written lessons *are* the course — read them,
or read [GUIDE.md](GUIDE.md) for the whole thing in one scroll.

**All five video episodes are also scripted**, one per domain, as **production assets** under
`course/domain-*/production/`. Each is a narration script plus a slide deck. **They are not
the course and they are allowed to lag it**, so every one opens with a header saying the
lessons are authoritative. Nothing has been filmed.

| Episode | Domain | Weight | Task statements | Target runtime |
|---|---|---|---|---|
| [1](course/domain-3-configuration/production/) | 3 — Configuration & Workflows | 20% | 3.1–3.4 | 9–11 min |
| [2](course/domain-2-tools-and-mcp/production/) | 2 — Tool Design & MCP | 18% | 2.1–2.5 | 9–10 min |
| [3](course/domain-1-agentic-architecture/production/) | 1 — Agentic Architecture | **27%** | 1.1–1.7 | 13–14 min |
| [4](course/domain-4-prompting-and-output/production/) | 4 — Prompting & Output | 20% | 4.1–4.6 | 10–11 min |
| [5](course/domain-5-context-and-reliability/production/) | 5 — Context & Reliability | 15% | 5.1–5.5 | 7–8 min |

**Runtime is proportional to blueprint weight**, which is why episode 3 is nearly twice
episode 5. That choice is what lets every episode after the first cover *all* of its domain's
task statements rather than leaving some on the floor. **Episode 1 is the exception** — it
covers four of Domain 3's six and says so on camera; TS 3.5 and 3.6 are written up in
[their lesson](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md).

`scripts/check_production.py` checks the decks for the defects that actually happened — a
stated slide count that disagrees with the slides (which occurred three times while writing
these), non-sequential numbering, broken links, and a missing authoritative header. **It
cannot check whether a script still agrees with its lesson**, because a script restates a
lesson in spoken prose and no diff can tell a rewording from a stale claim. Episode 1 taught
a corrected-away claim for five days before anyone noticed.

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

## How claims here are checked

Every claim in every lesson names its source — an exam-guide section, or a documentation
URL **with the date it was read**, because a live link is not a verified claim: pages get
rewritten under the same URL.

`scripts/check_citations.py` enforces that mechanically and runs in the test suite. It
was verified by breaking it three ways — a row citing nothing, a URL with no read date,
and a lesson with no Sources section — and it caught all three. As of **2026-10-18**:
**329 claim rows, 205 cited to the exam guide, 124 to documentation across 13 distinct
pages, 0 outstanding.** `--urls` resolves every cited link.

**Run the script rather than trusting those figures.** An earlier version of this
paragraph read "72 claim rows … 6 outstanding … all five currently return 200" long after
the real numbers were 329 and 0 across 13 pages. A hand-maintained count in a README is a
second copy of a measurement, and it goes stale pointing the wrong way — downward, which
reads as modesty rather than as an error.

**What a passing structural check does not establish: whether a cited page still says what
the row claims.** Only reading both does. That stronger check has now been run on **5 of
the 13 cited pages**, by re-fetching each and requiring the claim's *verbatim* wording
back; it found **zero contradictions and six omissions**, all since written into the
lessons. The other 8 pages were read when the lessons were written and have not been
checked since.

**[VERIFICATION.md](VERIFICATION.md) is the record** — which pages, on what date, what was
found, and what the process still cannot tell you. `check_citations.py` reads that file and
reports coverage as a fraction, so a page nobody adds to it is counted as unverified. A
passing structural check is not a verified lesson, and treating one as the other would be
the failure this course spends its time on.

## Going deeper, in my own public work

Several lessons touch a problem I have built and published something about. These are not
required reading and they are not polished teaching material — they are the working
artifacts, with their measurements and their negative results intact.

| Lesson | Repository | What it adds |
|---|---|---|
| [1.5 hooks](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) · [3.1 context vs control](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) | [fail-closed](https://github.com/julie-elkins/fail-closed) | Written standards for agent tooling and a staging guard that ships registered rather than as a template, because a guard whose script is missing never warns and never fires |
| [2.1 tool interfaces](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) · [2.2 structured errors](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) | [mcp-server-design-guide](https://github.com/julie-elkins/mcp-server-design-guide) | A 15-point standard for MCP servers, and the four failures you only find by audit |
| [5.3 error propagation](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) | [k8s-triage-agent](https://github.com/julie-elkins/k8s-triage-agent) | A read-only triage agent whose stated design goal is reporting what it could **not** check |
| [5.4 exploration](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) · [4.1 criteria](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md) | [course-corpus](https://github.com/julie-elkins/course-corpus) | Indexing content you have already written, where a missing verification date reports UNKNOWN and never CURRENT |
| [5.5 calibration](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) | [abstention-eval](https://github.com/julie-elkins/abstention-eval) · [nl2sql-eval](https://github.com/julie-elkins/nl2sql-eval) · [llm-eval-validity](https://github.com/julie-elkins/llm-eval-validity) | Measuring what a model declines to answer, and validating an evaluation harness the way a certification exam is validated |
| The lab's premise | [driftwood](https://github.com/julie-elkins/driftwood) | Detecting documentation that has silently stopped being true — **including the published negative result** where it lost to a baseline that flags nothing, which is why Course Doctor's detection is deterministic |

That last row is the one worth clicking. The reason this course's lab is designed the way
it is, is a measurement that went against the interesting approach.

## Accessibility

This is a written course, so **the markdown structure is the accessibility layer.** A
blind learner using a screen reader navigates by heading, skips, re-reads, changes speed
and searches — none of which an audio recording allows. So the work here is structural.

`scripts/check_accessibility.py` runs in the test suite and fails on three things that
make content unusable rather than merely awkward: **ambiguous link text**, because screen
readers offer a "list all links" mode where several links labelled `read` are
indistinguishable; **blank table column headers**, because the header is announced with
every cell and reads as "blank"; and **images with no alt text**. It also reports skipped
heading levels and untagged code fences.

Every rule exists because this repository had the defect. Measured before the fix:
**eleven links labelled `read`, and three tables with a blank first column header.** The
check was then verified by reintroducing all three.

**What that does not establish:** whether the prose reads sensibly aloud, whether alt text
is any good, or whether meaning is carried by emphasis alone. Those need a person, ideally
one who uses a screen reader. No mechanical defects is not an accessible course.

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

The scaffold and the first tool exist and run. **61 tests, 0 skips** — the floor is pinned in
`scripts/run-tests.sh` and this sentence is checked against it, because a hand-maintained
count in a README goes stale *downward* and then reads as modesty instead of as an error.
Lesson status is in the course outline above.

```
course/domain-*/      the 29 written lessons — these are the course
course/*/production/  narration scripts and slide decks for the video, which lags
src/course_doctor/    the tool: library, output models, MCP server
tests/                bounds, adapter, and a real stdio protocol test
.claude/rules/        path-specific rules, loaded only on matching files
.claude/skills/       check-sources, which runs forked
.mcp.json             how the server gets wired in
SOURCES.md            every lesson claim traced to a published source
```

**The lessons are the course and the scripts are downstream of them.** You never need the
production assets to study; they exist so the video can be recorded without rewriting the
material, and each says so in its own header.

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
