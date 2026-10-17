# How to use this course

Twenty-nine lessons, one per task statement. Four plans below depending on how much time
you have, and one thing to decide before you book anything.

## Decide this first: when to sit it

**The credential is valid for 12 months from the date it is awarded.** That is shorter
than most cloud certifications and it should shape *when* you sit, not just whether you
pass. Sitting it the week before a job search starts is worth more than sitting it eight
months earlier and renewing in the middle.

Exam mechanics, from the guide: **60 items, 4 scenarios drawn from a published bank of 6,
120 minutes, passing score 720 on a 100–1,000 scale, $125.** The score report gives
percent-correct **by domain** — useful diagnostics, and those section percentages do
**not** determine pass or fail. Only the total scaled score does.

---

## If you have a week

Dependency order, which is also the order the course is written in. Tools before the loop
that calls them; the loop before the output it shapes.

**Day 1 — Domain 3, configuration (20%).** Six lessons.
[3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) ·
[3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) ·
[3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) ·
[3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) ·
[3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md)

Start here because it is the most concrete and because two of its lessons set up a
distinction the rest of the exam keeps using.

**Day 2 — Domain 2, tools and MCP (18%).** Five lessons.
[2.1](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) ·
[2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) ·
[2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) ·
[2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) ·
[2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md)

**Days 3 and 4 — Domain 1, agentic architecture (27%).** Seven lessons, the largest slice.
[1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) ·
[1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) ·
[1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) ·
[1.4](course/domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md) ·
[1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) ·
[1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md) ·
[1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md)

Two days, not one. It is 27% of the items and the lessons are denser.

**Day 5 — Domain 4, prompting and output (20%).** Six lessons.
[4.1](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md) ·
[4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) ·
[4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) ·
[4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) ·
[4.5](course/domain-4-prompting-and-output/lesson-4-5-batch-processing.md) ·
[4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md)

**Day 6 — Domain 5, context and reliability (15%).** Five lessons.
[5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) ·
[5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md) ·
[5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) ·
[5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) ·
[5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md)

**Do not skip this one because it is 15%.** It appears in five of the six scenarios — see
[SCENARIOS.md](SCENARIOS.md). The weights say how many items come from a domain; the
scenarios say how often you will need it.

**Day 7 — the two synthesis pages, then the scenarios.** Read
[THEMES.md](THEMES.md) — four ideas that recur across domains, and the most useful thing to
hold on exam day. Then walk [SCENARIOS.md](SCENARIOS.md) and answer the closing question
under each of the six before reading anything again.

---

## If you have a weekend

**Saturday:** Domains 3 and 2 in full (11 lessons). Then [THEMES.md](THEMES.md).

**Sunday:** Domain 1 in full (7 lessons), then the anti-pattern section only of each
Domain 4 and 5 lesson. Finish on [SCENARIOS.md](SCENARIOS.md).

You will be thin on Domain 5, which is a real cost given how often it recurs. Know that
going in rather than discovering it.

---

## If you have an evening

Read, in this order:

1. [THEMES.md](THEMES.md) — the four recurring ideas
2. [SCENARIOS.md](SCENARIOS.md) — the six scenarios and their closing questions
3. The **anti-pattern** section of every lesson, nothing else

The anti-patterns are the published wrong answers, and well-built distractors are the
plausible mistakes a competent person actually makes. Three hours of anti-patterns is the
highest-yield three hours available.

This is triage, not preparation. It will not make up for not knowing the material.

---

## If you are coming back to it after a gap

[GLOSSARY.md](GLOSSARY.md) first. It exists because several words mean different things in
different lessons — "fork" means three things — and those are the distinctions that decay
first.

---

## What to do with the lab

The repository is a working system: [Course Doctor](README.md#the-lab-course-doctor), an
agent that checks training material against live documentation and reports what went stale,
what it could not check, and what needs a human.

Reading the course does not require running it. But if you learn by building, clone it, run
the tests, and read `src/course_doctor/` against lessons 2.1 and 2.2 — the error shapes and
the tool descriptions in there are the ones those lessons teach, and the comments say why
each decision was made rather than what the code does.

```
uv venv --python 3.12
uv pip install -e '.[test]'
./scripts/run-tests.sh
```

Several of its tests assert an **absence** — that a path escape is refused, that nothing is
read on a refusal. Use the script rather than bare `pytest`: it pins the collected count and
fails on any skip, because an absence test that never runs looks exactly like one that
passed.

---

## What this course cannot tell you

**Whether you are ready.** There is no practice exam here and there will not be. No
pass-rate, difficulty or score-distribution claim appears anywhere in this course, because
none is published and I have access to no such data for this exam. The guide's four
preparation exercises are the closest thing to practice material Anthropic publishes, and
**completing them is not a predictor of a score** and is not presented as one.

**What is on the exam.** The authoritative source is the exam guide on the Anthropic
Partner Academy certification page, which supersedes anything written here. Details change;
this course records what the guide said at the version noted in [SOURCES.md](SOURCES.md).

**That every claim here is current.** Every claim names its source and carries the date it
was read — but a page can return 200 and no longer say what it said. See the README's
section on how claims are checked, including the part that is **not** yet verified.
