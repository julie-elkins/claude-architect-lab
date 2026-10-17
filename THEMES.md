# Four ideas that carry most of this exam

The blueprint has 29 task statements. It does not tell you that several of them are the
same idea wearing different clothes.

This page names four. They are not in the exam guide — they are what fell out of writing
all 29 lessons and noticing the same shape arriving again. **If you understand these four,
you can reason your way to answers in task statements you have not studied**, because the
distractors are built from the same handful of plausible mistakes.

Read this last, not first. It will mean more once you have seen the instances.

---

## 1. A thing that looks like a guarantee and is not

The single most productive idea in this exam. In every case below there is a mechanism that
*prevents* something and a mechanism that *asks* for it, they read almost identically, and
the exam will offer you both.

| Where | What looks like a guarantee | What it actually is |
|---|---|---|
| [3.1](course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md) | A rule in `CLAUDE.md` | Context. The docs: *"not enforced configuration… To block an action regardless of what Claude decides, use a PreToolUse hook instead"* |
| [3.4](course/domain-3-configuration/lesson-3-4-plan-mode.md) | Plan mode blocks edits | It does in headless, SDK and VS Code chat. In an interactive terminal with bypass available, *"Claude Code also doesn't enforce plan mode's blocks"* |
| [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) | A hook enforces a policy | Until its script is missing, times out or crashes — all **non-blocking by default**, action proceeds. `onFailure: "block"` is the fix |
| [1.4](course/domain-1-agentic-architecture/lesson-1-4-enforcement-and-handoff.md) | A prompt instruction orders a workflow | The guide: prompt instructions alone have a **non-zero failure rate** |
| [2.3](course/domain-2-tools-and-mcp/lesson-2-3-tool-distribution.md) | "Always call the tool" under `tool_choice: "auto"` | A request the model may decline by answering in prose |
| [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) | A strict schema | Guarantees shape, not sense — and leaks on a refusal, a truncation, and enum capitalisation |

**The exam shape:** when one option strengthens wording and another adds a mechanism, the
mechanism is the answer. Every time.

**The practical corollary:** *"it did not do the thing"* is not the claim *"it could not do
the thing."* Only one of those is a control, and only firing it tells you which you have.

---

## 2. An absence that reads as a result

The failure this exam cares most about, and the one that is invisible by construction: a
report, a count or a status that is produced by *nothing having happened* and is
indistinguishable from one produced by success.

| Where | The flattering reading | What it can also mean |
|---|---|---|
| [5.3](course/domain-5-context-and-reliability/lesson-5-3-error-propagation.md) | An empty result | The search failed. Named anti-pattern: *"returning empty results as success"* |
| [2.2](course/domain-2-tools-and-mcp/lesson-2-2-structured-errors.md) | No data | An access failure, or a valid empty result — opposite responses |
| [1.2](course/domain-1-agentic-architecture/lesson-1-2-coordinator-patterns.md) | Every worker succeeded | The decomposition was too narrow and nothing covered the gaps between them |
| [5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) | 97% accurate | 60% on a document type that is a fifth of the volume |
| [2.5](course/domain-2-tools-and-mcp/lesson-2-5-built-in-tools.md) | A permission rule is in place | On macOS and Linux a `Grep` rule matches nothing, because the search arrives as `Bash` |
| [2.4](course/domain-2-tools-and-mcp/lesson-2-4-mcp-integration.md) | `/mcp` lists the tools | The list came from a discovery cache; the server has not been contacted |
| [1.7](course/domain-1-agentic-architecture/lesson-1-7-session-state.md) | The session restored fully | It restored file contents from before you edited those files |
| [5.4](course/domain-5-context-and-reliability/lesson-5-4-codebase-exploration.md) | A fluent, confident answer | Generic. The specific knowledge degraded and the prose did not |
| [3.3](course/domain-3-configuration/lesson-3-3-path-specific-rules.md) | A scoped rule never fired | Either the glob matches nothing, **or** the YAML failed to parse and it is loading on everything |

**The exam shape:** an option that reports what it could *not* check beats an option that
reports only findings.

**The practical corollary:** every result needs a coverage statement. Not as politeness —
as the only thing that distinguishes a clean run from a run that never started.

---

## 3. Wording strength is not a mechanism

Domain 4's thesis, and it reaches into three other domains. Asking more firmly is never the
answer, and it is always one of the options.

| Where | The tempting fix | The mechanism |
|---|---|---|
| [4.1](course/domain-4-prompting-and-output/lesson-4-1-explicit-criteria.md) | "Be conservative", "only high-confidence findings" | A categorical report-versus-skip list. The guide names both phrases as *failing* |
| [4.2](course/domain-4-prompting-and-output/lesson-4-2-few-shot.md) | More detailed instructions | 2–4 worked examples, including the ambiguous case |
| [4.3](course/domain-4-prompting-and-output/lesson-4-3-structured-output.md) | "Reply in valid JSON" | A schema, through tool use |
| [1.5](course/domain-1-agentic-architecture/lesson-1-5-hooks.md) | "Never run destructive commands" | A `PreToolUse` hook |
| [5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md) | "Escalate when the customer is upset" | Explicit criteria: a request for a human, a policy gap, no progress possible |
| [3.5](course/domain-3-configuration/lesson-3-5-3-6-iteration-and-pipelines.md) | "Be more careful about severity" | Concrete input/output examples |

**The tell:** if you cannot say what changed about the *test*, you have added an adverb.

---

## 4. Branch on structure, never on prose

A quieter theme, and the one that distinguishes a robust design from one that works most of
the time.

| Where | The soft signal | The hard signal |
|---|---|---|
| [1.1](course/domain-1-agentic-architecture/lesson-1-1-agentic-loops.md) | Parsing text for "I'm done"; checking whether assistant text exists | Tool calls present or absent. Both soft versions are **named anti-patterns**, and the text check fails intermittently because a model can emit text *and* tool calls together |
| [5.2](course/domain-5-context-and-reliability/lesson-5-2-escalation.md) | Sentiment; a self-reported confidence score | A policy gap, or an explicit request |
| [5.5](course/domain-5-context-and-reliability/lesson-5-5-human-review-and-calibration.md) | A confidence number, as a filter | The same number, **calibrated against labelled outcomes**, as a routing signal |
| [2.1](course/domain-2-tools-and-mcp/lesson-2-1-tool-interfaces.md) | Hoping the right tool is chosen | A description that names what the tool does *not* do and which sibling to use instead |

**The subtlety worth carrying:** confidence is ruled out as a *filter* in 4.1 and 5.2, and
named as a *routing signal* in 4.6 and 5.5. That is not a contradiction. Uncalibrated, it
is a word; measured against labelled data, it carries information. The difference is
whether anyone checked.

---

## Using this on exam day

Four scenarios, sixty items, judgment-weighted. When an item has four defensible-looking
options, the four questions above resolve most of them:

1. Is one option a **mechanism** and another a **request**?
2. Does one option **report what it could not check**?
3. Is one option an **adverb** and another a **test**?
4. Is one option reading a **soft signal** where a structural one exists?

**What this page is not.** It is not a shortcut past the task statements, and it is not
Anthropic's framing — the four headings are mine, drawn from writing the lessons. The
exam guide is the authority on what is tested. This is a way of holding it.

## Sources

Every row links to the lesson that carries the claim and its citation. The themes
themselves are the author's synthesis across all 29 lessons and are not stated anywhere in
the exam guide.
