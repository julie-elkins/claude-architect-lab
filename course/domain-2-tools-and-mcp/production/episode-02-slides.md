> **Production asset, not the lesson.** Slide bodies for the video version.
> The written lessons are listed on [the course front page](../../../README.md).

# Episode 2 slides — The description is the routing logic

One `## Slide N` per slide, plain text body lines, speaker notes as a blockquote underneath.

**Slide body text is deliberately plain — no asterisks, no hashes, no pipes.** Those arrive as
literal punctuation when pasted into Keynote or Google Slides and then have to be stripped by
hand. Copy a slide's body lines straight across.

15 slides for a 9–10 minute episode. Slides 4 through 13 are the build; the screen recording
carries those, so the slide is a title card the viewer can pause on, not a wall of text.

---

## Slide 1

Build to Pass
Claude Certified Architect – Foundations

Episode 2 of 5
Tool Design and MCP Integration

**Speaker notes:**

> Cold open is on the first line of the script, not here. Hold this one for about two seconds.
> Do not say "welcome back" — a viewer landing from search has not seen episode 1.

---

## Slide 2

Domain 2 — Tool Design and MCP Integration

18% of the exam

Domain 1  Agentic Architecture and Orchestration     27%
Domain 3  Claude Code Configuration and Workflows     20%
Domain 4  Prompt Engineering and Structured Output    20%
Domain 2  Tool Design and MCP Integration             18%
Domain 5  Context Management and Reliability          15%

**Speaker notes:**

> Weights are from exam guide section 4. Highlight Domain 2's row only.
> IDENTICAL to episode 1's slide 2 except which row is lit. That is the point — by episode 5
> the viewer has the blueprint memorised without having been asked to memorise it.
> Do not re-order the rows per episode. Descending by weight, every time.

---

## Slide 3

Five task statements in this domain

Tool interface design and descriptions
Structured error responses
Tool distribution and tool choice
MCP server integration
Built-in tool selection

All five in this episode

**Speaker notes:**

> Exam guide section 6, task statements 2.1 through 2.5, titles paraphrased to fit.
> Say "all five" out loud. Episode 1 covered four of six and flagged the gap; this one is
> complete, and the reason is runtime proportional to blueprint weight. Do not explain the
> runtime policy on camera — it is in STUDY-PATH.md for anyone who cares.

---

## Slide 4

The sentence the whole domain rests on

Tool descriptions are the primary mechanism
a model uses to select a tool

Not the code
Not the name
The description

**Speaker notes:**

> Exam guide section 6, task statement 2.1, first knowledge item. Quote it as the guide's,
> not as an opinion — this is the load-bearing citation of the episode.
> Screen recording starts after this slide.

---

## Slide 5

Two tools the model cannot tell apart

analyze_content
analyze_document

Near-identical descriptions
Neither one is wrong
Nothing distinguishes them

Misrouting is intermittent, which is worse

**Speaker notes:**

> This example is the guide's own, section 6 under 2.1 — say so. Using theirs means a viewer
> who reads the guide recognises it.
> Land the intermittent point: consistent failure gets debugged, intermittent failure gets
> blamed on the model.

---

## Slide 6

The highest-value sentence in a tool description

Say what the tool does NOT do

Reads a local material file.
Does not fetch URLs and does not follow links.

You are not documenting for a human
You are writing a routing table

**Speaker notes:**

> The boundary clause is what makes the NEXT tool distinguishable — that is the mechanism,
> and it is worth saying slowly.
> Also mention the guide's system-prompt trap here if time allows: wording elsewhere can
> create unintended tool associations and override a careful description. If the episode runs
> long, this is the first thing to cut.

---

## Slide 7

An agent has three reasonable moves

Retry
Ask a human
Move on

It picks between them using what your error said

A generic failure message deletes
the information it needed

**Speaker notes:**

> The guide's wording is that uniform error responses PREVENT appropriate recovery decisions.
> Frame it as deletion of information rather than as untidiness — that is what makes it
> examinable rather than stylistic.

---

## Slide 8

Four categories, named in the exam guide

