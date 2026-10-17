# The six scenarios, and which lessons each one needs

The exam presents **four scenarios, drawn at random from a published bank of six.** Every
question sits inside one of them. So the exam does not ask you about task statements — it
drops you into a production context and asks which of four defensible choices is right
*there*.

This page is the other index of the course. The [README](README.md) lists lessons by task
statement, which is how the blueprint is organised. This lists them by scenario, which is
how the exam is organised.

**All six scenarios are published in the exam guide, §5.** Their text and their primary
domains are Anthropic's, not reconstructed from anywhere — and nothing on this page comes
from sitting the exam. See [SOURCES.md](SOURCES.md) for why that boundary is the reason
this course can be trusted.

## How to use this

Pick a scenario. Read its lessons. Then ask yourself the question in its last column
before you look at anything else — that question is the one the scenario exists to test.

Four of these six will be in front of you. You do not get to choose which, so the honest
preparation is all six.

---

## Scenario 1 — Customer Support Resolution Agent

A support agent built on the Agent SDK, handling high-ambiguity requests — returns,
billing disputes, account issues — reaching backend systems through custom MCP tools
(`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). The target is
80%+ first-contact resolution **while knowing when to escalate.**

**Primary domains:** Agentic Architecture & Orchestration · Tool Design & MCP Integration ·
Context Management & Reliability

| Read | Why this scenario needs it |
|---|---|
| [lesson 1.4](course/domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md) | The refund gate. `process_refund` must not run until `get_customer` has **returned** a verified id, and the handoff goes to a human with no transcript |
| [lesson 5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md) | "Knowing when to escalate" is the scenario's own phrase. Sentiment and confidence are both ruled out as triggers |
| [lesson 5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) | A long support conversation is where a summary eats the amount and the order number |
| [lesson 2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) | Four error categories, and a business refusal the agent has to say out loud |
| [lesson 1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) | The loop underneath all of it |

**The question to ask yourself:** the customer is angry and the fix is one tool call away.
What do you do, and what changes if they ask for a person?

---

## Scenario 2 — Code Generation with Claude Code

A team using Claude Code for generation, refactoring, debugging and documentation,
integrating it into a development workflow with **custom slash commands, CLAUDE.md
configurations, and knowing when to use plan mode versus direct execution.**

**Primary domains:** Claude Code Configuration & Workflows · Context Management &
Reliability

| Read | Why this scenario needs it |
|---|---|
| [lesson 3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) | The hierarchy, and that a CLAUDE.md is context rather than a control |
| [lesson 3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) | The scenario names custom slash commands directly |
| [lesson 3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) | Conventions that must apply to files spread by type |
| [lesson 3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) | "When to use plan mode vs direct execution" is the scenario's own wording |
| [lesson 3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) | Iterating with artifacts rather than adjectives |
| [lesson 5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) | Long refactors are where a session starts talking about typical patterns |

**The question to ask yourself:** a rule applies and you cannot find where it came from.
Where do you look, in what order?

---

## Scenario 3 — Multi-Agent Research System

A coordinator delegating to specialised subagents — one searches the web, one analyses
documents, one synthesises findings, one generates reports — producing comprehensive,
**cited** reports.

**Primary domains:** Agentic Architecture & Orchestration · Tool Design & MCP Integration ·
Context Management & Reliability

| Read | Why this scenario needs it |
|---|---|
| [lesson 1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) | Hub-and-spoke, dynamic routing, and the over-narrow decomposition trap |
| [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) | Workers inherit nothing, so the coordinator passes findings not references |
| [lesson 5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) | One unreachable source must not become a clean report or a dead workflow |
| [lesson 1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md) | Fixed pipeline or adaptive plan, and per-item plus integration passes |
| [lesson 5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) | "Cited" is the hard word here — attribution has to survive the handoffs |
| [lesson 2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) | A synthesis agent holding a web search tool will use it |

**The question to ask yourself:** your synthesis reads complete and three subtopics were
never searched. What in the design would have told you?

---

## Scenario 4 — Developer Productivity with Claude

Tools built on the Agent SDK that help engineers explore unfamiliar codebases, understand
legacy systems, generate boilerplate and automate repetitive tasks, using the **built-in
tools (Read, Write, Bash, Grep, Glob)** and integrating with MCP servers.

**Primary domains:** Tool Design & MCP Integration · Claude Code Configuration &
Workflows · Agentic Architecture & Orchestration

| Read | Why this scenario needs it |
|---|---|
| [lesson 2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md) | The scenario names all six tools — and two of them are absent by default on macOS and Linux |
| [lesson 2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) | Wiring servers in, and what a populated `/mcp` does not prove |
| [lesson 5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) | "Explore unfamiliar codebases" is this lesson's entire subject |
| [lesson 2.1](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) | Boilerplate generation is where overlapping tool descriptions misroute |
| [lesson 1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) | Delegating the verbose reading |
| [lesson 3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) | The Explore subagent, for discovery that would fill the window |

**The question to ask yourself:** your permission rule for `Grep` never fires. Why?

---

## Scenario 5 — Claude Code for Continuous Integration

Claude Code in a CI/CD pipeline running automated code reviews, generating test cases and
providing pull request feedback, where you must **design prompts that give actionable
feedback and minimise false positives.**

**Primary domains:** Claude Code Configuration & Workflows · Prompt Engineering &
Structured Output

| Read | Why this scenario needs it |
|---|---|
| [lesson 3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) | `-p`, `--output-format json`, `--json-schema`, and CLAUDE.md as the CI context |
| [lesson 4.1](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md) | "Minimise false positives" is the scenario's own phrase, and "be conservative" is the named wrong answer |
| [lesson 4.6](course/domain-4-prompting-and-output/lesson-4-6-multi-instance-review.md) | The session that generated the code is the worst reviewer of it |
| [lesson 4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) | Actionable feedback has a format, and examples teach it |
| [lesson 4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) | Findings a pipeline can post as inline comments |
| [lesson 4.5](course/domain-4-prompting-and-output/lesson-4-5-batch-processing.md) | And why a pre-merge check cannot be a batch |

**The question to ask yourself:** developers have started ignoring the bot. Which category
do you turn off, and why does turning one off help the others?

---

## Scenario 6 — Structured Data Extraction

A system extracting information from unstructured documents, validating output against
JSON schemas, maintaining high accuracy, handling edge cases gracefully and integrating
with downstream systems.

**Primary domains:** Prompt Engineering & Structured Output · Context Management &
Reliability

| Read | Why this scenario needs it |
|---|---|
| [lesson 4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) | Schemas, `tool_choice`, and the three documented holes in the guarantee |
| [lesson 4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) | "Handling edge cases gracefully" — and the retry that cannot work |
| [lesson 5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) | "Maintaining high accuracy" is the phrase this lesson exists to interrogate |
| [lesson 4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) | Varied document structures, and reducing extraction hallucination |
| [lesson 4.5](course/domain-4-prompting-and-output/lesson-4-5-batch-processing.md) | Volume extraction at half price, with partial-failure recovery |
| [lesson 5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) | Trimming what a document tool returns before it accumulates |

**The question to ask yourself:** you are at 97% accuracy. What are you not able to say
yet?

---

## Coverage, stated honestly

Every one of the 29 task statements appears in at least one scenario above, and several
appear in four. **That is not a coincidence and it is worth planning around:** the domains
that recur across scenarios — Context Management & Reliability appears in five of six — pay
off more than their 15% weighting suggests, because they are in play whichever four
scenarios you draw.

The weights say how many items come from each domain. The scenarios say how often you will
need it. Those are different questions and the second one is not in the blueprint.

## Sources

Exam guide **Version 1.0, effective July 2026**, §5 — all six scenario descriptions and
their primary domains. §4 for the domain weights.

The lesson mappings and the closing questions are the author's reading of the published
scenarios, not Anthropic's. They are a study aid, not a statement about what the exam
asks.
