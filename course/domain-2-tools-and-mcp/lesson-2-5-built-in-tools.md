# Lesson 2.5 — The built-in tools, and the two that are not there

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.5:** Select and apply built-in tools (Read, Write, Edit, Bash, Grep,
Glob) effectively.

Lab artifact: tracing Course Doctor's own call path using the search strategy below,
rather than reading the whole package.

## What you will be able to do afterwards

Choose the right tool for a search or an edit, build understanding of an unfamiliar
codebase without reading all of it — and know why a permission rule written for `Grep`
may match nothing on your machine.

## Why the exam cares

The guide's framing is selection: Grep for content, Glob for paths, Read and Write for
whole files, Edit for targeted changes. And it names a *strategy*, not just a mapping —
**start with Grep to find entry points, then Read to follow imports and trace flows,
rather than reading all files upfront.**

That is a context-management answer wearing a tooling hat, which is why it sits here and
pays off in Domain 5. Reading twenty files to answer one question spends the budget you
needed for the answer.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Content search versus path search.** Finding text inside files against finding files by
name. *Why it matters here:* it is the Grep/Glob distinction and the guide's first
knowledge item. *Depth:* `man grep`, `man find`.

**Anchored editing.** Changing a file by matching surrounding text rather than by line
number. *Why it matters here:* it is how Edit works, and why it fails when the anchor is
not unique. *Depth:* any treatment of patch application.

**Incremental exploration.** Building understanding by following references from an entry
point. *Why it matters here:* it is the named strategy, and the alternative is reading
everything. *Depth:* Domain 5 TS 5.4.

**Default tool sets.** Which tools a session actually has, which is not the same as which
tools exist. *Why it matters here:* see the build. It is the whole surprise in this
lesson. *Depth:* `/docs/en/tools-reference`.

## The idea, before any commands

**Match the tool to the question.**

- *Where is this string?* → content search.
- *Which files are named like this?* → path search.
- *What does this file say?* → Read.
- *Change this one part* → Edit.
- *Replace the whole thing* → Write.

**Then sequence it.** The guide's strategy is Grep to locate, Read to follow. For tracing
a function across wrapper modules it names a two-step: identify all exported names first,
then search for each across the codebase. That beats opening files and hoping.

**And know what your session actually has.** Which is the part nobody expects.

## The build

### Step 1 — the surprise, and it matters for your permission rules

> **"On macOS, Linux, and WSL, Claude Code leaves Glob and Grep out of the default tool
> set, and Claude searches with `find` and `grep` through the Bash tool instead. In
> Claude's shell those two commands run embedded versions of `bfs` and `ugrep`, and the
> searches reach your hooks and permission rules as `Bash` calls."**

On Windows, `Glob` is in the default set. On the platforms most developers use, **it and
`Grep` are not.**

Three consequences:

1. A **permission rule** written for `Grep` matches nothing on macOS or Linux, because the
   search never arrives as a `Grep` call. It arrives as `Bash`.
2. A **hook** matching `Grep` never fires there either.
3. A **subagent tool list** naming `Grep` and `Glob` is naming tools that may not be in
   the set to begin with.

The exam guide's TS 2.5 discusses *selecting* Grep and Glob as though they are simply
available, which is true of the objective and not of every platform. Both facts are worth
holding: the guide tests the selection reasoning; the documentation tells you what your
session has.

### Step 2 — Edit, and the uniqueness rule

> **"`old_string` must appear exactly once. When it appears more than once, Claude either
> supplies a longer string with enough surrounding context to pin down one occurrence, or
> sets `replace_all: true` to replace them all."**

Which is why the guide names the fallback as a tested skill: **when Edit cannot find a
unique anchor, use Read followed by Write.** Read the whole file, write the whole file,
no anchor needed.

### Step 3 — explore incrementally

Tracing how a lesson's cited URLs reach the fetch layer:

```
1. search content for "urls"           -> finds the extractor and its tests
2. Read the extractor                  -> gives the function name and its caller
3. search content for that name        -> finds every call site
4. Read only those                     -> the flow, without the package
```

