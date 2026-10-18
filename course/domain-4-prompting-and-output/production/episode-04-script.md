> **⚠ The written lessons are authoritative, not this script.** This was written
> 2026-10-18, after the documentation verification pass of the same date, so it does not
> lag the lessons today. It will. There is no automated check for script-versus-lesson
> drift — a diff cannot tell a legitimate rewording from a stale claim — so **re-read the
> lesson for each task statement below and reconcile before recording.**
>
> **This is a production asset, not the lesson.** It is the narration script for the video
> version: spoken wording, screen directions, and a recording checklist.
>
> **If you are here to learn, read the written lessons instead.**
> [The course front page](../../../README.md) lists all twenty-nine. This script covers
> task statements 4.1 through 4.6:
> [4.1](../lesson-4-1-explicit-criteria.md) ·
> [4.2](../lesson-4-2-few-shot.md) ·
> [4.3](../lesson-4-3-structured-output.md) ·
> [4.4](../lesson-4-4-validation-and-retry.md) ·
> [4.5](../lesson-4-5-batch-processing.md) ·
> [4.6](../lesson-4-6-multi-instance-review.md)

# Episode 4 — Wording strength is not a mechanism

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
Target runtime 10–11 minutes · ~1,600 spoken words
Ships: Course Doctor's extraction contract — a schema, a validation-retry loop, and an
independent reviewer

**Runtime is proportional to blueprint weight** — 20% here, which is what allows all six
task statements rather than four.

---

## Before you record

- Clean recording profile, per the recording checklist kept outside this repo.
- **Start from episode 3's commit.**
- **The batch segment cannot be demonstrated in real time.** A 24-hour window does not fit
  in an episode. Show the submission and a previously-completed result, and **say that is
  what you are doing** — do not cut between them in a way that implies one run.
- **Three claims in this episode are the guide's, not measurements.** That general
  instructions fail to improve precision, that few-shot is the most effective technique for
  consistency, and that a model retains reasoning context from generation. Attribute all
  three out loud.
- The multi-instance segment is the one place this course demonstrates its own method on
  itself. Worth saying so — see the note in the script.

---

## Fundamentals

Not spoken on camera. For the written lesson and the episode description.

**Precision and recall.** Precision is what fraction of the things you flagged were real;
recall is what fraction of the real things you found. *Why it matters here:* task statement
4.1 is a precision problem, and tightening precision usually costs recall. *Depth:* any
introductory statistics or information-retrieval treatment.

**False positive.** Something flagged that should not have been. *Why it matters here:* it
is the named target of 4.1, and one noisy category makes a whole report ignorable. *Depth:*
lesson 5.5, where measuring it properly is the subject.

**Few-shot prompting.** Giving a model a small number of worked examples rather than only
instructions. *Why it matters here:* the guide calls it the most effective technique for
consistency. *Depth:* the prompt engineering documentation.

**JSON Schema.** A declarative description of what a JSON document may contain. *Why it
matters here:* it is the enforcement mechanism in 4.3. *Depth:* `json-schema.org`.

**Constrained decoding.** Restricting token generation so output cannot leave the grammar.
*Why it matters here:* it is *why* a strict schema cannot be violated, and also why
optional fields cost something. *Depth:* the structured outputs documentation.

**Syntactic versus semantic error.** Malformed against well-formed-but-wrong. *Why it
matters here:* this distinction is the whole of 4.3's examinable half. *Depth:* the same
distinction in compilers — a program that parses and does the wrong thing.

**Idempotence and retries.** Whether repeating an operation is safe, and whether repeating
it can help. *Why it matters here:* 4.4's judgment is *whether* to retry, not how.
*Depth:* REST semantics.

---

## Script

