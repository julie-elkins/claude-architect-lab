# Lesson 3.3 — Rules that only load when they are relevant

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.3:** Apply path-specific rules for conditional convention loading.

Lab artifact: Course Doctor's conventions split so that the test rules are absent from
context while you edit the library.

## What you will be able to do afterwards

Choose between a path-specific rule and a subdirectory instruction file for a given
convention, and say which one you chose and why in one sentence.

And demonstrate that a rule did **not** load — which is the harder and more useful half.

## Why the exam cares

The guide's own stated skill is **"choosing path-specific rules over subdirectory
CLAUDE.md files when conventions must apply to files spread across the codebase."**

That is a judgment item, and it has a clean discriminator. A subdirectory instruction
file is scoped by *location*. A path-specific rule is scoped by *pattern*. So the
question is always: are the files this convention governs **in one place**, or **spread
by type**?

Test files are the canonical example — they live beside the code they test, scattered
through the tree. There is no directory to put their conventions in. `**/*.test.tsx`
catches all of them regardless of where they sit, which is the thing a subdirectory file
structurally cannot do.

And the reason this sits in Domain 3 but pays off in Domain 5: **instructions cost
context.** A convention loaded while irrelevant is budget spent on nothing.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

Skip what you know.

**Glob patterns.** Wildcards that match paths. `*` matches within one path segment;
`**` crosses segments; so `src/api/**/*` is everything at any depth under `src/api`, and
`**/*.test.tsx` is every file of that type anywhere. *Why it matters here:* the pattern
*is* the scoping mechanism, so a wrong glob is a rule that never loads. *Depth:*
`man 7 glob`, or your shell's pattern documentation.

**YAML frontmatter.** A short block of key/value metadata at the top of a file, fenced
by `---` lines. *Why it matters here:* it is where a rules file declares its `paths`.
*Depth:* `yaml.org`; you need only the mapping and list forms.

**Conditional loading.** Content read only when a trigger fires, rather than always.
*Why it matters here:* it is the whole mechanism. *Depth:* lazy loading in any build
system is the same idea with a different trigger.

**The context window as a budget.** Everything loaded occupies finite space, and what
you spend is unavailable for the work. *Why it matters here:* it is the reason the
mechanism exists at all. *Depth:* Domain 5, where this is the subject rather than a
consequence.

**Scoping by location versus by type.** Two different ways to say "this applies here."
*Why it matters here:* this is the exam's discriminator, stated above. *Depth:* none
needed — it is a distinction rather than a technology.

## The idea, before any files

One question decides it: **can you draw a directory around the files this convention
governs?**

If yes — everything under `terraform/`, say — a subdirectory instruction file is simpler
and needs no pattern.

If no, because the files are defined by *what they are* rather than *where they live*,
you need a pattern. Tests, migrations, generated files, anything with a naming
convention: all scattered by design.

The second question is cheaper and people skip it: **would this convention be noise on a
task that does not touch those files?** If yes, conditional loading is not tidiness, it
is the point.

## The build

Course Doctor has two sets of conventions that should not travel together: how its MCP
tools are written, and how its tests are written.

### Step 0 — the grammar, now that it is documented

`paths` is the **only** field Claude Code reads from a rule. Any other field is ignored
without an error. It accepts a YAML list or a comma-separated string, and the frontmatter
is stripped before the rule is loaded.

A path-scoped rule loads when Claude uses Read, Write or Edit on a matching file — and
also when it views one with a Bash command that counts as a read, like `cat` or `head`.
**A rule with no `paths` field loads unconditionally.**

Brace expansion works and has a budget: `src/**/*.{ts,tsx}` expands to two patterns, and
a rule's whole `paths` list shares a ceiling of 1,000 expanded patterns and 4 MiB —
**patterns without braces do not count against it.** A pattern that would exceed the
budget **is used unexpanded, so its literal braces match nothing.**
And `[` starts a bracket expression, so `photos [2024/**` is invalid and matches nothing
while the rule's other patterns keep working; escape it as `photos \[2024/**`.

