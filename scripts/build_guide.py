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

Lessons are in **dependency order**, not exam-weight order. See the
[repository README](README.md) for the exam details, the full 29-task-statement outline
including what is not yet written, how the course is sourced, and how to run the lab.

---

"""


def build() -> str:
    """Return the full guide text, or raise if a listed lesson is missing."""
    parts = [HEADER]

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
    parts.append("\n".join(lines) + "\n\n---\n\n")

    for rel in covered:
        body = (COURSE / rel).read_text(encoding="utf-8").strip()
        parts.append(body + "\n\n---\n\n")

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
