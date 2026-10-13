# Sources

Every factual claim in this course traces to one of two places. If a claim cannot be traced to
a row in this file, **it gets cut rather than softened.**

## The two permitted sources

**A. The published CCAR-F exam guide.** A public PDF linked from the certification page on the
Anthropic Partner Academy. No login required.

- Title: *Claude Certified Architect – Foundations Exam Guide*
- Get it yourself from the certification page, which links the PDF directly:
  <https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification>
  (verified reachable 2026-10-12). The same page links the **Certification Terms and
  Conditions** and the **Anthropic Certification Exam Policy** — read both before booking.
- Version read for this course: **Version 1.0, effective July 2026**
- The guide states it is "subject to change without notice," so **re-read it before re-recording
  any episode.** If the version string has moved past 1.0, treat every row below as unverified
  until checked.

**B. Public Claude documentation**, at `docs.claude.com` and `claude.com`. Cited by URL with the
date read.

## What is NOT a source, and never will be

**Sitting the exam.** Exam content — questions, answer options, and the scenarios as presented
during the exam — is confidential and proprietary under the non-disclosure agreement accepted
before the exam begins. None of it appears in this course in any form, including paraphrase,
including "the kind of thing they ask."

The six scenarios are discussed in this course **only because the exam guide publishes them**
in section 5. That publication is Anthropic's, not mine.

**Other people's prep material, braindumps, or exam-recall forums.** Not consulted, and not a
permitted source if offered.

## Claim table

Source column `EG §n` means exam guide section n. `TS n.n` means task statement.

### Exam mechanics (README)

| Claim | Source |
|---|---|
| Exam code CCAR-F | EG §3 |
| 60 items | EG §3 |
| Multiple-choice and multiple-response; each item states how many to select | EG §3 |
| 4 scenarios drawn from a bank of 6 | EG §3, §5 |
| 120 minutes | EG §3 |
| Passing score 720 scaled on 100–1,000 | EG §3, §10 |
| Fee $125 USD | EG §3 |
| Validity 12 months from award | EG §3 |
| Score report gives percent-correct by domain | EG §3 |
| Section percentages do not determine pass/fail; total scaled score does | EG §10 |
| Exam is criterion-referenced | EG §10 |
| Confidentiality agreement covers questions, answer options and scenarios | EG §14 |

### Blueprint weights (README, every episode's opening slide)

| Domain | Weight | Source |
|---|---|---|
| 1 — Agentic Architecture & Orchestration | 27% | EG §4 |
| 2 — Tool Design & MCP Integration | 18% | EG §4 |
| 3 — Claude Code Configuration & Workflows | 20% | EG §4 |
| 4 — Prompt Engineering & Structured Output | 20% | EG §4 |
| 5 — Context Management & Reliability | 15% | EG §4 |

### Course thesis

| Claim | Source |
|---|---|
| The exam measures practical judgment about tradeoffs, not only conceptual knowledge | EG §1, quoted verbatim in README |
| Questions are grounded in realistic scenarios from customer use cases | EG §1 |
| Intended candidate has 6+ months practical experience with the four technologies | EG §2 |

### Episode 1 — Claude Code Configuration & Workflows (Domain 3)

| Claim | Source |
|---|---|
| Domain 3 covers CLAUDE.md hierarchy and scoping | EG §6, TS 3.1 |
| Custom slash commands and skills are tested | EG §6, TS 3.2 |
| Path-specific rules for conditional convention loading are tested | EG §6, TS 3.3 |
| Plan mode vs direct execution is a tested judgment call | EG §6, TS 3.4 |
| Iterative refinement for progressive work is tested | EG §6, TS 3.5 |
| Claude Code in CI/CD pipelines is tested | EG §6, TS 3.6 |
| `.claude/rules/` files use YAML frontmatter glob patterns, e.g. `paths: ["src/api/**/*"]` | EG §8, Exercise 2 |
| Skills support `context: fork` and `allowed-tools` frontmatter | EG §8, Exercise 2 |
| `.mcp.json` supports environment variable expansion for credentials | EG §8, Exercise 2 |
| A personal MCP server can live in `~/.claude.json` alongside a project `.mcp.json`, both available at once | EG §8, Exercise 2 |
| Preparation includes configuring Claude Code for a real project | EG §7 |

**Verified by running it, 2026-10-13**, against Claude Code and `mcp` 2.3.0 on this machine.
These are recorded as OBSERVED rather than cited, which is a weaker claim than a documentation
URL and is labelled as such — a behaviour measured on one version is not a documented contract:

- [x] **`.mcp.json` loads a project server, and `${VAR:-default}` expansion works.** OBSERVED:
      the server appeared as `mcp__course-doctor__read_material_file` and nothing else.
- [x] **`.claude/rules/` files load CONDITIONALLY.** OBSERVED: both rule files were present on
      disk and *not* in context, because no matching file had been touched. This is the
      episode's central claim and it is demonstrable on camera rather than asserted.
- [x] **A project skill with `context: fork` and `allowed-tools` is recognised.** OBSERVED:
      `check-sources` was listed as available.
- [x] **A project `CLAUDE.md` does NOT suppress a parent one.** OBSERVED: both the repo's
      `CLAUDE.md` and the one in the parent directory loaded together.

**Still needs a documentation citation before Episode 1 is recorded** — each needs a
`docs.claude.com` URL and a read date, because the script states these as how the mechanism
works rather than as what one run did:

- [ ] CLAUDE.md resolution order across enterprise, user, project and subdirectory scope
- [ ] `.claude/rules/` frontmatter schema and exact glob matching semantics
- [ ] Skill frontmatter: the full option list, and precisely what `context: fork` isolates
- [ ] `.mcp.json` schema, and whether `${VAR:-default}` is a documented form or incidental
- [ ] Slash command file format and argument passing
- [ ] Plan mode: what it permits and what it blocks

## Verification procedure

Before any episode is published:

1. Every `docs.claude.com` URL in that episode's rows returns 200 **and still says what the row
   claims.** A live link is not a verified claim — pages get rewritten under the same URL.
2. Every mechanic demonstrated on camera is run from a **clean clone** in a fresh shell. A lab
   that works only on the author's machine is the standard way this kind of material is wrong.
3. The exam guide version string is re-read and still matches the version recorded above.

## Known gaps, stated rather than hidden

- The exam guide publishes domain weights but not item counts per domain. Any statement like
  "expect about sixteen questions on Domain 1" would be my arithmetic on a percentage, not a
  published figure, and **does not appear in this course.**
- The guide's four preparation exercises are the closest thing to practice material that
  Anthropic publishes. This course builds against them, but completing them is not a predictor
  of a score and is not presented as one.
- No pass-rate, difficulty or score-distribution claim appears anywhere in this course. None is
  published, and I have access to no such data for this exam.