**Two version floors on exactly this mechanism, and they matter because the older
behaviour looks like your pattern being wrong.** Before Claude Code **v2.1.217**, a
`paths` value with many brace groups *stalled or crashed the CLI at startup* rather than
being refused — so a budget-busting pattern on an old build does not report a budget. And
before **v2.1.211**, rules that load on demand, including path-scoped rules and rules in
nested `.claude/rules/` directories, **loaded even when `project` was excluded** — the
exclusion was configured, read as applied, and did not hold. Both are the course's
recurring shape: the configuration says one thing and the version decides.

### Step 1 — a rule scoped by pattern

```
mkdir -p .claude/rules
```

`.claude/rules/tests.md`:

```
---
paths: ["tests/**/*"]
---

Tests that assert an ABSENCE must be mutated inverted: add the forbidden thing
and confirm the test fails. A test that passes because the thing is missing
goes on passing after it arrives.
```

`.claude/rules/mcp-tools.md`:

```
---
paths: ["src/course_doctor/server.py", "src/course_doctor/contracts.py"]
---

Every tool parameter description says what a WRONG value does, not what type
it is. A bare type restatement passes a truthiness check and tells a caller
nothing.
```

Two files, two patterns, neither loading unless a matching file is in play.

### Step 2 — prove the negative

This is the step that matters and the one almost everybody skips.

Start a session and touch nothing. Both rule files exist on disk. **Neither should be in
context**, because no matching file has been opened.

Then edit something under `tests/`. The test rule arrives. Then edit a file matching
neither pattern. It should not.

**Verifying only the matching case tells you something loaded. It does not tell you the
pattern is doing the selecting.**

And there are **two failure modes, in opposite directions**, which is why testing the
non-match is not optional:

- **Valid YAML, bad glob.** The pattern matches nothing, the rule never loads, and nothing
  reports it. A rule that never fires looks exactly like a rule you have not needed yet.
- **Invalid YAML.** This one is worse and it is the documented behaviour: *"If the YAML
  between the markers doesn't parse, Claude Code ignores the frontmatter and loads the rule
  as if it had no `paths`."* So a typo in the frontmatter does not disable the rule — **it
  makes the rule universal**, loaded on every file, which is the exact opposite of the
  context saving you wrote it for.

`claude --debug` shows the parse error. Nothing else will.

### Step 3 — choose deliberately, and write down which

For each convention, say in one line whether it is location-scoped or type-scoped:

- MCP tool conventions → two named files. Could be a subdirectory file; the pattern is
  more precise, because `src/course_doctor/` holds the library too and the library has
  no MCP dependency on purpose.
- Test conventions → `tests/**/*` today, and would become `**/*_test.py` the moment
  tests move beside the code they test. **Type-scoped, so pattern-scoped.**

## Tips

Things the documentation does not tell you.

**A rule that has never fired is indistinguishable from a rule with a broken glob.** The
only evidence you have a working pattern is having watched it not match something.

**There is no precedence between user rules and project rules.** The documentation is
explicit: *"Claude Code loads user-level rules before project rules... Neither set
overrides the other: if a user rule and a project rule conflict, Claude may follow either
one, so keep the two consistent."* Everyone assumes the more specific wins. A conflict is
not a precedence puzzle; it is a bug, and the fix is removing the conflict.

**Each rules file counts separately toward the combined instruction-length warning.**
Splitting one long instruction file into six rules files does not reduce the total if
they all match the file you are editing — it only helps when they *don't*. Splitting by
topic and splitting by path are different moves, and only the second buys context back.

**A broken frontmatter makes a rule apply everywhere, not nowhere.** This is the one to
remember, because the intuition runs the other way. A rule you meant to scope to tests,
with a YAML typo, is now in context on every task — and it still works, so nothing
complains.

**Pin the pattern you expect to change.** `tests/**/*` is a directory assumption wearing
a glob. The day tests move next to their code, the rule silently stops matching. A
pattern written against the file *type* survives the reorganisation; one written against
the current layout does not.

