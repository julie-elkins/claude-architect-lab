> **⚠ This script LAGS the lessons, and the lessons are authoritative.** It was written
> 2026-10-13, before the documentation verification pass of 2026-10-17. Two claims in it
> were corrected on 2026-10-18 after the written lessons had already fixed them. Before
> recording, re-read the lesson for each task statement this covers and reconcile — there
> is no automated check for script-versus-lesson drift, which is why this warning is here
> rather than in a test.
>
> **This is a production asset, not the lesson.** It is the narration script for the
> video version of this material — spoken wording, screen directions, and a recording
> checklist. It is kept in the repository because the video is still planned.
>
> **If you are here to learn, read the written lessons instead:**
> [the course front page](../../README.md) lists all of them. This script covers task
> statements 3.1 through 3.4; the written lesson for **TS 3.1** is
> [here](../lesson-3-1-claude-md-hierarchy.md), and 3.2 through
> 3.4 are being written.

# Episode 1 — Configuration is the exam's quietest 20%

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
Target runtime 9–11 minutes · ~1,500 spoken words
Ships: the Course Doctor repo scaffold, working, from empty

---

## Before you record

- Clean recording profile, per the recording checklist kept outside this repo. This episode
  shows `/mcp` on screen, so the isolation flags matter here specifically.
- Start from an **empty directory**. The whole point is that the viewer watches it come from
  nothing.
- The six mechanics in this script are demonstrated live, not asserted. If one behaves
  differently in your installed version than the script expects, **say so on camera and keep the
  take.** A prep course that shows a surprise and explains it is worth more than one that cuts
  to a version where it worked.

---

## Fundamentals

Not spoken on camera. This block is for the written lesson and the episode
description — it gives a learner new to the stack somewhere to go, and a senior
engineer a one-line refresh of something they have not touched in years. Skippable
by design: nothing in the script below depends on having read it.

**Configuration hierarchy.** Settings resolve across levels — user, project, and
subdirectory — and where a rule lives decides who it applies to. *Why it matters
here:* this is the whole of mechanism one, and the exam's question is always "who
does it apply to," never "how important is it." *Depth:* any tool with both a home
dotfile and a committed config — `git`, `ssh`, `editorconfig` — teaches the same
resolution idea.

**Glob patterns.** The `*`, `**` and `?` wildcards that match file paths. `src/**/*.py`
means every Python file at any depth under `src`. *Why it matters here:* a
path-specific rule's frontmatter is a glob, and there are **two** failure modes in
opposite directions — a glob that matches nothing gives a rule that never loads and
never complains, while **invalid YAML in the frontmatter makes the rule load on every
file**, because Claude Code ignores unparseable frontmatter and loads the rule as if it
had no `paths`. *Depth:* `man 7 glob`, and lesson 3.3.

**The context window as a budget.** Everything loaded — instructions, files, history
— occupies a finite space, and what you spend is not available for the work.
*Why it matters here:* it is the entire reason path-specific rules exist. Loading API
conventions while editing a test file is not untidy, it is expensive. *Depth:* this
is Domain 5's material, where it is the primary subject rather than a consequence.

**Environment variables.** Named values supplied by the shell rather than written
into a file. *Why it matters here:* `.mcp.json` is committed, so credentials go in as
references and the environment supplies the secret. *Depth:* the twelve-factor
config chapter is the clearest short statement of why.

**Process isolation.** Running work in a separate context so its intermediate state
does not persist into yours. *Why it matters here:* that is what a forked skill does
— thirty files read, one answer returned, no debris. *Depth:* any treatment of
subprocess isolation; the concept transfers directly.

**MCP — the Model Context Protocol.** A standard for handing a model your own tools:
a client talks to a server, the server advertises tools, the client calls them.
*Why it matters here:* mechanism four configures *where the server comes from*;
writing one is episode two. *Depth:* the protocol specification at
`modelcontextprotocol.io`.

---

## Script

