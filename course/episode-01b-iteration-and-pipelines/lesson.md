# Lesson 3b — Working in increments, and running without a human

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
Covers **TS 3.5** (iterative refinement for progressive work) and **TS 3.6** (Claude
Code in CI/CD pipelines). Episode 1 covers TS 3.1 through 3.4; these two are the rest
of the domain.

Written lesson. Lab artifact: the Course Doctor scaffold gains a non-interactive run
and a stop condition.

## What you will be able to do afterwards

Split a task into increments an agent can be checked between, and run that agent in a
pipeline where nobody is watching — knowing in advance what ends the run.

## Why the exam cares

These two task statements are a third of Domain 3 and they are the two that look
least like configuration, which is why they get skipped.

They are also the two where a wrong answer is expensive rather than embarrassing. Plan
mode, from TS 3.4, is about the cost of a wrong *direction*. These are about the cost
of a wrong direction **nobody is there to notice** — which is a different question and
has a different answer.

Expect judgment items, not recall. "A pipeline runs an agent nightly against a
repository. Which configuration prevents an unbounded run?" has four defensible-looking
options and one correct one.

## Fundamentals

Skip what you know. Here so a newcomer has somewhere to go and a senior gets the
one-line refresh.

**Idempotence.** An operation you can run twice with the same result as running it
once. *Why it matters here:* an increment that is not idempotent cannot be safely
retried, and a pipeline's first instinct on failure is to retry. *Depth:* any
treatment of REST method semantics explains it cleanly.

**Checkpointing.** Saving a known-good state you can resume from or roll back to.
*Why it matters here:* it is what makes an increment a decision point rather than just
a smaller chunk of the same gamble. *Depth:* database transaction logs are the
canonical version.

**Non-interactive execution.** Running a program with no terminal attached, so there
is no one to answer a prompt. *Why it matters here:* a permission prompt in a pipeline
does not ask anybody anything — it blocks or fails, and the pipeline reports something
unhelpful. *Depth:* the distinction between a login shell and a batch job; `ssh
somehost command` versus `ssh somehost`.

**Exit codes.** A number a process returns to say whether it succeeded. Zero is
success; anything else is not. *Why it matters here:* a pipeline step's pass or fail is
this number and nothing else, so an agent that fails politely while returning zero
reports success. *Depth:* `man 3 exit`, and your CI system's documentation on step
failure.

**Stop conditions.** A stated rule for what ends a run — an iteration count, a budget,
a goal test, a timeout. *Why it matters here:* this is the central idea of both task
statements. An agentic loop without one does not stop because it is finished; it stops
because something external killed it. *Depth:* Domain 1 treats termination as its own
subject, and the exam guide's anti-patterns for it are published.

**Least astonishment in automation.** An unattended process should fail loudly rather
than succeed quietly. *Why it matters here:* the whole second half of this lesson.

## The idea, before any files

Two questions, and they are the same question asked at different scales.

**For iteration: what do I want to be able to see before the next step runs?** The
reason to work in increments is not that smaller is safer. It is that an increment
creates a *place to look* — a diff, a test result, a report — before the next decision
compounds on the last one. An increment nobody inspects is just a slower monolith.

So the unit is not "a small task." It is **one complete thing you can judge.** A
vertical slice that runs end to end beats a horizontal layer that cannot be evaluated
until the layer above it exists.

**For pipelines: what ends this run, and who finds out?** An unattended agent has
three properties or it should not run: you can see what it did, you can undo it, and
something stops it. Most pipeline failures in this area are the third one missing,
because the first two are easy to add and the third requires deciding a number.

And the sharp edge: **a run nobody watched that reported success is not evidence of
success.** It is evidence that nothing raised an error, which is also what a
no-op looks like.

## The build

### Part one — increments with a place to look

Take the Course Doctor work and slice it so each step is judgeable.

Wrong shape, and it is the tempting one:

```
1. Write all the output models
2. Write all the tools
3. Write all the tests
```

Nothing is runnable until step three. There is no place to look in between.

Right shape:

```
1. One tool, end to end, with its bounds and its test   -> runs, provable
2. Second tool, same                                    -> runs, provable
3. The coordinator that calls both                      -> runs, provable
```

Each increment is one complete path. After step one you can run the thing and read a
real result. That is the difference the task statement is about.

Make the checkpoint explicit, so the place to look is a command and not a habit:

```
./scripts/run-tests.sh && git add -p && git commit
```

Three verbs in order: prove, inspect, record. `git add -p` is the inspection — it puts
each hunk in front of you rather than staging whatever happens to be there.

### Part two — a run with no human in it