**Narrow patterns beat clever ones.** Two explicit filenames are easier to verify than
one regex-ish glob that covers both plus something you did not intend.

## The anti-pattern

From the guide's objectives for this domain, the failure is:

> **Every rule loading on every task regardless of what you are touching.**

The monolithic instruction file is the common form: one file, every convention,
always loaded. It works, it is simple, and it spends context on API conventions while
you edit a test.

The subtler form, and the one the task statement is actually pointing at:

> **Reaching for a subdirectory instruction file when the files are spread by type.**

It is the intuitive move — put the convention near the code — and it quietly covers only
the files that happen to live in that directory today. The convention appears to be in
force and is absent everywhere else, which is worse than not having written it, because
you believe it is handled.

## What this lesson does not cover

- **CLAUDE.md hierarchy and scoping** — lesson 3.1, and worth reading first.
- **Symlinked rule directories.** `.claude/rules/` supports symlinks for sharing rules
  across projects, and a symlink pointing outside the working directory is treated as an
  external import needing approval. Real, and beyond this task statement.
- **Hooks.** A rule is context; a hook is a control. Lesson 3.1 covers the distinction,
  Domain 1 TS 1.5 covers hooks.
- **Context budget as a subject** — Domain 5.
- **Skills and slash commands** — lesson 3.2.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.3.

| Claim | Source |
|---|---|
| `.claude/rules/` files use YAML frontmatter `paths` fields containing glob patterns for conditional rule activation | EG §6, TS 3.3 |
| Path-scoped rules load only when editing matching files, reducing irrelevant context and token usage | EG §6, TS 3.3 |
| Glob-pattern rules are advantageous over directory-level CLAUDE.md for conventions spanning multiple directories | EG §6, TS 3.3 |
| Example patterns `paths: ["terraform/**/*"]` and `**/*.test.tsx` | EG §6, TS 3.3 |
| Choosing path-specific rules over subdirectory CLAUDE.md when conventions apply to spread-out files is a tested skill | EG §6, TS 3.3 |
| "Neither set overrides the other: if a user rule and a project rule conflict, Claude may follow either one" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Each CLAUDE.md, rules file and `@path` import counts separately toward the combined-length warning | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| `.claude/rules/` organises topic-specific rule files as an alternative to a monolithic CLAUDE.md | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| `[` starts a bracket expression; an invalid one matches nothing while the rule's other patterns keep working, and a literal `[` is escaped as `\[` | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Brace expansion shares a budget of 1,000 expanded patterns and 4 MiB; a pattern exceeding it is used unexpanded and its literal braces match nothing | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Patterns without braces do not count against the brace-expansion budget | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-19 |
| "Before v2.1.217, a `paths` value with many brace groups stalled or crashed the CLI at startup" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-19 |
| "Before v2.1.211, rules that load on demand, including path-scoped rules and rules in nested `.claude/rules/` directories, loaded even when `project` was excluded" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-19 |
| "If the YAML between the markers doesn't parse, Claude Code ignores the frontmatter and loads the rule as if it had no `paths`." `claude --debug` shows the parse error | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| A path-scoped rule loads on Read, Write or Edit of a matching file, and on a Bash command that counts as a read such as `cat` or `head` | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| A rule without a `paths` field loads unconditionally | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| `paths` accepts a YAML list or a comma-separated string | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| `paths` is the only field Claude Code reads from a rule; any other field is ignored without an error, and the frontmatter is stripped before loading | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |

**Verified by running it, 2026-10-13** — recorded as `OBSERVED`, a weaker claim than a
citation:

- Both rule files were present on disk and **not** in context, because no matching file
  had been touched. This is the lesson's central claim and it is demonstrable rather
  than asserted.

**Citation closed 2026-10-17**, and it corrected this lesson rather than confirming it:
the first version taught that a bad pattern makes a rule silently absent. The documented
behaviour for *invalid YAML* is the opposite — the rule loads unconditionally. Both failure
modes are now taught.