```
Configuration is twenty percent of this exam, and it is the part people skip.

[screen: the blueprint table, Domain 3 highlighted]

Here is why skipping it is expensive. The other four domains are about building
things, so they feel like the real material. Domain 3 is about setting things up,
so it feels like admin. But it carries six task statements and a fifth of the
scored items, and almost every question in it is a judgment call rather than a
fact. Those are the ones you cannot cram.

By the end of this episode you will have a working project configured the way the
blueprint describes, and we will build on it for the next four episodes.

[screen: empty directory, terminal]

We are starting from nothing. This is the lab we are building across the whole
course: Course Doctor. It is an agent that checks training material against live
documentation and tells you what went stale.

I will say more about what it does in episode two. Today it is a skeleton,
because configuration is what we are learning.

[screen: creating CLAUDE.md]

First mechanism. CLAUDE.md.

A CLAUDE.md file is standing instructions that load automatically, so you stop
re-explaining your project every session. The exam cares about something more
specific than that: where you put it.

Because these files resolve in a hierarchy. There is a user-level one that
applies to everything you do, a project-level one that applies to this
repository, and you can put them in subdirectories too.

[screen: the hierarchy, side by side]

The decision the exam will put in front of you is which level a given rule
belongs at. And the test is not "how important is this rule." It is "who does it
apply to."

A testing convention that every engineer on the team must follow goes at the
project level, committed, because a rule that lives on one laptop is not a team
convention — it is a personal habit that the next person does not inherit.

Your own preference about how you like output formatted goes at the user level,
because putting it in the project file pushes your taste onto everyone who clones
the repo.

Get that backwards and nothing errors. It just quietly applies to the wrong
people. That is the shape of a Domain 3 question.

[screen: creating .claude/rules/ with two files]

Second mechanism, and this is the one I see missed most.

Path-specific rules. A rules file carries a small header at the top that says
which files it applies to — a glob pattern, like everything under source API, or
anything that looks like a test.

[screen: the frontmatter, zoomed]

Then the rule only loads when a matching file is in play.

Here is the consequence, and it is not just tidiness. Instructions cost context.
If every convention for every area of your codebase loads on every single task,
you are spending context on API conventions while editing a test file — and
context you spent is context unavailable for the actual work.

So this is a context-management mechanism wearing a configuration hat. Which is
why it shows up in Domain 3 and pays off again in Domain 5.

[screen: edit a matching file, show the rule applying; edit a non-matching file,
show it not applying]

And watch this, because this is the thing to actually verify rather than trust.
I am editing a file that matches the pattern. The rule applies. Now a file that
does not match. It does not.

If you only ever test the matching case, you have not tested the rule. You have
confirmed that something loaded.

[screen: creating .claude/skills/ with frontmatter]

Third mechanism. Skills.

A skill is a packaged procedure — a set of instructions for a particular kind of
task that you can invoke by name instead of re-typing.

Two frontmatter options on it are explicitly in the blueprint, and both are about
containment.

The first restricts which tools the skill is allowed to use. The second runs the
skill in a forked context, which means it does its work in isolation and does not
pollute your main conversation.

[screen: run the skill, show main context unaffected]

Think about what that second one buys. A skill that reads thirty files to answer
one question would, without isolation, leave all thirty files sitting in your
context afterwards. Fork it, and you get the answer back without the debris.

So: fork it when the work is bulky and only the conclusion matters. Don't, when
you need the detail to stay available for what comes next. That trade is the
question.

[screen: creating .mcp.json]

Fourth. Wiring in a tool server.

MCP is the Model Context Protocol — the standard way you hand Claude your own
tools. We are writing the server itself in episode two. Today we just configure
where it comes from.

[screen: the env var expansion, zoomed]

One detail worth stopping on. The credentials go in as environment variable
references, not as literal values. The config file names the variable; the
environment supplies the secret.

That is in the blueprint, and the reason is that this file is committed. Paste a
real key here and you have published it to everyone who clones the repository,
and rotating it is now the cheapest part of your day.

[screen: /mcp listing]

And there are two places a server can be configured: the project file, which the
team shares, and a personal one, which is yours alone. Both are active at the
same time. That is deliberate — it is how you try an experimental server without
pushing it onto your team.

[screen: plan mode toggle]

Fifth, and this one is pure judgment. Plan mode.

Plan mode has Claude work out an approach and show it to you before making
changes, rather than going straight to editing.

The blueprint asks when to use it. The honest answer is that it is about the cost
of a wrong direction, not the size of the task.

[screen: three tasks side by side]

A single-file bug fix where there is one obvious correct change: planning first
mostly buys you a delay.

Migrating a library across many files: plan first. Not because it is big, but
because a wrong approach applied consistently to forty files is forty things to
undo.

A new feature with several defensible designs: plan first, and this is the
strongest case of the three. When more than one answer is reasonable, the thing
you most need is to see which one is being chosen — while it is still cheap to
pick differently.

So the test is: if this goes the wrong way, how much does it cost to find out
late? Expensive means plan.

[screen: the anti-pattern slide]

Before we close, the part most prep courses leave out.

The exam guide names anti-patterns. Explicitly. In writing.

Take that seriously, because well-written multiple-choice distractors are not
random noise — they are the plausible mistakes a competent person actually makes.
That is what makes them work. So a published list of anti-patterns is a published
list of the wrong answers' shapes, handed to you before the exam.

For this domain, the ones to recognise: a convention that belongs to the team
sitting in a personal config, every rule loading on every task regardless of what
you are touching, a secret written literally into a committed file, and reaching
for plan mode by task size rather than by the cost of being wrong.

If an option on exam day looks like any of those, you have seen it before.

[screen: the repo, committed]

That is the scaffold, and it runs.

Next episode we write the MCP server — four tools, descriptions built to be told
apart, and error responses structured so the agent can tell a problem it should
retry from one it should not.

Everything in this course is sourced from the published exam guide or the public
documentation, and every claim is traced in SOURCES.md in the repo. Nothing here
comes from sitting the exam.

Repo link is below.
```

