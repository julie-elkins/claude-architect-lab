# What this exam sits on top of

Every lesson has a Fundamentals block covering the terms *that lesson* needs. This page is
the layer underneath all of them: the prerequisite stack, what the guide assumes you
already have, and a way to find out whether you have it before you spend a week.

**Read this first if you are not sure the course is pitched at you.** Read it last, or not
at all, if you build production systems for a living.

---

## The stack, for this exam specifically

```
                    measurement and calibration        Domain 5.5
                         LLM behaviour                 Domains 4, 5
                      distributed systems              Domain 1  (27%)
                software engineering + DevOps           assumed throughout
```

The guide's own statement of the floor: the ideal candidate *"typically has 6+ months of
practical experience building with Claude APIs, Agent SDK, Claude Code, and MCP,
understanding both the capabilities and limitations of large language models in production
environments."*

Note what that sentence does **not** say. It does not say machine learning.

---

## What is NOT a prerequisite, and this surprises people

If you came from a cloud or data certification track, the natural assumption is a ladder:
developer knowledge → DevOps → data engineering → machine learning → AI. That ladder is
real, and **it is not this exam's.**

The guide's appendix (§17) puts all of the following **explicitly out of scope**:

- Fine-tuning Claude models or training custom models
- Embedding models or vector database implementation details
- Constitutional AI, RLHF, or safety training methodologies
- Claude's internal architecture, training process, or model weights
- Performance benchmarking or model comparison metrics
- Token counting algorithms or tokenization specifics

**So the ML layer is not underneath this exam.** You do not need to know how a model is
trained, how embeddings work, or how tokenisation is implemented. You need to know how a
model *behaves* in production — which is a different subject with a different literature.

See [SCOPE.md](SCOPE.md) for the full out-of-scope list. It is the cheapest page in this
repository.

---

## Layer 1 — software engineering and DevOps

Assumed everywhere and never taught. If any of these is unfamiliar, start here rather than
with lesson 3.1.