Four steps, four files read instead of twenty. The guide's words for the alternative are
*reading all files upfront*, and it names the incremental version as the skill.

### Step 4 — note what prompts and what does not

Permission behaviour differs by tool, and in Manual mode for paths inside the working
directory: `Read`, `Grep` and `Glob` do not prompt; `Edit`, `Write` and `Bash` do. But
**`Read`, `Grep` and `Glob` still prompt for paths outside the working directory**, and
`Bash` runs a built-in set of read-only commands without prompting even though it is
marked as requiring permission.

So "read tools are free" is nearly true and wrong at the boundary — which is the boundary
that matters, because that is where somebody reaches outside the project.

## Tips

Things the documentation does not tell you.

**If a permission rule or hook for `Grep` never fires, check your platform before your
syntax.** On macOS, Linux and WSL the search is a `Bash` call. This is the single most
expensive surprise in this task statement, and nothing warns you — the rule is valid, it
simply never matches.

**`Bash` is marked as requiring permission and still runs read-only commands without
prompting.** So the permission column tells you less than it appears to, in both
directions.

**An Edit that fails on a non-unique anchor is not an error to work around with a longer
anchor every time.** Sometimes the honest answer is Read plus Write, which the guide names
as the fallback — and it is more reliable on a file where the same line appears five
times.

**Reading a file to find out whether it is relevant is the expensive habit.** Search
first. The file list from a content search is itself information, and it costs almost
nothing next to opening each one.

**Export names first, then search each one** when tracing through wrapper modules. The
guide names this specifically, and it is the difference between finding every caller and
finding the ones you guessed.

## The anti-pattern

From the guide's objectives:

> **Reading all files upfront** instead of building understanding incrementally from an
> entry point.

And the one the documentation adds:

> **Assuming a tool is in your session's tool set because it exists.**

Same family as the rest of this course: configuration that looks correct and does nothing.
A rule naming a tool the session does not have is not an error — it is silently inert,
which is the worst of both.

## What this lesson does not cover

- **Context management as a subject** — Domain 5, especially TS 5.4 on large codebases.
- **Subagents for exploration** — Domain 1 TS 1.3, and lesson 3.4 for the `Explore` agent.
- **Permission rule syntax** in depth. Named here for where tool names appear; the rules
  themselves are configuration rather than tool selection.
- **Custom tools via MCP** — lessons 2.1 through 2.4.
- **Every built-in tool.** There are far more than six. This covers the six the task
  statement names, plus the availability fact that changes how two of them behave.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.5.

| Claim | Source |
|---|---|
| Grep for content search; Glob for file path pattern matching; Read/Write for full file operations; Edit for targeted modifications using unique text matching | EG §6, TS 2.5 |
| When Edit fails due to non-unique text matches, using Read + Write as a fallback | EG §6, TS 2.5 |
| Building codebase understanding incrementally — Grep for entry points, then Read to follow imports — rather than reading all files upfront | EG §6, TS 2.5 |
| Tracing function usage across wrapper modules by identifying exported names, then searching each across the codebase | EG §6, TS 2.5 |
| Selecting Glob for files matching naming patterns, e.g. `**/*.test.tsx` | EG §6, TS 2.5 |
| "On macOS, Linux, and WSL, Claude Code leaves Glob and Grep out of the default tool set, and Claude searches with `find` and `grep` through the Bash tool instead... the searches reach your hooks and permission rules as `Bash` calls." | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| On Windows, Glob is part of the default tool set | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| Tool names are the exact strings used in permission rules, subagent tool lists and hook matchers | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| Edit: "`old_string` must appear exactly once"; otherwise more surrounding context or `replace_all: true` | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| `Read`, `Grep` and `Glob` do not prompt inside the working directory but still prompt outside it; `Bash` is marked as requiring permission yet runs a built-in read-only command set without prompting | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| `Read` reads file contents; `Write` creates or overwrites files; `Bash` executes shell commands; `Edit` makes targeted edits | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
