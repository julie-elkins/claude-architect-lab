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
EXPECTED_TESTS=56

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