| You need | Because | Where it bites |
|---|---|---|
| Reading and writing code in at least one language | Tools, schemas and hooks are code | all of Domain 2 |
| JSON, and YAML frontmatter | Every config file and every schema | [3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) · [3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) · [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) |
| Shell and CLI basics — flags, pipes, stdin and stdout, exit codes | `-p`, `--output-format`, `2>&1`, what a non-zero exit means | [3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| Glob patterns | `paths` scoping, file selection | [3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) · [2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md) |
| Git, and version control hygiene | What is committed versus local, and why a secret in a committed file is published | [3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) · [2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) |
| Environment variables | How a credential reaches a server without being written down | [2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) |
| CI/CD concepts — a pipeline, a step, a gate, a timeout | TS 3.6 is literally this | [3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| Least privilege | Half of Domain 2 and all of the hook material | [2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) · [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |

**If you are weak here**, the honest advice is that this is not the exam to study for yet.
It assumes six months of building, and the blueprint is written for someone who has made
these mistakes already.

---

## Layer 2 — distributed systems

**The missing layer, and the one that explains why Domain 1 is 27%.** Multi-agent
orchestration is a distributed system: independent components, partial failure, no shared
memory, coordination overhead. Every classic problem shows up with a new name.

| Classic concept | Appears as | Lesson |
|---|---|---|
| No shared memory between processes | Subagents inherit nothing; context must be passed explicitly | [1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) |
| Hub-and-spoke topology | The coordinator pattern, and why workers never talk to each other | [1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) |
| Partial failure | Some workers succeed and some do not, and the join must say which | [5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) |
| Idempotence | Whether a retry is safe, and whether a resumed tool already took effect | [4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) · [1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) |
| Timeouts and bounded work | `max_turns`, `max_budget_usd`, and stop conditions | [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) |
| Map-reduce / fan-out and join | Parallel subagents, then synthesis | [1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) · [1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md) |
| Error context propagation | Failure type, what was attempted, partial results, alternatives | [5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) |
| Crash recovery and state export | Manifests, scratchpads, resuming at the first gap | [5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) |
| Middleware / interception | Hooks on tool calls | [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |

**If you have operated a distributed system, Domain 1 will feel familiar and you will still
need the specifics** — which tool spawns a worker, what a background subagent loses, where
a budget cap overshoots.

**If you have not**, read Domain 1's lessons twice, and read them for the *shapes* rather
than the API names. The exam is judgment-weighted, and the judgment is distributed-systems
judgment.

---

## Layer 3 — how a model behaves in production

Not how one is built. How one behaves, which is the thing the guide actually asks for.

| You need to know | Lesson |
|---|---|
| A context window is finite, accumulates, and does not reset between turns | [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) · [5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) |
| Output is non-deterministic, so an instruction has a failure rate | [1.4](course/domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md) · [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |
| Models can produce confident wrong content, and fluency is not accuracy | [4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) · [5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) |
| Position in a long input affects what gets used | [5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) |
| Examples teach more reliably than descriptions | [4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) |
| A model asked to review its own work inherits its own assumptions | [4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md) |

**Prompt caching is on the boundary**: the guide says it is out of scope *"beyond knowing it
exists."* Know the term. Stop there.

---

## Layer 4 — measurement

One task statement, and it rests on a discipline nothing else in the exam touches.

Needed for [5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md):

- **Aggregate versus segmented metrics** — why one number hides a population. The formal
  version is Simpson's paradox.
- **Stratified random sampling** — sampling *within* strata so a rare segment is actually
  represented.
- **Calibration** — whether a stated confidence matches observed accuracy, measured against
  labelled data.
- **Denominators** — why a rate without its n is not a claim.

This layer also explains the exam's own scoring, which is worth reading once in
[EXAM-DAY.md](EXAM-DAY.md): criterion-referenced, with a cut score set by a formal
standard-setting study, and scaled to equate across forms.

---

## A readiness check

Answer these before committing a week. Each maps to a layer, and a "no" tells you where to
start rather than whether to give up.

1. Can you explain the difference between a non-zero exit code and a program that printed
   an error? *(layer 1)*
2. Can you say what a glob pattern matches, including what `**` adds? *(layer 1)*
3. Can you explain why a retry is safe for one operation and unsafe for another?
   *(layer 2)*
4. Given five workers where one fails, can you name three defensible things the coordinator
   could do? *(layer 2)*
5. Can you say why an instruction in a config file is not a guarantee? *(layer 3 — and it
   is [theme 1](THEMES.md))*
6. Can you say what "97% accurate" does not tell you? *(layer 4)*

**Four or more yes:** start with [STUDY-PATH.md](STUDY-PATH.md).

**Two or three:** read this course and expect Domain 1 to be the hard part. Budget the
extra day the study path already allows for it.

**Fewer than two:** the guide's six-months-of-building floor is doing real work. Build
something with the Agent SDK and MCP first; the exam tests judgment you acquire by making
these mistakes, and no course substitutes for that.

---

## Where to learn each layer

Deliberately short, and deliberately not a link farm.

- **Layer 1** — your language's own documentation, `man` pages for shell semantics, and
  `git`'s book. There is no shortcut and no need for one.
- **Layer 2** — any distributed systems text covers partial failure, idempotence and
  coordination better than any AI material does. The concepts transfer intact; only the
  names change.
- **Layer 3** — Anthropic's own [Claude Academy](https://academy.claude.com/) courses on AI
  fluency and on capabilities and limitations are the right level for this layer, and they
  are free. They are not exam preparation and do not claim to be.
- **Layer 4** — standard sampling and measurement material. Calibration curves and
  stratified sampling are old, well-documented ideas.

## Other people's material

Named because leaving it out would be the more dishonest choice in a course about material
going stale. Not affiliated with this course, and has not reviewed it.

- **Matthew Purcell's consolidated prep list**, on LinkedIn at
  [linkedin.com/in/purcellmatthew](https://www.linkedin.com/in/purcellmatthew/) — free
  practice question sets for all four Claude certifications, a CCAR-F quick reference, and a
  written review of the exams. It is the most used community material for these exams by a
  wide margin, and it is the thing to read if what you want is **practice questions**, which
  [SCOPE.md](SCOPE.md) explains this course will never contain.

**Only one entry, and that is deliberate.** There is plenty of other free Claude and agent
material, some of it good. It is not listed here because **I have not worked through it**,
and a recommendation from someone who has not read the thing is worth exactly nothing —
which is the same standard this course applies to its own claims. If you have found
something that earned its place, tell me and I will read it before naming it.

**What this course does that the list above does not:** one task statement per lesson
against the published blueprint, a lab you build and run, and a claim table that says where
every factual statement came from and when it was read. That is the whole pitch, and it is
only worth anything if the sourcing claim is true — which is what
[VERIFICATION.md](VERIFICATION.md) tracks and keeps honest about the parts not yet done.

## Sources

The prerequisite layers and the readiness check are the author's, drawn from writing all 29
lessons. They are not in the exam guide.

What *is* from the guide: the audience statement and the six-months floor (§2), and every
out-of-scope item quoted above (§17). The claim that the ML layer is not a prerequisite is
an inference from §17's exclusions, and it is stated as one.
