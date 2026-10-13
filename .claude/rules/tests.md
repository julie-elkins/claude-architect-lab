---
paths:
  - "tests/**/*.py"
---

# Conventions for tests

- **Name the property, not the function.** `test_a_refusal_says_nothing_was_read` beats
  `test_read_material_error`. The test name is the only documentation anyone reads
  while a suite is failing.
- **Pin the positive direction alongside the negative one.** A bound tested only from
  above passes just as well if the comparison is inverted — and an inverted bound
  refuses everything, which looks like a strict tool rather than a broken one. See
  `test_a_file_at_exactly_the_limit_is_read`.
- **An absence proof needs the runner.** Tests here assert that an escape is refused,
  that nothing is read on a refusal, that no URL is fetched. Each passes trivially if
  it never runs, so use `./scripts/run-tests.sh` — it pins the collected count and
  fails on any skip. Raise the floor per episode, never per test.
- **Protocol tests must not touch real files.** Everything in `test_protocol.py` calls
  tools with inputs that fail their bounds check, so the file runs on a fresh clone with
  no fixtures. A protocol test depending on a real file passes on the author's machine
  and fails everywhere else.
- **Pass a subprocess its environment explicitly.** `StdioServerParameters(env=None)`
  does not inherit; the SDK drops `PYTHONPATH`, and the symptom is `Connection closed`
  with nothing pointing at the cause.
- **Pin the imperative, not the topic.** Asserting the server instructions "mention
  data" would pass on text that mentioned it and then told the caller to act on file
  contents anyway.
- **Derive surface checks from the live tool list**, never a hand-maintained list of
  tool names. A list is a second copy that stops matching the day a tool is added.
- Fixtures under `tests/fixtures/` are hand-written prose, which is a deliberate
  shortcut: nothing asserts they came from a generator. If that directory grows past a
  handful of files, add one.