Non-interactive execution needs three things decided before it starts.

**One. Permissions must be settled in advance.** In a pipeline there is nobody to
approve a prompt. Every tool the run needs has to be permitted before the run, and
anything not permitted has to fail rather than wait.

**Two. A stop condition has to be stated.** Pick the one that matches what you are
afraid of: a wall-clock timeout if you fear a hang, an iteration cap if you fear a
loop, a budget if you fear cost. Write it into the invocation, not into a comment.

**Three. The exit code has to mean something.** Decide what makes the step fail — any
finding, or only an error? Both are defensible and they are different products. A
drift checker that fails the build on any stale citation is a gate; one that reports
and exits zero is a dashboard. Choose deliberately, because the pipeline cannot.

Then make the artifact outlive the run:

```
./scripts/run-tests.sh > ci-report.txt 2>&1; echo "exit=$?" >> ci-report.txt
```

Redirect both streams and record the exit code in the file. A log that omits the exit
code cannot distinguish a clean run from a crashed one after the fact, and the one time
you need it is the one time nobody was watching.

## Tips

Things that cost somebody an hour.

**A permission prompt in CI is not a prompt, it is a hang.** The run sits there until
the job times out, and the failure message names the timeout rather than the
permission. If a pipeline step mysteriously takes exactly as long as your CI timeout,
look for an unapproved tool before anything else.

**Redirect stderr or you will lose the only useful line.** `> log.txt` captures stdout
and leaves the traceback on a stream nobody saved. `2>&1` costs four characters and is
the difference between debugging a failure and re-running it blind.

**A crashed guard is invisible in a way a refusing guard is not.** A check that *blocks*
something leaves a record of the refusal. A check that *errors out* can let the action
through and write nothing at all — so a transcript with a broken guard looks identical
to one with no guard configured. Nothing passive tells you a guard is still armed; only
running a verifier does.

**Name the stop condition in the invocation, not the documentation.** A cap written in
a README is a cap nobody enforces. The question the exam asks is which configuration
prevents an unbounded run, and the answer is never "we agreed not to."

**A quiet report is not a clean run.** When an unattended run produces no findings, the
first thing to establish is whether it looked. An empty result and a run that never
started are the same output, and the second one is more common than people expect.

## The anti-pattern

The exam guide names anti-patterns for this domain explicitly, and the shape to
recognise here is:

> **An unattended run with no stated stop condition.**

Three forms, all of which look like working automation:

- **A cap in prose.** Agreed in a document, enforced by nothing.
- **A stop condition that is a side effect.** The run ends when the CI job times out,
  so the timeout *is* your stop condition — chosen by your CI provider's default rather
  than by you.
- **A success that means "no error raised."** The step exits zero, the dashboard is
  green, and nothing distinguishes a clean pass from a run that did no work.

And the related iteration anti-pattern:

> **Increments that cannot be evaluated individually.**

Slicing by layer rather than by path produces three steps where nothing is runnable
until the third. That is not iterative refinement. It is a monolith delivered in
instalments, and it fails the task statement for exactly the reason the exam cares
about: there was never a place to look.

## What this lesson does not cover

- **Loop termination as an architectural subject.** That is Domain 1, where the exam
  guide publishes two specific anti-patterns for it, and it is covered there.
- **A specific CI provider's syntax.** The task statement is about Claude Code in a
  pipeline, not about any one pipeline. The exit-code and stream-redirection ideas
  transfer; the YAML does not.
- **Cost figures.** No spend numbers appear here. Any figure would be from one
  person's usage on one set of tasks, and presenting it as a planning number would be
  worse than giving none.
- **Secrets handling in CI.** Adjacent and genuinely important; the env-var reference
  pattern in episode 1 is the part that belongs to this domain.
- **Whether your pipeline should run an agent at all.** Out of scope, and a fair
  question.

## Sources

- CCAR-F exam guide, Domain 3, **TS 3.5** (iterative refinement for progressive work)
  and **TS 3.6** (Claude Code in CI/CD pipelines) — both already recorded in
  `SOURCES.md` under Episode 1's claim table, EG §6.
- **Needs a documentation citation before publication**, consistent with the six items
  already listed as outstanding in `SOURCES.md`: the non-interactive invocation form,
  how permissions are supplied to a run with no terminal, and whether any stop-condition
  flag is a documented contract or incidental behaviour. Record URL and read date.
- Everything in the Tips section is **OBSERVED** rather than cited — measured behaviour
  on one version, which is a weaker claim than a documentation URL and is labelled as
  such, matching the convention already used in `SOURCES.md`.
