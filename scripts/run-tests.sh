#!/usr/bin/env bash
#
# Run the suite and fail a run whose SHAPE is wrong, not just one with a failing
# assertion.
#
# WHY THIS EXISTS RATHER THAN A BARE `pytest`. Several tests here prove an ABSENCE --
# that a path outside the root is refused, that nothing is read on a refusal, that no
# URL is fetched. An absence test passes trivially if it never runs, and a test that
# did not run looks exactly like a test that passed. So this script pins the collected
# count and requires zero skips.
#
# The floor is a COLLECTION check, not a coverage target. Raise it per episode when
# tests are added, never per test -- a floor edited on every commit is a floor nobody
# reads.
set -euo pipefail

cd "$(dirname "$0")/.."

# Episode 1: 41 tests, 0 skips. Update this when an episode adds tests.
# 2026-10-19: +4 for RECALL.md — link resolution, term-still-in-lesson, the
# page's own ceiling disclaimer, and the README's count of surprising defaults.
# +1 more: this floor against the test count stated in README.md and CLAUDE.md,
# both of which had gone stale downward.
# 2026-10-19 (later): 61 -> 83. The network arrived with check_quote_on_page --
# 17 for the citations library and 5 for its adapter. Two previously pinned tests
# were EDITED rather than deleted: the open-world hint is now asserted per tool in
# both directions, and the protocol test lists both tools by name.
# 2026-10-19 (later still): 83 -> 87. GUIDE.md now assembles the seven learner-
# facing root pages as well as the lessons, so four tests pin that a declared page
# exists, is actually emitted, raises when missing, and that the two deliberate
# omissions are explained in the guide itself.
# 2026-10-19 (last): 87 -> 88. Every lesson's Fundamentals block now carries a
# skip signpost, pinned so a NEW lesson cannot ship without one -- a missing
# signpost looks exactly like a section meant to be read in full.
# 2026-10-19 (final): 88 -> 102. The exam-guide tripwire. 14 tests, almost all of
# them failure directions -- the mutants worth running are the ones that make an
# unreachable page or a missing link report as UNCHANGED, because a tripwire that
# passes silently is indistinguishable from one that found nothing wrong.
# 2026-10-19 (truly last): 102 -> 118. The claim-verification loop. Mutate inverted
# here too: the valuable mutants let `--offline` return 0, drop the exit-2 on a failed
# fetch, or classify a stitched quote as checkable so it fails forever.
# 2026-10-19 (the tiers): 118 -> 134. verify_claims grew three more tiers and the rule
# that their counts are never added together. Two more inverted mutants to watch: pooling
# the IDENTIFIER count into VERBATIM, and dropping the placeholder truncation so a
# templated path reports a rename that never happened.
EXPECTED_TESTS=134

PYTHON=".venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "No .venv found. Run:  uv venv --python 3.12 && uv pip install -e '.[test]'" >&2
  exit 2
fi

OUTPUT="$("$PYTHON" -m pytest -q "$@" 2>&1)" || {
  echo "$OUTPUT"
  echo
  echo "FAIL: the suite did not pass." >&2
  exit 1
}

echo "$OUTPUT"

# Parse the summary line. `grep -c` on PASSED would undercount by one on some pytest
# versions and -- more importantly -- the identical mistake on a SKIP count fails
# OPEN, reporting a clean run. So read the numbers pytest states rather than counting
# lines that look like passes.
PASSED="$(printf '%s' "$OUTPUT" | sed -n 's/^\([0-9]\{1,\}\) passed.*/\1/p' | tail -1)"
SKIPPED="$(printf '%s' "$OUTPUT" | grep -o '[0-9]\{1,\} skipped' | grep -o '^[0-9]\{1,\}' | tail -1 || true)"
SKIPPED="${SKIPPED:-0}"

if [[ "${PASSED:-0}" -lt "$EXPECTED_TESTS" ]]; then
  echo "FAIL: ${PASSED:-0} tests passed, expected at least ${EXPECTED_TESTS}." >&2
  echo "Tests disappeared rather than failed, which is the quieter problem." >&2
  exit 1
fi

if [[ "$SKIPPED" -ne 0 ]]; then
  echo "FAIL: ${SKIPPED} test(s) skipped. A skipped absence proof reads as a pass." >&2
  exit 1
fi

echo "OK: ${PASSED} passed, 0 skipped."
