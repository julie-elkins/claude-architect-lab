---
name: check-sources
description: Audit SOURCES.md against the repo — verify every documentation URL still resolves and still says what its row claims, and list any course claim with no traceable source. Use before publishing an episode, or when the exam guide version may have moved.
context: fork
allowed-tools: Read, Grep, Glob, WebFetch
---

# Check the sources

Verify that this course can still prove where its content came from.

**Why this skill runs forked, and it is the whole lesson in episode 1.** This audit
reads every file under `course/`, reads `SOURCES.md`, and fetches a documentation page
per row. That is bulky work where only the conclusion matters — nobody needs the forty
intermediate page bodies afterwards. Run it in the main conversation and all of it stays
in context, crowding out the work you were actually doing. Forked, you get the verdict
back and the debris is discarded.

**Why the tool list is restricted.** This skill audits; it does not fix. `Read`, `Grep`,
`Glob` and `WebFetch` are sufficient to reach a verdict, and the absence of `Edit` and
`Write` means a run cannot "helpfully" rewrite a row to match a page that changed —
which would make the audit self-confirming and destroy the only signal it produces.

## What to do

1. **Read `SOURCES.md`.** Note the recorded exam guide version string.

2. **Check the exam guide version.** Fetch the certification page named in `SOURCES.md`
   and establish whether the published guide is still the recorded version. If it has
   moved, **stop and report that first** — every exam-guide row is unverified until
   someone re-reads the guide, and continuing would produce a reassuring report about a
   stale baseline.

3. **For every row citing a URL:** fetch it and decide two separate things.
   - Does it resolve? A 404 is a dead citation.
   - **Does it still say what the row claims?** This is the one that matters and the one
     that is easy to skip. Pages get rewritten under the same URL, so a 200 is not a
     verified claim. Report these as different findings, because the remedies differ:
     a dead link needs a new URL, and a changed page needs the lesson re-checked.

4. **Find untraceable claims.** Grep the files under `course/` for factual assertions —
   numbers, version strings, named mechanics, exam figures — and check each has a row in
   `SOURCES.md`. Report anything that does not.

5. **Check the unresolved checklist.** `SOURCES.md` carries a list of mechanics still
   needing a documentation citation. Report how many remain, and name them.

## What to report

A short written verdict, in this order:

1. **Exam guide version: matches / has moved.** If it has moved, everything below is
   provisional and say so.
2. **Dead URLs**, with the row that cites each.
3. **URLs that resolve but no longer support their row**, with what the page says now.
4. **Claims in `course/` with no row in `SOURCES.md`.**
5. **Outstanding citation checklist items**, by name.

**Report an empty finding list as "no findings," never as "sources verified."** If a
fetch failed, a page was unreachable, or a step did not run, say which — a clean report
from an audit that could not complete is the exact failure this repository is built to
prevent, committed against itself.

Change nothing. The output is a verdict for a human to act on.
