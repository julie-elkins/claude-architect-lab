#!/usr/bin/env python3
"""Assemble the written lessons into one readable GUIDE.md.

Why this exists: a learner should be able to open one file and scroll the whole
course, rather than clicking in and out of 29 directories. And a 29-lesson
hand-maintained single file has costs that arrive later than the benefit —
unreadable diffs, no per-lesson history, and a single chunk where the corpus
tooling expects one chunk per lesson.

So the lessons stay the source and the guide is GENERATED. `--check` compares the
committed guide against what the lessons would produce and fails if they differ,
which is what stops the guide going quietly stale after someone edits a lesson.

Design rules:

1. READING ORDER IS DATA, not inferred from filenames. `MANIFEST` below is the
   course order, and it is dependency order rather than exam-weight order.
2. A lesson listed in MANIFEST but missing on disk is a FAILURE, not a skip. A
   silently omitted lesson is the one failure mode a generated file has that a
   hand-written one does not.
3. Two task statements may share one lesson file. The file is emitted once and
   the manifest records both, so the count of task statements covered stays
   honest without duplicating prose.
4. The generated file says it is generated, names the script, and tells the
   reader where to edit. Otherwise someone edits the guide and loses the change.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
COURSE = REPO / "course"
GUIDE = REPO / "GUIDE.md"

# Front matter included before the lessons, so the single-document reading path
# is genuinely self-contained rather than linking back out -- the clicking in and
# out of files is the thing GUIDE.md exists to avoid.
#
# Both are EXTRACTED from their own source file rather than duplicated here. Two
# copies of a notice drift, and the first time they do a reader is told something
# that is no longer true. The staleness check covers this automatically: editing
# either source makes `--check` fail until the guide is rebuilt.
NOTICE_SOURCE = REPO / "README.md"
NOTICE_HEADING = "## Certification program update: December 7, 2026"

# The pages that surround the lessons, included so the single-document reading
# path is the WHOLE course rather than the lessons alone. Added 2026-10-19: a
# learner reading GUIDE.md end to end was getting 29 lessons and none of the
# study path, scope, scenarios, themes, recall sheet, glossary or exam-day
# mechanics -- which are seven of the nine things a reader actually asks for.
#
# EXTRACTED, never duplicated, for the same reason the notice above is: two
# copies of a page drift, and `--check` makes editing either one fail the build
# until the guide is rebuilt.
#
# Each entry carries the sentence that introduces it IN THE GUIDE. A page lifted
# out of its own file loses the context its filename gave it -- "Scope" means
# nothing dropped between a lesson and a glossary -- so the lead-in is data here
# rather than prose inside the page, which has to stand alone too.
FRONT_MATTER: tuple[tuple[str, str], ...] = (
    ("STUDY-PATH.md",
     "Read this first if you have a date booked. It is the only page here that "
     "tells you what to skip."),
    ("FUNDAMENTALS.md",
     "What the exam sits on top of, and a readiness check. Skippable if you are "
     "already building with this stack daily."),
    ("SCOPE.md",
     "What the guide says is in scope, and the sixteen topics it says will not "
     "appear at all. The out-of-scope list is the cheapest page in the course: it "
     "tells you what to stop studying."),
)

# After the lessons, because each one is either an index into them or a thing to
# look up rather than to read through.
APPENDICES: tuple[tuple[str, str], ...] = (
    ("SCENARIOS.md",
     "The six published scenarios and the lessons each one needs. This is how the "
     "exam presents the material; the lessons above are how the blueprint "
     "organises it."),
    ("THEMES.md",
     "Four ideas that recur across every domain. Deliberately last of the reading "
     "pages: it means little before you have seen the instances."),
    ("RECALL.md",
     "The conventions you cannot reason your way to -- file locations, flags, enum "
     "values, and the places where the default is the opposite of the guess. Use "
     "it as a self-test, not as reading."),
    ("GLOSSARY.md",
     "The words that mean different things in different lessons. Look things up "
     "here rather than reading it through."),
    ("EXAM-DAY.md",
     "Registering, sitting, scoring and renewing. Nothing here is about the "
     "content; it is the part people discover too late."),
)

# DELIBERATELY NOT INCLUDED: SOURCES.md and VERIFICATION.md. Both are the
# course's own audit trail rather than material for a candidate -- they answer
# "can I trust this course", which is a real question and not one to answer with
# 150 lines of verification record wedged between a learner and the lessons. Both
# are linked from the pages above and from the README, and the lessons each carry
# their own Sources section inline, which is where a claim's provenance is
# actually useful.

# Dependency order: tools before the loop that calls them, the loop before the
# output it shapes. Domain 1 is the largest slice of the exam and still cannot
# come first.
MANIFEST: tuple[tuple[str, str, str], ...] = (
    ("1.1", "Design and implement agentic loops for autonomous task execution",
     "domain-1-agentic-architecture/lesson-1-1-agentic-loops.md"),
    ("1.2", "Orchestrate multi-agent systems with coordinator-subagent patterns",
     "domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md"),
    ("1.3", "Configure subagent invocation, context passing, and spawning",
     "domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md"),
    ("1.4", "Implement multi-step workflows with enforcement and handoff patterns",
     "domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md"),
    ("1.5", "Apply Agent SDK hooks for tool call interception and data normalization",
     "domain-1-agentic-architecture/lesson-1-5-hooks.md"),
    ("1.6", "Design task decomposition strategies for complex workflows",
     "domain-1-agentic-architecture/lesson-1-6-task-decomposition.md"),
    ("1.7", "Manage session state, resumption, and forking",
     "domain-1-agentic-architecture/lesson-1-7-session-state.md"),
    ("2.1", "Design effective tool interfaces with clear descriptions and boundaries",
     "domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md"),
    ("2.2", "Implement structured error responses for MCP tools",
     "domain-2-tools-and-mcp/lesson-2-2-structured-errors.md"),
    ("2.3", "Distribute tools appropriately across agents and configure tool choice",
     "domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md"),
    ("2.4", "Integrate MCP servers into Claude Code and agent workflows",
     "domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md"),
    ("4.1", "Design prompts with explicit criteria to improve precision and reduce false positives",
     "domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md"),
    ("4.2", "Apply few-shot prompting to improve output consistency and quality",
     "domain-4-prompting-and-output/lesson-4-2-few-shot.md"),
    ("4.3", "Enforce structured output using tool use and JSON schemas",
     "domain-4-prompting-and-output/lesson-4-3-structured-output.md"),
    ("4.4", "Implement validation, retry, and feedback loops for extraction quality",
     "domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md"),
    ("4.5", "Design efficient batch processing strategies",
     "domain-4-prompting-and-output/lesson-4-5-batch-processing.md"),
    ("4.6", "Design multi-instance and multi-pass review architectures",
     "domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md"),
    ("5.1", "Manage conversation context to preserve critical information across long interactions",
     "domain-5-context-and-reliability/lesson-5-1-conversation-context.md"),
    ("5.2", "Design effective escalation and ambiguity resolution patterns",
     "domain-5-context-and-reliability/lesson-5-2-escalation.md"),
    ("5.3", "Implement error propagation strategies across multi-agent systems",
     "domain-5-context-and-reliability/lesson-5-3-error-propagation.md"),
    ("5.4", "Manage context effectively in large codebase exploration",
     "domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md"),
    ("5.5", "Design human review workflows and confidence calibration",
     "domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md"),
    ("2.5", "Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively",
     "domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md"),
    ("3.1", "Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization",
     "domain-3-configuration/lesson-3-1-claude-md-hierarchy.md"),
    ("3.2", "Create and configure custom slash commands and skills",
     "domain-3-configuration/lesson-3-2-commands-and-skills.md"),
    ("3.3", "Apply path-specific rules for conditional convention loading",
     "domain-3-configuration/lesson-3-3-path-specific-rules.md"),
    ("3.4", "Determine when to use plan mode vs direct execution",
     "domain-3-configuration/lesson-3-4-plan-mode.md"),
    ("3.5", "Apply iterative refinement techniques for progressive improvement",
     "domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md"),
    ("3.6", "Integrate Claude Code into CI/CD pipelines",
     "domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md"),
)

HEADER = """# Build to Pass — Claude Certified Architect – Foundations