```
"Be more careful" is not an engineering change.

[screen: the blueprint table, Domain 4 highlighted]

Domain 4 is twenty percent of the exam, and it has one thesis running through all
six task statements: wording strength is not a mechanism.

Every task statement here gives you a pair — a tempting option that makes the
instruction firmer, and a correct option that changes the structure. Once you see
the pattern you can answer most of this domain from it.

[screen: the six task statements]

Six task statements. All six today.

[screen: two instructions side by side]

Four point one. Criteria.

The guide names the failing instruction by quoting it. "Be conservative." "Only
report high-confidence findings." It says those fail to improve precision compared
to specific categorical criteria.

That is a strong claim, stated plainly. And it matters because confidence-based
filtering feels like a tightening and changes nothing measurable. "High
confidence" is not a property the model can calibrate on request. It's a word.

[screen: the contrast, quoted]

Here is the guide's own contrast. Weak: "check that comments are accurate."
Strong: "flag comments only when claimed behaviour contradicts actual code
behaviour."

The first is a hope. The second is a test — you can apply it and get the same
answer twice.

So if your fix to a precision problem is an adverb, it isn't a fix.

And write the skip list, not just the report list. The skip list is as important
and about half as likely to get written.

[screen: three examples in a prompt]

Four point two. Examples.

The guide's claim is unqualified: few-shot examples are the most effective
technique for consistently formatted, actionable output when detailed instructions
alone produce inconsistent results.

Read that next to four point one and you have the domain's thesis in two halves.
When the criterion is vague, define it. When the criterion is fine and the output
is still inconsistent, examples beat more instruction.

Neither one is fixed by stronger wording.

[screen: an ambiguous-case example]

And the guide is specific about which examples. Ones that demonstrate
ambiguous-case handling, and that let the model generalise to novel patterns
rather than matching only the cases you listed.

That is the difference between two examples and three. Two examples teach
matching. The third teaches generalising.

The number the guide gives is two to four targeted examples. Not twenty.

And put the reasoning inside the example. An example that shows the verdict
teaches the format. One that shows why teaches the judgment.

[screen: a strict schema]

Four point three. Structured output.

The guide's position: tool use with JSON schemas is the most reliable approach for
guaranteed schema-compliant output, eliminating JSON syntax errors.

And then it immediately names the limit, which is the more examinable half.
Strict schemas eliminate syntax errors. They do not prevent semantic errors.

[screen: a valid document with wrong numbers]

So: line items that don't sum to the total. Values in the wrong fields. A
perfectly valid document that is wrong.

That's the lesson. Treating schema compliance as correctness is the named
anti-pattern — and it is a seductive one, because structure reads as rigour. A
schema-valid document looks more trustworthy than prose, and it has no more claim
to being right.

The cheapest guard is the guide's own: put a calculated total next to the stated
total and compare them.

[screen: stop_reason]

Two mechanics worth knowing. Check stop_reason before you parse, because on a
refusal or a truncation, output that doesn't match the schema is documented
behaviour, not a bug. And compare enum values case-insensitively — the docs say
capitalisation may differ, typically on the first letter after a space.

One design note. The guide says make fields optional when the source may not
contain the information, so the model isn't pressured into inventing a value. The
API documentation says the opposite — reduce optional parameters.

Both are right about different things, and the reconciliation is the guide's own
other objective: make the field required and give it an explicit "not present"
member. An enum with "unclear" in it. The model must answer, and "unclear" is an
answer you can count.

[screen: three identical failed retries]

Four point four. Retries.

Here is the thing people get wrong, and the guide states it directly: retries are
ineffective when the required information is simply absent from the source.

Format errors respond to a retry. Structural errors respond to a retry. A missing
fact does not. Three attempts at extracting a figure that is not in the document
produce three failures and a bill.

So the examinable judgment is not how to retry. It's whether.

[screen: a retry with validation errors appended]

And when a retry is worth doing, the guide names what makes it worth anything:
retry with error feedback. Append the specific validation errors to the prompt, so
the second attempt is informed rather than just repeated.

A retry without the previous output and its errors is not a correction. It's a
re-roll.

One more line that saves you: say "change nothing else." Otherwise the retry
rewrites the parts that already worked.

[screen: the batch API]

Four point five. Batch processing.

Three numbers and one prohibition, and they are the whole decision. Fifty percent
cost saving. Up to a twenty-four hour window. No guaranteed latency.

Which makes this mechanical. Blocking workflows cannot use it — the guide's
example is a pre-merge check, and the failure is definitional. A gate that might
answer tomorrow is not a gate.

Non-blocking, latency-tolerant work should. Overnight reports. Weekly audits.
Half price for work nobody is waiting on.

[screen: the cadence arithmetic]

And there's a second-order skill here that is unusually concrete, which means it's
answerable: calculating submission frequency from an SLA.

The guide's worked figure — four-hour submission windows to guarantee a thirty-hour
SLA against twenty-four-hour processing. Twenty-four plus four is twenty-eight,
which fits inside thirty with margin.

That's arithmetic you can be asked to do. Pick a cadence by feel and you meet the
SLA until the first slow day.

Two practical things: make your custom_id self-describing rather than sequential,
because you will be reading it in a failure report. And when some requests fail,
resubmit the failed IDs with a modification — not the whole batch.

[screen: two instances]

Four point six. Review.

The guide gives a mechanism rather than an opinion, and the mechanism is worth
being able to state: a model retains reasoning context from generation, which
makes it less likely to question its own decisions in the same session.

That's not "models are overconfident." It's specific. The reasoning that produced
the output is still there, so a review in that session inherits the assumptions
instead of testing them.

And it ranks the alternatives explicitly. Independent review instances, without
prior reasoning context, catch subtle issues better than self-review instructions
or extended thinking.

Both of those are the tempting options. Both are named as weaker.

[screen: this repo's VERIFICATION.md]

I'll be honest about something here, because this is the one place the course
demonstrates its own subject on itself.

The claims in these lessons were written by an agent, and they were checked by the
same agent. That is exactly the configuration this task statement says is weakest.
The partial defence I used was to demand the documentation's verbatim wording back
rather than a judgment — so the page's own words had to appear, not an opinion
about them. That is weaker than independent review and stronger than
self-assessment, and it's written down in VERIFICATION.md with what it still
cannot tell you.

"Review your own output carefully" is an instruction to the one party that cannot.

[screen: the anti-pattern slide]

The anti-patterns for this domain.

"Be conservative" and "only report high-confidence findings" as precision fixes.
Confidence-based filtering instead of a defined report-versus-skip list. Detailed
instructions where examples are needed. Examples that only cover the cases you
listed. Treating schema compliance as correctness. Required fields where the
source may not have the information. Retrying when the fact is absent. A retry
without the validation errors appended. Batch processing a blocking workflow.
Resubmitting a whole batch to recover failures. And self-review in the generating
session.

Look at how many are the firmer-wording option. That's the domain in one
observation: when one choice rewrites the instruction and another changes the
structure, the structure wins.

[screen: the contract, tests passing]

That's the extraction contract, and it runs.

Last episode: Domain 5. Context management and reliability — and the task
statement that decides whether anything else in this exam was real.

Everything in this course is sourced from the published exam guide or the public
documentation, and every claim is traced in SOURCES.md. Content verification state
is in VERIFICATION.md, including what has not been checked. Nothing here comes
from sitting the exam.

Repo link is below.
```

