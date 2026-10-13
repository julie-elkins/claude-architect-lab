---
paths:
  - "src/course_doctor/server.py"
  - "src/course_doctor/contracts.py"
---

# Conventions for the MCP layer

These load only when the server or the output models are in play. That is the point of
a path-specific rule: instructions cost context, and API conventions loaded while you
are editing a test file are context spent on the wrong thing.

- **Every tool parameter needs a description saying what the WRONG value does to the
  output**, not what type it is. "The path, a string" clears a truthiness check and
  tells a caller nothing. There is a length floor in `tests/test_server.py`.
- **An array or object parameter must show one literal element of itself** in its
  description, for example `[{"stage": "cueing", "verdict": "pass"}]`. A composite
  renders as a nested schema an agent will not reliably read, and the failure is
  silent: the call refuses correctly and the refusal never names the shape.
- **Return a model, never `dict[str, Any]`.** A raw dict publishes an empty output
  schema, so a caller has to invoke the tool once to learn what comes back.
- **Optional output fields are explicitly nullable with an explicit default.** A field
  that is merely "sometimes absent" can be published as non-nullable while the server
  serialises `None` into it — and only the *served* path validates, so the in-process
  tests stay green while a real client breaks.
- **A refusal is a result with an `error` field.** Never raise across the tool
  boundary. Add the new code to the `Literal` in `contracts.Refusal` so it stays
  published rather than discovered.
- **Every refusal's `guidance` names the next action**, and says plainly when nothing
  was read. The specific misread to prevent is a failed call being recorded as a file
  that cited no documentation — a clean-looking zero.
- **`diagnostics.what_it_does_not_show` is required on the success path too.** A
  successful result silent about its own coverage is indistinguishable from a complete
  one.
- **`logging`, never `print`.** On stdio, stdout carries the protocol.
- **A new tool means `openWorldHint` needs a decision.** It is `false` while nothing
  fetches; the episode that adds the network changes it, and a test pins the current
  value so that is a deliberate edit rather than an oversight.