**This file is generated. Do not edit it.**

It is the whole written course in one document, assembled from the per-lesson files
under `course/` by `scripts/build_guide.py`. Edit the lesson, then run:

```
python3 scripts/build_guide.py
```

The test suite checks this file against the lessons, so a stale guide fails the build
rather than quietly disagreeing with the course.

**This is the whole course, in reading order.** It opens with the current program notice,
then the study path, the prerequisite stack and the scope boundary; then the 29 lessons in
**dependency order** rather than exam-weight order; then the scenarios, the recurring
themes, the recall sheet, the glossary and the exam-day mechanics.

Every section below is also a standalone file, and each one says which — the files are the
source and this document is assembled from them, so nothing here is a second copy that can
drift. Two files are deliberately *not* included, because they are the course's own audit
trail rather than material for a candidate: [SOURCES.md](SOURCES.md), which records what
this course treats as a source, and [VERIFICATION.md](VERIFICATION.md), which records which
cited pages have been re-read verbatim and which have not. Read both if your question is
whether to trust this course. Each lesson also carries its own sources inline.

See the [repository README](README.md) for the exam details, the blueprint map, and how to
run the lab.

---

"""


def extract_section(path: pathlib.Path, heading: str) -> str:
    """Pull one `## heading` section out of a markdown file, up to the next `## `.

    Raises if the heading is gone, rather than silently emitting nothing. A
    notice that quietly disappears from the guide is worse than one that was
    never there, because the README still carries it and the two now disagree.
    """
    text = path.read_text(encoding="utf-8")
    start = text.find(heading)
    if start == -1:
        raise ValueError(
            "heading %r not found in %s -- the guide cannot include a section "
            "that has been renamed or removed" % (heading, path.name)
        )
    rest = text[start + len(heading):]
    end = rest.find("\n## ")
    return (heading + (rest if end == -1 else rest[:end])).strip()


def include_page(name: str, lead_in: str) -> str:
    """One surrounding page, with its lead-in, ready to drop into the guide.

    Raises on a missing file rather than emitting nothing. Rule 2 applies to
    these exactly as it does to a lesson: a page that silently vanishes from the
    guide leaves a reader with a course that looks complete and is not, and the
    standalone file still being on disk is what makes that invisible.
    """
    path = REPO / name
    if not path.is_file():
        raise FileNotFoundError("listed page missing: %s" % name)
    body = path.read_text(encoding="utf-8").strip()
    return "> %s\n>\n> Read it standalone at [%s](%s).\n\n%s\n\n---\n\n" % (
        lead_in, name, name, body,
    )


def build() -> str:
    """Return the full guide text, or raise if a listed lesson or page is missing."""
    parts = [HEADER]

    # The program-update notice, lifted from the README so there is one copy.
    parts.append(extract_section(NOTICE_SOURCE, NOTICE_HEADING) + "\n\n---\n\n")

    for name, lead_in in FRONT_MATTER:
        parts.append(include_page(name, lead_in))

    covered: dict[str, list[str]] = {}
    for ts, _title, rel in MANIFEST:
        covered.setdefault(rel, []).append(ts)

    missing = [rel for rel in covered if not (COURSE / rel).is_file()]
    if missing:
        # Rule 2. A listed lesson that silently vanished from the guide is the
        # one failure a generated file has that a hand-written one does not.
        raise FileNotFoundError(
            "listed in MANIFEST but not on disk: " + ", ".join(sorted(missing))
        )

    lines = ["## Contents", ""]
    for rel, statements in covered.items():
        text = (COURSE / rel).read_text(encoding="utf-8")
        title = next(
            (l[2:].strip() for l in text.splitlines() if l.startswith("# ")),
            rel,
        )
        label = "TS " + " and ".join(statements)
        lines.append("- **%s** — %s" % (label, title))
    # The appendices are listed here too. A reader who has scrolled past 29
    # lessons will not discover a recall sheet at the bottom by accident.
    lines.append("")
    lines.append("**After the lessons:** " + " · ".join(
        name.removesuffix(".md") for name, _ in APPENDICES
    ))
    parts.append("\n".join(lines) + "\n\n---\n\n")

    for rel in covered:
        body = (COURSE / rel).read_text(encoding="utf-8").strip()
        parts.append(body + "\n\n---\n\n")

    for name, lead_in in APPENDICES:
        parts.append(include_page(name, lead_in))

    return "".join(parts).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assemble the written lessons into GUIDE.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if GUIDE.md is not what the lessons produce",
    )
    args = parser.parse_args(argv)

    try:
        text = build()
    except FileNotFoundError as exc:
        print("build-guide: %s" % exc, file=sys.stderr)
        return 2

    if args.check:
        current = GUIDE.read_text(encoding="utf-8") if GUIDE.exists() else ""
        if current != text:
            print(
                "build-guide: GUIDE.md is STALE.\n"
                "A lesson changed and the guide was not regenerated, so the guide\n"
                "and the course now disagree. Run: python3 scripts/build_guide.py",
                file=sys.stderr,
            )
            return 1
        print("build-guide: GUIDE.md is current (%d task statement(s))." % len(MANIFEST))
        return 0

    GUIDE.write_text(text, encoding="utf-8")
    print(
        "build-guide: wrote %s — %d task statement(s), %d lesson file(s), %d words."
        % (
            GUIDE.relative_to(REPO),
            len(MANIFEST),
            len({rel for _, _, rel in MANIFEST}),
            len(text.split()),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