---

## Tips

Not spoken on camera — for the written lesson and the episode notes.

**If your fix to a precision problem is an adverb, it is not a fix.** This is the single
most portable sentence in the domain.

**One noisy category poisons the accurate ones.** The guide's remedy is to disable a
high-false-positive category temporarily rather than leaving it on while you improve it —
because people stop reading the whole report, not just that section.

**A skip list is as important as a report list, and half as likely to get written.**

**Two examples teach matching; the third teaches generalising.** If output is still rigidly
copying your examples, you have too few, not too many.

**Put the reasoning inside the example.** An example showing the verdict teaches format; one
showing why teaches judgment.

**An example demonstrating an "I don't know" output is the highest-value pair you can
write**, because it is the case the model is least willing to produce unprompted.

**A schema-valid document can be completely wrong, and it looks more trustworthy than
prose.** Structure reads as rigour.

**Check `stop_reason` before parsing.** On a refusal or a truncation the payload will not
match your schema, and your parser's error will point at the schema rather than the reason.

**The structured-output limits are per request, not per tool.** Adding a twelfth strict tool
can break a request by pushing a combined total over 24 optional parameters or 16
union-typed ones — and the error arrives while you are editing something unrelated.

**A required field with an `unclear` member beats an optional field.** The model must take a
position, and "unclear" is a position you can count. An absent field is indistinguishable
from one the model forgot.

**Retrying an absent fact is the most expensive no-op available**, and it looks like
diligence in the logs.

**Say "change nothing else" or the retry will rewrite the parts that worked.**

**Extract the evidence, not the conclusion.** A quoted span can be checked by a human; a
verdict cannot.

**Make `custom_id` self-describing, not sequential.** You will read it in a failure report,
and `item-0041` tells you nothing.

**The 24 hours is a ceiling, not an estimate**, and expiry is more likely exactly when you
are busiest.

**Test the prompt on fifty before you send fifty thousand.** Half price on a bad prompt is
not a saving.

**Use a fresh subagent, not a fork, for the reviewer.** A fork inherits the conversation,
which is precisely the reasoning context that makes self-review weak.

**Ask the reviewer what the author did not check.** It is a better question than "is this
correct" and it surfaces the gaps rather than re-litigating the claims.

**Confidence routes; it does not filter.** Dropping low-confidence findings hides them;
routing them to review surfaces them.

---

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, nothing in the window title or
      tab bar.
- [ ] **No API key visible in any frame**, including scrollback.
- [ ] The batch segment makes clear that submission and result are two separate runs. If the
      cut implies one continuous run, re-edit.
- [ ] All three guide claims — precision, few-shot effectiveness, retained reasoning context
      — are attributed on screen, not stated as measured here.
- [ ] The cadence arithmetic is shown worked, not asserted. 24 + 4 = 28, inside 30.
- [ ] The self-review admission is kept. It is the most credible thirty seconds in the
      series and cutting it for time would be the wrong call.
- [ ] Clean clone at this episode's commit reproduces the contract and the tests.
- [ ] Description carries the repo link with the `julie-elkins` handle.
