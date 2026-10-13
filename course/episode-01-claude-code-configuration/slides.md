# Episode 1 slides — Configuration is the exam's quietest 20%

One `## Slide N` per slide, plain text body lines, speaker notes as a blockquote underneath.

**Slide body text is deliberately plain — no asterisks, no hashes, no pipes.** Those arrive as
literal punctuation when pasted into Keynote or Google Slides and then have to be stripped by
hand. Copy a slide's body lines straight across.

13 slides for a 9–11 minute episode. Slides 4 through 11 are the build; the screen recording
carries those, so the slide is a title card the viewer can pause on, not a wall of text.

---

## Slide 1

Build to Pass
Claude Certified Architect – Foundations

Episode 1 of 5
Claude Code Configuration and Workflows

**Speaker notes:**

> Cold open is on the blueprint slide, not here. Hold this one for about two seconds.
> Do not say "welcome back" — a viewer landing from search has not been here before.

---

## Slide 2

Domain 3 — Claude Code Configuration and Workflows

20% of the exam

Domain 1  Agentic Architecture and Orchestration     27%
Domain 3  Claude Code Configuration and Workflows     20%
Domain 4  Prompt Engineering and Structured Output    20%
Domain 2  Tool Design and MCP Integration             18%
Domain 5  Context Management and Reliability          15%

**Speaker notes:**

> Weights are from exam guide section 4. Highlight Domain 3's row only.
> Order the rows by weight here, descending — it shows the viewer where the mass is.
> This is the one slide that recurs in all five episodes, with a different row highlighted.
> Keeping it identical across episodes is the point: by episode 5 the viewer has the blueprint
> memorised without having been asked to memorise it.

---

## Slide 3

Six task statements in this domain

CLAUDE.md hierarchy and scoping
Custom slash commands and skills
Path-specific rules for conditional loading
Plan mode versus direct execution
Iterative refinement for progressive work
Claude Code in CI/CD pipelines

**Speaker notes:**

> Exam guide section 6, task statements 3.1 through 3.6, titles paraphrased to fit.
> Say out loud that we build the first four today. Iterative refinement shows up naturally
> in episodes 3 and 4, and CI/CD is its own thing — flag honestly that this episode does not
> cover it rather than letting the viewer assume the domain is closed.

---

## Slide 4

CLAUDE.md

Standing instructions that load automatically

User level     applies to everything you do
Project level  applies to this repository, committed
Subdirectory   applies to one area

**Speaker notes:**

> Screen recording starts here. This slide is the title card.
> Define it in the sentence: standing instructions that load automatically, so you stop
> re-explaining the project every session.
> Verify the resolution order live against the installed version before filming — it is on
> the SOURCES.md checklist and must not be asserted from memory.

---

## Slide 5

The question is not how important the rule is

It is who the rule applies to

Team convention    project level, committed
Personal taste     user level

Get it backwards and nothing errors
It applies to the wrong people, quietly

**Speaker notes:**

> This is the load-bearing slide of the first third. If the episode runs long, cut slide 3
> before this one.
> The failure being described is silent, and that is why it is examinable: there is no error
> message that tells you a convention landed on one laptop instead of the team.

---

## Slide 6

Path-specific rules

A header at the top of the rule says which files it applies to

paths: src/api/**/*        API conventions
paths: **/*.test.*         testing conventions

The rule loads only when a matching file is in play

**Speaker notes:**

> Glob examples are taken from exam guide section 8, exercise 2 — use theirs, not invented
> ones, so the viewer recognises them if they read the guide.
> Show the frontmatter zoomed on screen. Verify the exact schema live.

---

## Slide 7

This is a context mechanism wearing a configuration hat

Instructions cost context

Load every convention on every task, and you spend
context on API rules while editing a test file

Context you spent is context unavailable for the work

Test the non-matching case too
Or you have only confirmed that something loaded

**Speaker notes:**

> Two ideas on one slide because they are the same idea. If it feels crowded, split after
> "unavailable for the work."
> The last two lines are the verification point and they generalise well past this exam —
> testing only the positive case is how you confirm a rule exists without confirming it is
> conditional.

---

## Slide 8

Skills

A packaged procedure you invoke by name

Two frontmatter options, both about containment

allowed-tools    restricts what the skill may use
context: fork    runs it in isolation

**Speaker notes:**

> Both options are named in exam guide section 8, exercise 2 — that is why they are on the
> slide rather than the full frontmatter list.
> The example that lands: a skill reading thirty files to answer one question leaves thirty
> files in your context unless it is forked. Fork when the work is bulky and only the
> conclusion matters; don't when you need the detail downstream.

---

## Slide 9

Wiring in a tool server

MCP — the Model Context Protocol
The standard way you hand Claude your own tools

Credentials go in as environment variable references
The config names the variable, the environment supplies the secret

Project config   shared with the team, committed
Personal config  yours alone

Both active at once

**Speaker notes:**

> Define MCP in the sentence, every episode, even though episode 2 is entirely about it.
> A viewer arriving from search on episode 4 has not heard the definition.
> The reason for env var references is that the file is committed. Say the consequence:
> paste a real key and you have published it to everyone who clones the repo.
> We only configure the server here. We write it in episode 2.

---

## Slide 10

Plan mode

Work out the approach and show it, before making changes

Single-file bug fix, one obvious change
Library migration across many files
New feature with several defensible designs

**Speaker notes:**

> The three task sizes are from exam guide section 8, exercise 2, which asks you to test plan
> mode against exactly these.
> Do not give the answer on this slide. Let the viewer predict, then turn it over on slide 11.

---

## Slide 11

The test is not task size

It is the cost of a wrong direction found late

Bug fix              planning buys a delay
Migration            a wrong approach applied to 40 files is 40 undos
Several good designs plan — this is the strongest case

When more than one answer is reasonable,
seeing which one is being chosen is the whole value

**Speaker notes:**

> This is the single most examinable judgment in Domain 3, because the wrong heuristic — plan
> big things, don't plan small ones — is defensible enough to be a good distractor.
> Land the reframe clearly: cost of being wrong, not size.

---

## Slide 12

The anti-patterns, published in the exam guide

A team convention living in a personal config
Every rule loading on every task
A secret written literally into a committed file
Reaching for plan mode by task size

Well-built distractors are the plausible mistakes
a competent person actually makes

So a published anti-pattern list is a published
list of the wrong answers' shapes

**Speaker notes:**

> This slide is the course's differentiator and it recurs in all five episodes. Do not rush it.
> The first and third anti-patterns here are mine, drawn from the guide's knowledge and skills
> bullets rather than quoted from a named anti-pattern list — the guide states its explicit
> anti-patterns under Domain 1. Say "the ones to recognise in this domain," not "the guide
> lists these four," because that would overstate the source. Accuracy here is the whole point
> of the slide.

---

## Slide 13

Next: the MCP server

Four tools, descriptions built to be told apart
Errors structured so the agent knows what to retry

Sourced from the published exam guide
and public documentation only

Every claim traced in SOURCES.md
Nothing from sitting the exam

github.com/julie-elkins/claude-architect-lab

**Speaker notes:**

> The sourcing statement goes on screen in every episode, not just episode 1. A viewer who
> arrives at episode 3 from search needs to know where the material came from, and scrolling
> back is not a thing they will do.
> Check the handle in the URL before export. The bare old handle 404s.
