# Three-Part Learning Path

This is the learner-facing route through three existing public repositories. It is not a
fourth course and it does not copy their content. Each repository owns the material and
the runnable work it teaches.

The sequence moves from building agent systems, to checking whether an agent workflow is
safe to trust, to checking whether the evaluation itself supports the decision.

## Before you start

You need:

- a terminal;
- basic Python and Markdown familiarity;
- `uv`, the Python environment and package runner used by these projects; and
- no API credentials for the required path.

The required exercises are offline or synthetic. The optional judge stage in Part 3 is
the only step that can spend money, and it is not required for this learning path.

## Part 1 — Build the system

Repository: [Claude Architect Lab](https://github.com/julie-elkins/claude-architect-lab)

### Objective

Understand how agentic loops, tools, MCP (Model Context Protocol), configuration,
structured output, context management, and human escalation fit together in one working
system.

### Start

Read [GUIDE.md](GUIDE.md) from top to bottom. It is the whole 29-lesson course in
dependency order. Use [STUDY-PATH.md](STUDY-PATH.md) instead if you need a shorter
schedule.

Then run the local Course Doctor tests:

```bash
uv venv --python 3.12
uv pip install -e '.[test]'
./scripts/run-tests.sh
```

### Expected result

The course test script completes with all tests passing and no skipped tests. The
Course Doctor lab demonstrates that cited material, verified material, and material
requiring human review are different states.

### Checkpoint

Before continuing, explain:

- why a citation is not the same thing as verification;
- what the Course Doctor refuses to claim when it cannot fetch or match evidence; and
- why the lesson files are edited while `GUIDE.md` is generated.

### Limitation

This course teaches architecture and implementation judgment. Completing it does not
grant a certification or predict an exam score.

## Part 2 — Check the workflow

Repository: [Agent Assurance Harness](https://github.com/julie-elkins/agent-assurance-harness)

### Objective

Learn to distinguish transport success from task success and to require evidence before
an agent reports completion.

### Start

From the Agent Assurance Harness repository root, run:

```bash
uv run python examples/agent-workflow-teaching-lab/run_lab.py
```

### Expected result

The output shows:

- the naive path is `failed`;
- the guarded path is `completed`;
- both paths report transport status `ok`;
- the naive path retries three times and exceeds its synthetic ceilings; and
- the guarded path records a semantic outcome and escalates for human approval.

### Checkpoint

Explain:

- why an HTTP-success response is not enough to prove task success;
- what retry and cost ceilings protect against; and
- why the breaker must be independent of the component it evaluates.

### Limitation

This is an offline synthetic control. It does not establish live model quality,
production monitoring, or business impact.

## Part 3 — Check the measurement

Repository: [LLM Eval Validity](https://github.com/julie-elkins/llm-eval-validity)

### Objective

Learn to ask whether an evaluation measures what it claims to measure, rather than
accepting a green pass rate as sufficient evidence.

### Start

From the LLM Eval Validity repository root, run:

```bash
make analyse
```

This runs the offline analyses only. Do not run `make judge` for this path; that is the
optional model-judge stage and can incur provider cost.

### Expected result

The analyses complete from the checked-in fixture without network access or credentials.
The reports show why sample size, stratification, confidence bounds, rater agreement,
and evaluator repeatability can change a deployment decision.

### Checkpoint

Explain:

- why a point estimate can look safe while its confidence bound is not;
- why pooled results can hide a high-consequence failure family; and
- why an evaluation needs evidence about its own repeatability.

### Limitation

This study uses a fixed historical fixture and one human reference pass. It demonstrates
evaluation reasoning; it does not establish general model quality or production safety.

## Completion check

You have completed the path when you can:

1. describe the agent workflow you would build;
2. identify evidence that would make the workflow abstain or escalate; and
3. explain why the evaluation method itself may be too weak to support the decision.

Continue to the individual repositories when you want deeper implementation detail.