Transient    try again
Validation   fix the input
Business     the rule says no, retrying is pointless
Permission   a human has to act

**Speaker notes:**

> Exam guide section 6, task statement 2.2. Four, named. Worth memorising in this order.
> The business category is the one people get wrong: it is a permanent no, and marking it
> retryable is how a loop burns budget on something that will never succeed.

---

## Slide 9

The distinction the guide names as a tested skill

An access failure
A valid empty result

A search that timed out
A search that matched nothing

Both are "no data"
They call for opposite responses

Different types, not one type with a flag

**Speaker notes:**

> This is the single most examinable item in the domain and the guide flags it explicitly as
> a skill. Do not rush it.
> The last line is the engineering point: a flag gets dropped by one careless caller and the
> two collapse back together.

---

## Slide 10

Return a refusal as a result
Do not raise it

An agent formats whatever it is handed

Raised as a transport error, it becomes
"the tool failed" — and your guidance is gone

**Speaker notes:**

> This is the lab's own design rule and it is in the repo's CLAUDE.md. Say that it cost real
> time to learn, because it did.
> Same information, thrown away by the delivery mechanism. That phrasing lands.

---

## Slide 11

The guide gives a number

18 tools instead of 4 or 5
degrades selection reliability

Not because any tool is bad
Because the decision got harder

**Speaker notes:**

> Exam guide section 6, task statement 2.3. The most quotable figure in the domain.
> ATTRIBUTE IT OUT LOUD. You cannot demonstrate selection reliability falling in nine
> minutes, so do not imply this was measured here.
> Tie forward: every configured MCP server's tools are live at once, so adding servers moves
> you toward the eighteen by the back door.

---

## Slide 12

tool_choice

auto     the model decides
any      it must call some tool
forced   you name the tool

An instruction has a failure rate
A setting does not

**Speaker notes:**

> Expect an item where the right answer is forcing a tool and the tempting one is firmer
> wording. Say that prediction out loud — it is the kind of thing viewers remember.
> The last two lines are the course's spine and recur in every episode.

---

## Slide 13

A populated server list does not prove the server works

An unset variable with no default still loads the server
You get a warning and the literal variable text

A tool list can come from a cache
rather than from a connection

A cached list and a live connection render identically

So call something

**Speaker notes:**

> Both behaviours are documented — MCP docs, re-verified 2026-10-18, cited in lesson 2.4.
> This is the slide to hold longest in the episode. "The absence of an error is not evidence
> that nothing is wrong" is the spine of the whole course, and this is its cleanest instance.
> Show /mcp populated on screen, then show the call failing.

---

## Slide 14

The anti-patterns, from the exam guide

Overlapping descriptions that misroute
Returning empty results as success
Terminating a workflow on one failure
Eighteen tools where four would do
Tools outside an agent's specialisation
A secret written into a committed file
A custom server for a standard integration

Two of those are opposites
So the answer is neither extreme

**Speaker notes:**

> This slide is the course's differentiator and it recurs in all five episodes. Do not rush it.
> The guide names these under Domain 2's objectives — unlike episode 1, where two of the four
> were mine. Here you can say "the guide names these." Accuracy about the source is the whole
> point of the slide.
> Close on the opposites: recover what you can, propagate what you cannot with enough context
> to decide, and never let a failure render as a clean result.

---

## Slide 15

Next: Domain 1, the biggest one

27% of the exam
The loop, coordinators, and subagents
Including two ways a granted tool disappears anyway

Sourced from the published exam guide
and public documentation only

Every claim traced in SOURCES.md
Verification state in VERIFICATION.md
Nothing from sitting the exam

github.com/julie-elkins/claude-architect-lab

**Speaker notes:**

> The sourcing statement goes on screen in every episode, not just episode 1. A viewer who
> arrives here from search needs to know where the material came from, and scrolling back is
> not a thing they will do.
> VERIFICATION.md is new and worth naming — it says what has NOT been checked, which is the
> differentiator for a course about content freshness.
> Check the handle in the URL before export. The bare old handle 404s.
