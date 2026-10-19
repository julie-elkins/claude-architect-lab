# What has actually been verified, and what has not

This page exists because **"cited" and "verified" are different claims**, and the gap
between them is where a course goes quietly wrong. `scripts/check_citations.py` proves every
claim row names a source and every URL carries a read date. That is a structural property.
It says nothing about whether the page still says the thing.

This file is the record of the stronger check, and it is the file `check_citations.py` reads
to report coverage. **A page not listed below is reported as unverified**, so forgetting to
add one understates coverage rather than overstating it. That direction is deliberate.

---

## The three states a cited page can be in

| State | Means |
|---|---|
| **RE-VERIFIED** | Re-fetched on the date shown, with the check demanding the claim's **verbatim wording** back. A paraphrase was not accepted as a pass. |
| **AUTHORED, NOT RE-VERIFIED** | The page was read when the lesson was written and the claim came from that read. It has not been checked since. |
| **NOT CHECKED** | No read on record. There are currently none of these. |

**"AUTHORED, NOT RE-VERIFIED" is not a defect and is not a pass.** It is the honest state
of most of this course, and it decays: every day it is a slightly weaker claim, because the
documentation moves and nothing here notices.

---

## Re-verified, 2026-10-18 and 2026-10-19

Six pages. The reason the first five and not others is recorded below under *why this
subset*; `memory` was next because it carries the most claim rows in the course.

| Page | Date | Result |
|---|---|---|
| `https://code.claude.com/docs/en/hooks` | 2026-10-18 | verbatim match |
| `https://code.claude.com/docs/en/sub-agents` | 2026-10-18 | verbatim match |
| `https://code.claude.com/docs/en/mcp` | 2026-10-18 | verbatim match |
| `https://code.claude.com/docs/en/skills` | 2026-10-18 | verbatim match |
| `https://platform.claude.com/docs/en/build-with-claude/structured-outputs` | 2026-10-18 | verbatim match |
| `https://code.claude.com/docs/en/memory` | 2026-10-19 | verbatim match, 22 of 22 rows |

### `memory`, 2026-10-19 — the method changed, and that is the headline

**Every one of the 22 claim rows citing this page came back verbatim. Contradictions:
zero.**

**The method is different from the 10-18 pass and is strictly better.** Appending `.md` to
a docs URL serves the **raw page source** — `https://code.claude.com/docs/en/memory.md`
returned 51,526 bytes of `text/markdown`. The 10-18 pass had to ask a fetch tool for
verbatim wording and trust that it complied; the five pages re-verified that day were
re-verified precisely *because* that tool had previously returned model-generated
summaries. **Fetching the source removes the question rather than managing it**, and every
remaining page should be re-verified this way.

**One methodological trap, found by hitting it.** Two claims first reported as MISSES were
both false alarms:

- The lesson quotes *"To block an action regardless of what Claude decides, use a PreToolUse
  hook instead."* The page says exactly that — with the link markup inside the sentence:
  `use a [PreToolUse hook](/docs/en/hooks-guide) instead`. **A verbatim probe against raw
  markdown must normalise inline links**, or a correct quote reads as a missing one.
- The other was an escaping error in the probe itself.

**Both failed in the safe direction** — a false MISS costs a minute of checking, where a
false MATCH would have left a stale claim marked verified. A checker for this should be
built to fail that way on purpose.

**Omissions found: six**, all now written into the lessons. Two change what a reader would
do, and both are the course's own thesis:

1. **Claude Code reads a `CLAUDE.md` of up to 4 MiB in full and SKIPS a larger file.** Not
   truncate — skip. A dropped file produces no instruction and no error. Added to 3.1.
2. **Auto memory loads the first 200 lines of `MEMORY.md` or the first 25KB, whichever comes
   first.** Two cutoffs, so a file under 200 lines can still be cut by the byte limit.
   Added to 3.1.
3. **Managed policy `CLAUDE.md` files cannot be excluded**, so organization-wide
   instructions always apply. Added to 3.1.
4. **Patterns without braces do not count against** the 1,000-pattern / 4 MiB brace budget.
   The lesson taught the budget without the qualifier. Added to 3.3.
5. **Before v2.1.217, a `paths` value with many brace groups stalled or crashed the CLI at
   startup** rather than being refused — so on an old build a budget-busting pattern does
   not report a budget. Added to 3.3.
6. **Before v2.1.211, rules that load on demand — path-scoped rules and rules in nested
   `.claude/rules/` directories — loaded even when `project` was excluded.** The exclusion
   was configured, read as applied, and did not hold. Added to 3.3.

**Checked and already correct, so recorded rather than changed:** lesson 3.1's `AGENTS.md`
treatment, including the per-combination table and the **v2.1.277** floor for reading
`AGENTS.md` directly. The page confirms the default the lesson states — with an
`AGENTS.md` *and* a `CLAUDE.md` or `CLAUDE.local.md` at or above the working directory,
Claude reads **the `CLAUDE.md` files only** — and adds that this default is changeable
through the **Project instructions** setting, which the lesson also carries.

**Version floors on this page that the course deliberately does not teach**, because they
are outside the exam guide's scope rather than missing: `/doctor prompt-audit` (v2.1.283),
the `cc-plugin-agents-md@builtin` plugin ID change (v2.1.285), `/memory` opening behaviour
(v2.1.216), `AGENTS.md` availability on Bedrock and telemetry-disabled sessions (v2.1.281),
and link-target exclusion matching (v2.1.239).

**Contradictions found: zero.** Every claim the lessons quoted from these five pages came
back word for word, including the two that carry the most weight in the course:

