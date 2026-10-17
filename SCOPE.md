# What is in scope, and what is explicitly not

The exam guide's appendix (§17) lists the technologies and concepts that may appear, the
topics explicitly tested, and — more useful than either — **the topics that explicitly will
not appear.**

That last list is the reason this page exists. Most study time is lost to material that was
never going to be tested, and the guide tells you what that is.

Everything here is from the exam guide, **Version 1.0, effective July 2026**, §17.

---

## Explicitly OUT of scope

> "The following related topics will **not** appear on the exam"

Sixteen items. If you find yourself studying one of these, stop.

- Fine-tuning Claude models or training custom models
- Claude API authentication, billing, or account management
- Detailed implementation of specific programming languages or frameworks, beyond what is
  needed for tool and schema configuration
- **Deploying or hosting MCP servers** — infrastructure, networking, container
  orchestration
- Claude's internal architecture, training process, or model weights
- Constitutional AI, RLHF, or safety training methodologies
- Embedding models or vector database implementation details
- Computer use — browser automation, desktop interaction
- Vision and image analysis capabilities
- Streaming API implementation or server-sent events
- Rate limiting, quotas, or API pricing calculations
- OAuth, API key rotation, or authentication protocol details
- Specific cloud provider configurations — AWS, GCP, Azure
- Performance benchmarking or model comparison metrics
- **Prompt caching implementation details, beyond knowing it exists**
- Token counting algorithms or tokenization specifics

Three of those are worth dwelling on, because they are where a competent engineer's
instincts will pull them off course.

**Deploying MCP servers is out; designing them is in.** You need tool descriptions, error
shapes, scoping and configuration — lessons 2.1 through 2.4. You do not need Docker,
networking, or how to host one.

**Prompt caching is out "beyond knowing it exists."** That is an unusually precise
boundary. Know the term; do not study the mechanics.

**Cloud provider configuration is out** — which, if you came from a cloud certification
background, is the hardest habit to drop.

---

## Technologies and concepts that may appear

The guide's own list, verbatim in substance, with the lesson that covers each.

| Technology or concept | Covered in |
|---|---|
| **Claude Agent SDK** — agent definitions, agentic loops, `stop_reason` handling, hooks (`PostToolUse`, tool call interception), subagent spawning via **Task tool**, `allowedTools` configuration | [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) · [1.3](course/domain-1-agentic-architecture/lesson-1-3-subagent-invocation.md) · [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) |
| **Model Context Protocol** — servers, tools, resources, `isError` flag, tool descriptions, tool distribution, `.mcp.json`, environment variable expansion | [2.1](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) · [2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) · [2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) · [2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) |
| **Claude Code** — CLAUDE.md hierarchy (user/project/directory), `.claude/rules/` with YAML frontmatter path-scoping, `.claude/commands/`, `.claude/skills/` with SKILL.md frontmatter (`context: fork`, `allowed-tools`, `argument-hint`), plan mode, direct execution, `/memory`, `/compact`, `--resume`, `fork_session`, **Explore subagent** | [3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) · [3.2](course/domain-3-configuration/lesson-3-2-commands-and-skills.md) · [3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) · [3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) · [1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) · [5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) |
| **Claude Code CLI** — `-p` / `--print`, `--output-format json`, `--json-schema` | [3.5 and 3.6](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) |
| **Claude API** — `tool_use` with JSON schemas, `tool_choice` (`"auto"`, `"any"`, forced), `stop_reason` values (`"tool_use"`, `"end_turn"`), `max_tokens`, system prompts | [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) · [2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) · [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) |
| **Message Batches API** — 50% cost savings, up to 24-hour window, `custom_id`, polling, **no multi-turn tool calling support** | [4.5](course/domain-4-prompting-and-output/lesson-4-5-batch-processing.md) |
| **JSON Schema** — required vs optional fields, enums, nullable fields, `"other"` + detail string, strict mode for syntax error elimination | [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) |
| **Pydantic** — schema validation, semantic validation errors, validation-retry loops | [4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md) — see the note below |
| **Built-in tools** — Read, Write, Edit, Bash, Grep, Glob, their purposes and selection criteria | [2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md) |
| **Few-shot prompting** — targeted examples for ambiguous scenarios, format demonstration, generalisation to novel patterns | [4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) |
| **Prompt chaining** — sequential decomposition into focused passes | [1.6](course/domain-1-agentic-architecture/lesson-1-6-task-decomposition.md) |
| **Context window management** — token budgets, progressive summarisation, lost-in-the-middle, context extraction, scratchpad files | [5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md) · [5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) |
| **Session management** — resumption, `fork_session`, named sessions, session context isolation | [1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) |
| **Confidence scoring** — field-level confidence, calibration with labelled validation sets, stratified sampling | [5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) |

**Pydantic is named by the guide and the lessons treat it generically.** Lesson 4.4 teaches
validation, semantic-versus-syntactic errors and retry loops without tying them to a
library. The lab's `src/course_doctor/contracts.py` is Pydantic, so the concrete version is
there if you want it — but the exam is testing the *concepts* the guide lists, and this
course does not teach a library's API.

---

## In-scope topics, explicitly tested

The guide lists these separately from the technologies. Every one maps to a lesson except
the last, which is noted below.

Agentic loop implementation · multi-agent orchestration · subagent context management
including **crash recovery using manifests** · tool interface design · MCP tool and
resource design · MCP server configuration · error handling and propagation · escalation
decision-making · CLAUDE.md configuration including **`@import` patterns** · custom
commands and skills · plan mode versus direct execution · iterative refinement · structured
output via `tool_use` · few-shot prompting · batch processing · context window optimisation
· human review workflows.

### The one with no home

> **"Information provenance: claim-source mappings, temporal data handling, conflict
> annotation, coverage gap reporting"**

This is listed as explicitly tested and it maps to **no single task statement.** The course
covers its parts across [5.1](course/domain-5-context-and-reliability/lesson-5-1-conversation-context.md)
(metadata in structured outputs, attribution surviving handoffs),
[5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) (coverage
annotations for gaps from unavailable sources) and
[4.4](course/domain-4-prompting-and-output/lesson-4-4-validation-and-retry.md)
(`conflict_detected`), but never under that name.

Worth knowing as a phrase, because an item framed around "provenance" is asking about those
three things together: where did this claim come from, when was it true, and what did the
report fail to cover.

---

## Preparation material the guide publishes

Two things, and they are the only practice material with Anthropic's name on it.

**Sample questions with full rationales**, in §9. Each gives the correct answer and
explains why each distractor is wrong. Those explanations are the most valuable study
material in the entire guide, because they show you how the distractors are built.

**Four preparation exercises**, in §7 and §8. The guide's own suggested hands-on work.

**This course contains no practice questions and will not.** The guide's sample items are
published with reasoning; there is no reason to write worse ones, and good reason not to.
See [SOURCES.md](SOURCES.md) for what this course does and does not treat as a source.

## Sources

Exam guide **Version 1.0, effective July 2026**, §17 (Appendix: Technologies and Concepts,
In-Scope Topics, Out-of-Scope Topics), §9 (sample questions), §7 and §8 (preparation and
exercises).

The lesson mappings in the tables are the author's. The lists themselves are the guide's.
