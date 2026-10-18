> **⚠ The written lessons are authoritative, not this script.** This was written
> 2026-10-18, after the documentation verification pass of the same date, so it does not
> lag the lessons today. It will. There is no automated check for script-versus-lesson
> drift — a diff cannot tell a legitimate rewording from a stale claim — so **re-read the
> lesson for each task statement below and reconcile before recording.**
>
> **This is a production asset, not the lesson.** It is the narration script for the video
> version: spoken wording, screen directions, and a recording checklist.
>
> **If you are here to learn, read the written lessons instead.**
> [The course front page](../../../README.md) lists all twenty-nine. This script covers
> task statements 2.1 through 2.5:
> [2.1](../lesson-2-1-tool-interfaces.md) ·
> [2.2](../lesson-2-2-structured-errors.md) ·
> [2.3](../lesson-2-3-tool-distribution.md) ·
> [2.4](../lesson-2-4-mcp-integration.md) ·
> [2.5](../lesson-2-5-built-in-tools.md)

# Episode 2 — The description is the routing logic

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
Target runtime 9–10 minutes · ~1,400 spoken words
Ships: Course Doctor's real tool surface, with an error taxonomy the agent can act on

**Runtime is proportional to blueprint weight across the series** — 18% here against
Domain 1's 27%. That is deliberate and it is why this episode covers all five of its task
statements rather than four. See `STUDY-PATH.md`.

---

## Before you record

- Clean recording profile, per the recording checklist kept outside this repo. This episode
  shows `/mcp` and a `.mcp.json` on screen, so the isolation flags matter here specifically.
- **Start from episode 1's commit**, not from empty. The viewer should recognise the repo.
- The `tool_choice` demonstration needs a real API call. If you would rather not show a key
  on camera at all, show the config and narrate the behaviour — and **say that is what you
  are doing.** Do not let a described result look like a demonstrated one.
- **One mechanic in this episode is deliberately not demonstrated live:** the 4–5 versus 18
  tool-count degradation. You cannot show selection reliability falling in nine minutes.
  Attribute it to the guide out loud and move on.

---

## Fundamentals

Not spoken on camera. This block is for the written lesson and the episode description —
somewhere for a learner new to the stack to go, and a one-line refresh for a senior
engineer. Skippable by design.

**MCP — the Model Context Protocol.** A standard for handing a model your own tools: a
client talks to a server, the server advertises what it can do, the client calls it. *Why
it matters here:* this whole domain is tool design, and MCP is the shape tools arrive in.
*Depth:* the specification at `modelcontextprotocol.io`.

**A tool schema.** The machine-readable description of a tool's name, parameters and
types. *Why it matters here:* the model reads the schema and the descriptions in it, and
nothing else, when deciding what to call. *Depth:* JSON Schema, and lesson 4.3.

**Routing.** Choosing which of several available handlers should receive a request. *Why
it matters here:* tool selection *is* routing, and the description is the routing table.
*Depth:* any HTTP framework's router teaches the same idea with the ambiguity removed.

**Idempotence.** Whether repeating an operation is safe. *Why it matters here:* it decides
whether an error is retryable, which is half of the error taxonomy. *Depth:* REST method
semantics.

**Least privilege.** Give each component only the access it needs. *Why it matters here:*
it is the argument for scoping tools per agent role rather than handing everything to
everyone. *Depth:* any security text; the principle transfers intact.

**Fail-open versus fail-closed.** Whether a broken control lets work through or stops it.
*Why it matters here:* an error rendered as an empty success is fail-open, and this domain
names it as an anti-pattern. *Depth:* lesson 1.5, where it is the whole subject.

---

## Script

