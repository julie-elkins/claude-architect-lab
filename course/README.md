# Course files

**The course outline lives on [the repository front page](../README.md)** — all 29 task
statements, in reading order, with their status. It is kept in one place on purpose: two
copies of a 29-row list drift, and the first time they do, a reader is told a lesson
exists that does not.

## What is in here

Organised by exam domain, one folder per domain:

- **`domain-*/lesson-*.md`** — the written lessons. These are the course. Each is a
  single file you read start to finish, and each is named for the task statement it
  covers.
- **`domain-*/production/`** — **production assets**, not lessons: spoken narration,
  screen directions, slide bodies and a recording checklist for the video version of
  that domain. Kept because the video is planned. You do not need them to take the
  course, and each opens with a header saying so.

Reading the whole course in one scroll instead: **[GUIDE.md](../GUIDE.md)**, generated
from these lessons.

## The shape every lesson follows

What you will be able to do afterwards · why the exam cares · **fundamentals**, written
to be skippable so one block serves a newcomer and a senior · the idea before any files ·
the build with real commands · **tips** the documentation does not tell you · the
published anti-pattern · what the lesson does not cover · sources.

Two of those are worth explaining.

**Fundamentals** exists so the course does not have to pick an audience. Four to six
entries, each a term, a one-line gloss, why it matters in that lesson, and where to go
for real depth. A senior reads the glosses and moves on; a newcomer has somewhere to go.
Nothing later in a lesson depends on having followed a link.

**Tips** are only ever things the documentation does not say, and they go after the build
— a tip about something you have not done yet is a warning you cannot use. The test for
including one is whether it cost somebody an hour.

Every claim in every lesson traces to an exam-guide section or a documentation URL with a
read date, in [SOURCES.md](../SOURCES.md). Claims measured by running something are
labelled `OBSERVED`, which is a weaker claim than a citation and is marked as such.