- the fail-open hook default, and `onFailure: "block"` as the fix (lesson 1.5)
- *"Claude Code removes every other built-in tool from a background subagent, whether
  inherited or listed in the `tools` field"* (lesson 1.3)

**Omissions found: six**, all now written into the lessons. An omission is not a wrong
claim, but on four of these six the missing fact changes what a reader would do:

1. **`onFailure` requires Claude Code v2.1.295 or later.** On an older build the key is
   ignored rather than rejected, so the hook stays fail-open and the config still reads as
   enforced. Added to lesson 1.5, which is the lesson about exactly that failure shape.
2. **`onFailure` also accepts `"continue"`**, and with `"block"` set the behaviour matches
   exit code 2 per event — except on `PermissionRequest`, where it denies. Added to 1.5.
3. **A third structured-output limit: 20 tools with `strict: true` per request**, alongside
   the 24 optional parameters and 16 union-typed parameters already taught. All three are
   *combined totals per request, not per tool*, which is how they surprise you. Added to 4.3.
4. **A 180-second compilation timeout**, plus unquantified internal limits on compiled
   grammar size — so a schema can be rejected without crossing any published number. 4.3.
5. **`name` is optional in `SKILL.md`** (defaults to the directory name) and `description`
   is only *recommended* (falls back to the first non-empty line of the body). Added to 3.2,
   with the consequence: relying on the fallback makes your opening sentence routing logic.
6. **`description` + `when_to_use` is truncated at 1,536 characters in the skill listing**,
   so a trailing "do not use this when…" is the part most likely to be cut. 3.2.

Plus one correction that was not a documentation question at all: lesson 3.2 said *"Five
frontmatter fields"* over an example block containing **six**. Fixed, and `agent:` is now
named in the prose.

### Why this subset

These five pages originally came back from the fetch tool as **model-generated summaries
rather than page text**. A claim written from a summary is a paraphrase of a paraphrase, and
the failure mode is specific: a summary can be faithful in substance and still drop a
qualifier, a version floor or a scope word — which is precisely what four of the six
omissions above were.

The remaining eight pages are believed to have returned raw page text at authoring time.
**That belief is not evidence** — it rests on recollection of an earlier working session,
not on anything retained — so this file does not grant them a stronger state on the strength
of it. They are listed as authored-and-not-re-verified, same as any unchecked page.

---

## Not re-verified

Seven pages. Every claim cited to these came from a read at authoring time
(2026-10-13 to 2026-10-17) and has not been checked since.

Ranked by how many claim rows depend on them, which is the order to work in — a stale
claim on a page carrying 22 rows costs more than one on a page carrying 4. These counts
come from `check_citations.py`, which reads them out of the lessons' Sources tables rather
than being maintained here by hand.

| Page | Claim rows |
|---|---|
| `https://code.claude.com/docs/en/agent-sdk/agent-loop` | 10 |
| `https://code.claude.com/docs/en/sessions` | 10 |
| `https://platform.claude.com/docs/en/build-with-claude/batch-processing` | 7 |
| `https://code.claude.com/docs/en/cli-reference` | 6 |
| `https://code.claude.com/docs/en/permission-modes` | 6 |
| `https://code.claude.com/docs/en/tools-reference` | 6 |
| `https://code.claude.com/docs/en/headless` | 4 |

**`memory` was the one to do first and it is done** — 2026-10-19, above. Next by claim
count is `agent-sdk/agent-loop` at 10, tied with `sessions`. Use the raw-markdown method
(`<url>.md`); it is faster and it removes the paraphrase question rather than managing it.

**A correction worth recording, because it is the mistake this course keeps teaching
about.** An earlier draft of this page put `memory` at **44** claim rows. That number came
from a grep across `course/**/*.md` *and* the repository root — and `GUIDE.md` is generated
by concatenating every lesson, so every citation was counted twice. The figure was exactly
double and looked entirely plausible. It was caught only because `check_citations.py` counts
from the Sources tables of the manifest's lesson files and disagreed. **A generated file in
the search path double-counts silently**; nothing about the output says so.

---

## What this process still cannot tell you

**The exam guide is not verifiable from here, and it is the source of 205 of the 329 claim
rows.** It is a PDF read once, at the version stated in each lesson's Sources block
(**Version 1.0, effective July 2026**). If it is revised, nothing in this repository
notices. The December 7, 2026 content update makes that a dated risk rather than a
theoretical one — see the README notice.

**A verbatim match proves the page says it; it does not prove the lesson teaches it
correctly.** Lesson 3.3 once taught a real documented failure mode *backwards* while citing
the right page. That class of error survives this entire check, and the only thing that
caught it was reading the lesson against the page with the question "does this follow?"
rather than "is this quoted?"

**The same agent wrote the claims and ran the check.** This is the live case of what lesson
4.6 teaches about a model reviewing its own work: the check can confirm wording, and it
cannot notice a framing both passes share. The partial defence used here was to demand
verbatim quotes rather than a judgement, so the page's own words had to come back —
a weaker claim than independent review, and a stronger one than self-assessment.

**Nothing here is automated and nothing watches for drift.** There is no scheduled re-check
and no tripwire on the documentation changelog. Re-verification happens when a person runs
it, and this file is how you tell whether that has happened lately.

## Sources

The verdicts above are the author's, from the re-fetch performed 2026-10-18. Quoted
documentation wording is the documentation's own, retrieved on that date. The lesson
mappings and the judgement of which omissions "change what a reader would do" are the
author's.
