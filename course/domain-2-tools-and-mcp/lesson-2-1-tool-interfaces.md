# Lesson 2.1 — The description is the routing logic

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.1:** Design effective tool interfaces with clear descriptions and
boundaries.

Lab artifact: Course Doctor's tool surface, with each tool's purpose written so the next
one cannot be confused with it.

## What you will be able to do afterwards

Diagnose a tool that never gets called, or gets called for the wrong request, and fix it
in the description rather than in the code.

## Why the exam cares

The guide's first knowledge item states it outright: **tool descriptions are the primary
mechanism a model uses for tool selection, and minimal descriptions lead to unreliable
selection among similar tools.**

So a tool nobody calls is almost never a code problem. It is a description problem, and
the guide's own worked example is two tools called `analyze_content` and
`analyze_document` with near-identical descriptions — which misroute not because either
is wrong but because nothing distinguishes them.

It also names a trap most people never consider: **system prompt wording can create
unintended tool associations.** A keyword-sensitive instruction elsewhere can override a
well-written description.

## Fundamentals

**Dispatch.** Choosing which of several implementations to run. *Why it matters here:*
with an LLM, dispatch happens in natural language against your descriptions, so the
description *is* the dispatch table. *Depth:* any treatment of dynamic dispatch; the
mechanism differs, the problem does not.

**Interface contract.** What a caller may rely on: inputs, outputs, failure modes. *Why
it matters here:* the description is the only place a model learns the contract, since it
cannot read your implementation. *Depth:* design-by-contract literature.

**Cohesion.** One unit doing one thing. *Why it matters here:* a generic tool covering
three jobs cannot be described precisely, which is why the guide's fix is to split it.
*Depth:* any treatment of single responsibility.

**Schema.** A machine-readable description of accepted input. *Why it matters here:* the
schema constrains shape; the description conveys *meaning*, and only one of those stops a
wrong-tool call. *Depth:* `json-schema.org`.

## The idea, before any code

**Write the description for a reader who cannot see the code**, because that is literally
the situation. Three things it must carry, and the guide names all three: what the tool is
for, what it expects, and **when to use it rather than the similar one next to it.**

That last clause is the one people omit, and it is the one that does the routing. "Reads a
file" describes a tool. "Reads a lesson file and lists the URLs it cites; use
`fetch_source` to retrieve those URLs" routes between two.

**Then look for overlap deliberately.** If two descriptions could plausibly answer the
same request, the model will sometimes pick either — and you will debug the
implementation of whichever one it chose.

**If you cannot describe a tool precisely, it is doing too much.** The guide's fix is
splitting a generic `analyze_document` into `extract_data_points`, `summarize_content`
and `verify_claim_against_source`. Three names you can tell apart, three contracts.

## The build

### Step 1 — name the boundary in the description

Course Doctor's first tool:

```python
"""Read a material file and list the documentation URLs it cites.

Returns the file's text, a content hash, and every URL found. Use this to find
out WHAT a lesson claims and WHERE it says the claim came from. It does NOT
fetch those URLs or check whether they still support the claim — call
fetch_source for that.
"""
```

The last sentence is the routing. It names a sibling and says when to prefer it, so a
request to "check whether this lesson is still accurate" does not stop here.

### Step 2 — describe every parameter by its failure

A parameter description that restates the type tells a caller nothing — and it passes any
check that only looks for non-empty text:

```
BAD:   path: "A string path to the file."
GOOD:  path: "Path to one material file, relative to the project root. An
        absolute path or one escaping the root is refused rather than read.
        Pass one file; this tool does not take a directory."
```

The second says what a *wrong* value does. That is the information a caller cannot get
anywhere else.

### Step 3 — hunt for overlap, then split or rename

List your tools with one-line purposes side by side. For any pair you could imagine the
same request matching, do one of two things — both named by the guide:

- **Rename and re-describe** to eliminate the overlap: `analyze_content` becomes
  `extract_web_results` with a web-specific description.
- **Split the generic one** into purpose-specific tools with defined input and output
  contracts.

### Step 4 — read the system prompt for interference

The guide names this as a skill: reviewing system prompts for keyword-sensitive
instructions that might override well-written tool descriptions. An instruction saying
"always search before answering" can pull a search tool into requests that needed
something else, and no amount of description-polishing on the other tool fixes it.

## Tips

Things the documentation does not tell you.

**A tool that is never called looks exactly like a tool that is broken.** Before
debugging the implementation, check whether the description would make *you* pick it for
the request you expected. Most of the time the answer is no.

**A parameter description that names the type passes a truthiness check and teaches
nothing.** If your test asserts descriptions are non-empty, it is asserting almost
nothing. Assert a length floor, and better, review that each one says what a wrong value
does.

**Describing what a tool does NOT do is the highest-value sentence you will write.** It
is the only thing that stops a near-neighbour being called, and it is almost always
missing.

**Two tools with 80% overlapping descriptions behave worse than one tool.** The
single tool is reliably chosen; the pair is chosen at random and you debug whichever one
you happened to open.

**Returning raw dictionaries publishes an empty output schema.** A caller then has to
*call* the tool to learn the shape of the reply, which is the one thing a schema exists to
prevent. Typed output models cost almost nothing and are the difference between a
documented surface and a guessable one.

## The anti-pattern

From the guide's objectives:

> **Ambiguous or overlapping tool descriptions causing misrouting**, with
> `analyze_content` against `analyze_document` as the named case.

And its companion:

> **Minimal descriptions**, which the guide ties directly to unreliable selection among
> similar tools.

The shape to recognise on exam day: when one option offers a clearer *description* and
another offers a change to the *implementation* or the *prompt*, the description is
usually the answer — because the guide states the description is the selection mechanism.

## What this lesson does not cover

- **Error responses** — lesson 2.2, and the guide treats it as its own task statement.
- **How many tools an agent should have** — lesson 2.3.
- **MCP configuration** — lesson 2.4.
- **The built-in tools** — lesson 2.5.
- **Writing the schema itself.** Domain 4 TS 4.3 treats JSON schemas properly.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.1.

| Claim | Source |
|---|---|
| Tool descriptions are the primary mechanism LLMs use for tool selection; minimal descriptions lead to unreliable selection among similar tools | EG §6, TS 2.1 |
| Descriptions should include input formats, example queries, edge cases and boundary explanations | EG §6, TS 2.1 |
| Ambiguous or overlapping descriptions cause misrouting, e.g. `analyze_content` vs `analyze_document` | EG §6, TS 2.1 |
| System prompt wording is keyword-sensitive and can create unintended tool associations | EG §6, TS 2.1 |
| Renaming and re-describing to eliminate functional overlap is a tested skill | EG §6, TS 2.1 |
| Splitting a generic tool into purpose-specific tools with defined input/output contracts, e.g. `extract_data_points`, `summarize_content`, `verify_claim_against_source` | EG §6, TS 2.1 |
| Reviewing system prompts for instructions that override tool descriptions is a tested skill | EG §6, TS 2.1 |
| Writing descriptions that differentiate purpose, expected inputs, outputs, and when to use one versus a similar alternative | EG §6, TS 2.1 |