```
A tool that never gets called looks exactly like a tool that is broken.

[screen: the blueprint table, Domain 2 highlighted]

Domain 2 is eighteen percent of this exam, and it is about designing the tools you
hand an agent. Five task statements. We are doing all five today.

Here is the sentence the whole domain rests on, and it is from the exam guide:
tool descriptions are the primary mechanism a model uses to select a tool.

Not the code. Not the name. The description.

[screen: the five task statements]

Which means a tool nobody calls is almost never a code problem. You can test the
function, see it work, and still never see the agent reach for it.

[screen: two tool descriptions side by side]

The guide's own example is two tools called analyze_content and analyze_document,
with near-identical descriptions. Neither one is wrong. Nothing distinguishes
them, so the model misroutes — and it misroutes intermittently, which is worse
than consistently, because it looks like bad luck.

So here is the highest-value sentence you will write in a tool description, and
almost nobody writes it: say what the tool does NOT do.

[screen: a description with a boundary clause]

"Reads a local material file. Does not fetch URLs and does not follow links."

That clause is what makes the next tool distinguishable. You are not documenting
for a human. You are writing a routing table.

And one trap the guide names that nobody considers: wording in your system prompt
can create unintended tool associations. A keyword somewhere else can override a
description you wrote carefully. If selection is going wrong, the prompt is the
second place to look.

[screen: a generic error response]

Second mechanism. Errors.

The guide's framing is sharp: uniform error responses prevent the agent from
making recovery decisions. A generic "operation failed" is not a small
infelicity. It deletes the information the agent needed.

Because the agent has three reasonable moves — retry, ask a human, move on — and
it picks between them using what your error said.

[screen: the four-way taxonomy]

The guide names four categories: transient, validation, business, permission.
Transient means try again. Validation means fix the input. Business means the
rule says no and retrying is pointless. Permission means a human has to act.

And then it names one distinction specifically as a tested skill, which tells you
it is examinable: an access failure versus a valid empty result.

[screen: timeout beside no-matches]

Both of those are "no data". A search that timed out and a search that
legitimately matched nothing. They call for opposite responses, and if you
collapse them, your agent retries something that already worked — or gives up on
something that would have succeeded.

Make them different types. Not the same type with a flag.

[screen: a refusal payload with guidance]

One more thing about errors, and this is the one that costs people an afternoon.

Return a refusal as a result. Do not raise it.

An agent formats whatever it is handed. If your refusal arrives as a transport
error, the agent reports "the tool failed" — and the guidance field where you
wrote the fix is gone. Same information, thrown away by the delivery mechanism.

[screen: an agent with eighteen tools]

Third mechanism, and the guide gives a number, which is rare enough to notice.

Giving one agent eighteen tools instead of four or five degrades its selection
reliability. Not because any tool is bad. Because the decision got harder.

That figure is the most quotable thing in this domain, and it has a consequence
we hit in a minute.

[screen: tool_choice settings]

The other half is tool_choice, and there are three settings. Auto, where the
model decides. Any, where it must call some tool. Or forced, naming one.

Expect an exam item where the right answer is forcing a tool and the tempting
answer is a firmer instruction. Asking the model to always call something, under
auto, is context. Any is a control.

That distinction is this whole course in one line: an instruction has a failure
rate, a setting does not.

[screen: .mcp.json]

Fourth mechanism. Wiring a server in.

Project-level .mcp.json is committed and shared with the team. User-level config
is yours alone. Both are live at once — which is how a personal server quietly
duplicates a team one, and then you debug the wrong entry.

The file is committed, so credentials go in as environment variable references.
The config names the variable; the environment supplies the secret. Paste a real
key here and you have published it to everyone who clones the repo.

[screen: /mcp showing a populated list]

Now the part I want you to remember from this episode.

A populated server list does not prove the server works.

Two documented reasons. An unset variable with no default does not stop the
server loading — you get a warning and the literal variable text, so it
registers, looks configured, and fails mid-task on the first call. And a tool
list can come from a cache rather than a connection.

A cached list and a live connection render identically.

So call something. The absence of an error is not evidence that nothing is wrong,
and that sentence is the spine of this entire course.

[screen: Grep, then Read]

Fifth mechanism, quickly, because it pays off in Domain 5.

The built-in tools: Grep for content, Glob for paths, Read and Write for whole
files, Edit for targeted changes.

But the guide names a strategy, not just a mapping. Start with Grep to find the
entry points, then Read to follow the imports and trace the flow. Do not read
every file upfront.

Reading twenty files to answer one question spends the context you needed for the
answer. That is a context-management answer wearing a tooling hat.

[screen: the anti-pattern slide]

The part most prep courses leave out.

The exam guide names anti-patterns explicitly, in writing. Take that seriously,
because well-written distractors are not random noise — they are the plausible
mistakes a competent person actually makes. That is what makes them work. So a
published anti-pattern list is a published list of the wrong answers' shapes,
handed to you before the exam.

For this domain: overlapping descriptions that misroute. Silently suppressing an
error and returning empty results as success. Terminating a whole workflow on one
failure. Eighteen tools where four would do. An agent holding tools outside its
specialisation. A secret written literally into a committed file. And writing a
custom server for a standard integration, when a community one exists.

Note that two of those are opposites — suppressing a failure, and dying on one.
So the answer is neither extreme. Recover what you can, propagate what you
cannot with enough context to decide, and never let a failure render as a clean
result.

[screen: the tool surface, tests passing]

That is the tool surface, and it runs.

Next episode is the biggest one: Domain 1, twenty-seven percent. The agentic
loop, coordinators, and subagents — including the two ways a tool you granted a
subagent disappears anyway.

Everything in this course is sourced from the published exam guide or the public
documentation, and every claim is traced in SOURCES.md. Content verification
state is in VERIFICATION.md, including what has not been checked. Nothing here
comes from sitting the exam.

Repo link is below.
```

