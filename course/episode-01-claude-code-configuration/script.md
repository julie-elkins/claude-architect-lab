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

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, no `/mcp` entries beyond this
      lab's server, nothing in the window title or tab bar.
- [ ] Every mechanic shown actually worked on camera. If one was cut, it does not get claimed.
- [ ] `SOURCES.md` Episode 1 documentation checklist is complete — six URLs with read dates —
      before publishing.
- [ ] Clean clone of the repo at this episode's commit reproduces everything shown.
- [ ] Description carries the repo link with the `julie-elkins` handle.
