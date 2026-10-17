# Lesson 4.3 — A schema you cannot violate, and the errors it still lets through

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.3:** Enforce structured output using tool use and JSON schemas.

Lab artifact: Course Doctor's findings guaranteed parseable, with the fields that may
legitimately be absent handled so the model cannot invent them.

## What you will be able to do afterwards

Guarantee that output parses, say exactly which class of error that does **not** prevent,
and design the optional-field question deliberately — because the exam guide and the
current API documentation give opposite advice about it, for good reasons on both sides.

## Why the exam cares

The guide's position is clear: **tool use with JSON schemas is the most reliable approach
for guaranteed schema-compliant structured output, eliminating JSON syntax errors.**

And it immediately names the limit, which is the more examinable half: **strict schemas
eliminate syntax errors but do not prevent semantic errors** — line items that do not sum
to the total, values in the wrong fields. A valid document that is wrong.

That distinction is the lesson. Everything else is mechanics.

## Fundamentals

**JSON Schema.** A machine-readable description of what a document must contain. *Why it
matters here:* it is the contract. *Depth:* `json-schema.org`.

**Syntactic versus semantic validity.** Well-formed against actually correct. *Why it
matters here:* schemas guarantee the first and say nothing about the second. *Depth:* the
distinction is the same one in compilers — a program that parses and does the wrong thing.

**Constrained decoding.** Restricting token generation so output cannot leave the grammar.
*Why it matters here:* it is how the current API enforces schemas, and it is stronger than
validate-then-retry. *Depth:* the structured outputs documentation.

**Nullable versus required.** Whether a field may be absent. *Why it matters here:* the
tension at the heart of this lesson. *Depth:* the build.

**Enum with an escape hatch.** A closed set plus an explicit "none of these" member. *Why
it matters here:* it is the reconciliation of that tension. *Depth:* the guide's own
`"unclear"` and `"other" + detail` patterns.

## The idea, before any schema

**Decide what must be guaranteed, then pick the mechanism that guarantees it.**

The guide's mechanism is a tool whose input schema *is* your output shape: define an
extraction tool, let the model call it, read the structured data out of the call rather
than parsing prose. `tool_choice` then controls whether it *must* call — lesson 2.3 covers
the three settings, and `"auto"` is the one that lets it answer in text instead.

**Then accept what the guarantee does not cover.** A schema cannot tell you the extracted
total is wrong, that two fields were swapped, or that a confident value was invented. The
guide's answer is to **build the check into the schema**: extract `calculated_total`
*alongside* `stated_total` so a mismatch is visible, and add a `conflict_detected` boolean
for inconsistent sources. You are not validating the model; you are asking it to surface
the evidence that would reveal its own error.

## The build

### Step 1 — the schema as a tool's input

```json
{
  "name": "write_finding",
  "description": "Record one verification finding for one claim in one lesson.",
  "input_schema": {
    "type": "object",
    "properties": {
      "claim": {"type": "string"},
      "source_url": {"type": "string"},
      "verdict": {
        "type": "string",
        "enum": ["supported", "contradicted", "not_in_docs", "not_checked", "unclear"]
      },
      "quoted_support": {"type": "string"},
      "conflict_detected": {"type": "boolean"}
    },
    "required": ["claim", "source_url", "verdict", "conflict_detected"]
  }
}
```

Two deliberate choices. `verdict` is an enum with `unclear` in it — the guide's named
pattern for ambiguous cases. And `conflict_detected` is required, so the model must state
a position rather than omit the field when the answer is awkward.

### Step 2 — force the call when text would not do

Under `tool_choice: "auto"` the model may answer in prose instead. If you need structure,
`"any"` guarantees a tool call; a named tool guarantees *which*. The guide's own case is
`"any"` when several extraction schemas exist and the document type is unknown.

### Step 3 — the optional-field question, and the genuine disagreement

**The exam guide says:** design fields as optional or nullable when source documents may
not contain the information, *"preventing the model from fabricating values to satisfy
required fields."*

**The current API documentation says the opposite:** *"Reduce optional parameters. Make
parameters `required` where possible."* Its reason is mechanical — *"each optional
parameter roughly doubles a portion of the grammar's state space"* — and there are hard
limits: **24 optional parameters total across all strict schemas, 16 with union types.**

Both are right about different things. The guide is preventing a hallucinated value; the
documentation is managing constrained-decoding complexity. **The reconciliation is the
guide's own other objective:** make the field required and give it an explicit
"not present" member — an enum with `unclear`, or a nullable type stated once rather than
a parade of optional fields. The model then *must* answer, and `unclear` is an answer.

For the exam, answer the guide. For a real schema, prefer required fields with explicit
absent-values and keep your optional count well under the limit.

### Step 4 — know where the guarantee stops

Even under constrained decoding the documentation names three cases where output **may not
match your schema**:

- **A refusal.** `stop_reason: "refusal"` — safety takes precedence over the schema.
- **Truncation.** `stop_reason: "max_tokens"` — the output is incomplete.
- **Enum capitalisation.** A returned value *"may differ from your schema only in
  capitalisation, typically in the first letter of a word following a space."*

So: check `stop_reason` before trusting the payload, and compare enums
case-insensitively. Two lines of code, and without them the guarantee has three holes.

## Tips

Things that cost somebody an hour.

**A schema-valid document can be completely wrong, and it looks more trustworthy than
prose.** That is the actual risk here: structure reads as rigour. The guide's
`calculated_total` beside `stated_total` is the cheapest guard there is.

**Compare enum values case-insensitively.** The documentation says capitalisation may
differ, typically on the first letter after a space. A strict string comparison will fail
on a response that is otherwise exactly right.

**Check `stop_reason` before parsing.** On a refusal or a `max_tokens` truncation the
payload will not match your schema, and your parser's error will point at the schema
rather than at the reason.

**Every optional parameter you add has a cost you cannot see.** It roughly doubles part of
the grammar's state space, and there is a hard ceiling of 24. A schema that compiles
slowly or errors is usually a schema with too many optionals.

**A required field with an `unclear` member beats an optional field.** The model must take
a position, and "unclear" is a position you can count. An absent field is indistinguishable
from a field the model forgot.

## The anti-pattern

From the guide's objectives:

> **Treating schema compliance as correctness.** Strict schemas eliminate syntax errors
> and do not prevent semantic ones — values that do not sum, fields transposed.

> **Required fields where the source may not contain the information**, which pressures
> the model to fabricate a value to satisfy the schema.

And the one the documentation adds:

> **Trusting the payload without checking `stop_reason`.** On a refusal or a truncation,
> output that does not match the schema is the documented behaviour, not a bug.

## What this lesson does not cover

- **`tool_choice` in depth** — lesson 2.3 covers all three settings.
- **Validation and retry loops** — TS 4.4, which is what you do when the semantic check
  fails.
- **Few-shot examples** — TS 4.2, often the better fix for inconsistent *content* where a
  schema fixes inconsistent *shape*.
- **Batch processing** — TS 4.5.
- **The newer dedicated structured-outputs feature** (`output_config.format` and
  `strict: true` on a tool) beyond the facts above. The exam guide describes the
  tool-use-plus-schema approach; the current API has a stronger constrained-decoding
  mechanism. Both are noted; the exam tests the former.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.3.

| Claim | Source |
|---|---|
| Tool use with JSON schemas is the most reliable approach for guaranteed schema-compliant output, eliminating JSON syntax errors | EG §6, TS 4.3 |
| `tool_choice: "auto"` may return text instead of calling a tool; `"any"` must call one but chooses which; a named tool forces that tool | EG §6, TS 4.3 |
| Strict JSON schemas eliminate syntax errors but do not prevent semantic errors, e.g. line items that do not sum to a total, values in wrong fields | EG §6, TS 4.3 |
| Schema design: required versus optional fields, enum fields with `"other"` plus a detail string for extensible categories | EG §6, TS 4.3 |
| Setting `tool_choice: "any"` to guarantee structured output when multiple extraction schemas exist and the document type is unknown | EG §6, TS 4.3 |
| Designing schema fields as optional or nullable when source documents may not contain the information, preventing fabricated values | EG §6, TS 4.3 |
| Adding enum values like `"unclear"` for ambiguous cases and `"other"` plus detail fields for extensible categorisation | EG §6, TS 4.3 |
| Extracting `calculated_total` alongside `stated_total` to flag discrepancies, and a `conflict_detected` boolean for inconsistent source data | EG §6, TS 4.4 |
| Structured outputs enforce schemas by constrained decoding: "Always valid… Type safe… no retries needed for schema violations" | [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), read 2026-10-17 |
| **"Reduce optional parameters. Make parameters `required` where possible."** and "each optional parameter roughly doubles a portion of the grammar's state space" | [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), read 2026-10-17 |
| Hard limits: 24 optional parameters total across strict schemas, 16 parameters with union types | [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), read 2026-10-17 |
| Required properties appear first, followed by optional properties, regardless of schema order | [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), read 2026-10-17 |
| Output may not match the schema on a refusal (`stop_reason: "refusal"`), on truncation (`stop_reason: "max_tokens"`), or in enum capitalisation — which "may differ from your schema only in capitalisation, typically in the first letter of a word following a space" | [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), read 2026-10-17 |

**Noted tension, stated rather than resolved:**

- The exam guide advises optional/nullable fields to prevent fabrication. The current API
  documentation advises minimising optional parameters for grammar complexity. They
  optimise different things; the reconciliation offered in this lesson — a required field
  with an explicit absent-value member — is the author's, not either source's.