---

## Tips

Not spoken on camera — these belong in the written lesson and the episode notes. Each is
something the documentation does not say plainly.

**A tool that is never called looks exactly like a tool that is broken.** You will test the
function, watch it pass, and conclude the tool works. It does. It is just never selected,
and nothing surfaces that as a distinct state.

**A parameter description that names the type passes a truthiness check and teaches
nothing.** "An integer" is not a description. What the *wrong* value does is the
description — and a test asserting descriptions are non-empty will happily accept the
useless one.

**Two tools with 80% overlapping descriptions behave worse than one tool.** Merging them is
usually the fix, and it is the fix people reach for last because deleting a tool feels like
losing a feature.

**A refusal raised as an exception loses your `guidance` field.** The agent reports a failed
tool, the remedy you wrote never reaches anyone, and the bug looks like a model problem.

**An empty list and a failed read must be different types, not the same type with a flag.**
A flag gets dropped by one careless caller and the two collapse back together. The type
system is the only thing that keeps them apart.

**Populate "what this does not show" on SUCCESS, not only on failure.** A clean report is
indistinguishable from a healthy one otherwise, which is the failure this whole lab exists
to demonstrate.

**`tool_choice: "auto"` plus "always call the tool" is not a guarantee, and it fails
intermittently.** Intermittent is the expensive kind: it works through testing and breaks
in front of someone.

**Forcing a tool constrains one turn, not a sequence.** People reach for forced choice to
enforce an order and get the first call only. Order is a coordinator's job.

**An organisation `ask` control cannot be allowed away.** Worth knowing before you spend an
hour on a settings file trying.

**`timeout` is per-server and overrides the global.** So one slow server does not need a
change that loosens every other one.

**If a permission rule or hook for `Grep` never fires, check your platform before your
syntax.** A rule naming a tool the session does not have is not an error — it is silently
inert.

**Reading a file to find out whether it is relevant is the expensive habit**, and it is
invisible because each individual read looks reasonable.

---

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, no `/mcp` entries beyond this
      lab's server, nothing in the window title or tab bar.
- [ ] **No API key visible in any frame**, including a scrollback that scrolls past.
- [ ] Every mechanic shown actually worked on camera. If one was cut, it does not get claimed.
- [ ] The 4–5 versus 18 figure is attributed to the exam guide on screen, not stated as
      measured here.
- [ ] If `tool_choice` was narrated rather than demonstrated, the narration says so.
- [ ] Clean clone at this episode's commit reproduces the tool surface and the tests.
- [ ] Description carries the repo link with the `julie-elkins` handle.