---

## Tips

Not spoken on camera — these belong in the written lesson and the episode notes.
Each one is something the documentation does not tell you.

**Test the non-matching case, or you have not tested the rule.** This is in the
script for a reason and it generalises past globs: confirming a rule fires tells you
something loaded. Only confirming it *does not* fire on a non-match tells you the
pattern is doing the selecting.

**And there are two failure modes, in opposite directions.** A glob with a typo matches
nothing, loads nothing and reports nothing. But **invalid YAML** in the frontmatter is
worse and is the documented behaviour: Claude Code ignores the frontmatter and loads the
rule unconditionally, so a typo there makes the rule universal rather than absent. Only
`claude --debug` shows the parse error.

**An unset environment variable gives you a server that registers and then fails at
call time.** The reference in `.mcp.json` resolves to nothing, configuration looks
complete, `/mcp` looks populated, and the failure arrives mid-task on the first call.
Check the variable is actually exported in the shell you launched from, not just
present in a dotfile you have not sourced.

**Both MCP scopes are live at once, so a personal server can quietly duplicate a team
one.** That is the intended behaviour — it is how you trial a server without pushing
it on anyone — but it means two entries doing the same job is a normal-looking state
rather than an error, and you will debug the wrong one.

**A subdirectory `CLAUDE.md` is the hardest instruction to find later.** When a rule
is applying and you cannot see where it came from, the project-level file is the first
place you look and a nested one is the last. Knowing they exist is most of the fix.

**Forking a skill costs you the follow-up question.** You get the conclusion without
the debris, which is the point — but the detail is gone, so you cannot then ask "which
of those thirty files was it?" without running the work again. Decide which you need
before you fork, not after.

---

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, no `/mcp` entries beyond this
      lab's server, nothing in the window title or tab bar.
- [ ] Every mechanic shown actually worked on camera. If one was cut, it does not get claimed.
- [ ] `SOURCES.md` Episode 1 documentation checklist is complete — six URLs with read dates —
      before publishing.
- [ ] Clean clone of the repo at this episode's commit reproduces everything shown.
- [ ] Description carries the repo link with the `julie-elkins` handle.
