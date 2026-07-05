Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

---
name: absurdity-coding
description: "Merged protocol: the Absurdity Coding Force-Down methodology (specificity engine, domain mappings, coding constraints) integrated with the AI Agentic Workflow 4-phase process (predetermine, normalize, optimize, verify). Strategic planning + tactical coding discipline."
metadata:
  category: coding-methodology
  version: 1.0
  architecture: hybrid
  benchmark_score: "7.4/10"
---

# Absurdity Agentic Coding — Unified Protocol

> *Every insight terminates in code. Every path is predetermined before execution. No abstraction without a file path. No publication without verification.*

---

## Table of Contents

1. [The Core Mandate](#1-the-core-mandate)
2. [When to Use This Protocol](#2-when-to-use-this-protocol)
3. [The 4-Phase Workflow Overview](#3-the-4-phase-workflow-overview)
4. [Phase 1: Predetermine — The Force-Down Protocol](#4-phase-1-predetermine--the-force-down-protocol)
5. [Phase 2: Normalize — Domain-Driven Implementation](#5-phase-2-normalize--domain-driven-implementation)
6. [Phase 3: Optimize — Bottleneck Management](#6-phase-3-optimize--bottleneck-management)
7. [Phase 4: Verify — Industrial Gates](#7-phase-4-verify--industrial-gates)
8. [Domain Mappings — 10 Coding Patterns](#8-domain-mappings--10-coding-patterns)
9. [Coding Constraints](#9-coding-constraints)
10. [Unified PR Checklist](#10-unified-pr-checklist)
11. [Priority Matrix](#11-priority-matrix)
12. [Failure Modes & Pitfalls](#12-failure-modes--pitfalls)

---

## 1. The Core Mandate

**Information preservation.** Every pipeline stage degrades structured data. The goal is to drive IRR (Information Retention Ratio) from ~0.34 toward 1.0 by replacing lossy summarization with lossless structured transformations.

### The Two Pipeline Stage Types

| Stage Type | Behavior | Coding Rule |
|---|---|---|
| **Lossless** | Structured → Structured | Preferred always. Typed in, typed out. |
| **Lossy** | Structured → Summarized | Explicitly marked, minimized, and measured. |

### The Single Most Impactful Change

Lower temperature on any stage that fills templates rather than creates. In LLM pipelines: `temperature = 0.3` instead of `1.5` for template-filling stages. This alone recovers ~55% of lost structured data.

---

## 2. When to Use This Protocol

### Use this protocol when the task involves:
- Complex multi-step code generation across multiple files
- Cross-language translation or polyglot codebases
- Debugging or optimizing token-heavy agent loops
- Industrial-grade code requiring modularity + testability
- Architecture planning before tool execution
- Refactoring monolithic modules into specialist components

### Do NOT use this protocol for:
- Simple single-file edits (overhead exceeds benefit — use Domain -1 directly)
- Read-only queries (no generation needed)
- Interactive debugging sessions (too structured)
- Trivial tasks where the Force-Down Protocol's 6 steps would take longer than the implementation itself

---

## 3. The 4-Phase Workflow Overview

Every coding task passes through four sequential phases. Do not skip phases. Do not proceed to the next phase until the current one is complete.

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  PHASE 1        │ ──▶ │  PHASE 2        │ ──▶ │  PHASE 3        │ ──▶ │  PHASE 4        │
│  PREDETERMINE   │     │  NORMALIZE      │     │  OPTIMIZE       │     │  VERIFY         │
│                 │     │                 │     │                 │     │                 │
│  Force-Down     │     │  Domain         │     │  Token budget   │     │  Specificity    │
│  Protocol       │     │  Mapping        │     │  Parallelize    │     │  Engine         │
│  State-space    │     │  AST normalize  │     │  Granularity    │     │  Complexity <3  │
│  enumeration    │     │  Drift detect   │     │  Temperature    │     │  Size <50 lines │
│  ⚠️ Specificity │     │                 │     │                 │     │  Intent align   │
│  Engine (veto)  │     │                 │     │                 │     │                  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Important:** The Specificity Engine is applied at TWO points:
1. **End of Phase 1** (Pre-code veto) — reject vague proposals BEFORE any code is written
2. **Phase 4 Gate 1** (Pre-publication) — verify the final implementation matches the spec

---

## 4. Phase 1: Predetermine — The Force-Down Protocol

Before any code is written, enumerate all valid execution paths and select the optimal one using the Force-Down Protocol.

### Step 1: Parse Intent & Enumerate Paths
1. Parse user intent into atomic sub-tasks using dependency analysis
2. Enumerate all valid execution paths (max depth 5, max 30 branches)
3. Select optimal path by minimizing token-to-execution ratio
4. Pre-identify 3–5 failure modes and their mitigations

### Step 2: Apply the Force-Down Protocol

Every feature, refactor, or architecture decision must pass through these 6 steps before any code is written.

| # | Step | Question | Example |
|---|---|---|---|
| 1 | **Reveal Principle** | What domain principle does this pattern borrow from? | "Immunological memory detects recurring drift patterns" |
| 2 | **Envision Artifact** | What is the concrete implementation? | `ImmuneMemory` class |
| 3 | **Define Interface** | What are the exact input/output types? | `recognize(drift: DriftEvent, memory: DriftDB) -> Correction | None` |
| 4 | **Pinpoint File Location** | What is the exact module path? | `src/pipeline/engines/immune.py` |
| 5 | **Identify Call Site** | Where is this invoked in the codebase? | `Pipeline.run()` at line 142 |
| 6 | **Plan Tests** | What are the ≥3 test cases? | normal, edge, failure |

### Step 3: Apply the Specificity Engine (Pre-Code Veto)

Before moving to Phase 2, run the Specificity Engine. Any NO means **reject the proposal** — do not proceed until it passes.

| Criteria | Pass/Fail |
|---|---|
| Names a file (exact path relative to project root) | YES / NO |
| Names a function/class/module | YES / NO |
| Inputs and outputs are typed (concrete types, not Any) | YES / NO |
| Can be tested (test plan with ≥3 cases exists) | YES / NO |
| Call site is identified (file + function + approximate line) | YES / NO |

### Vague → Specific Translations

Use this reference table to convert vague requests into spec that passes the Specificity Engine:

| Vague | Specific |
|---|---|
| "Improve continuity" | "Create `CharacterDNA.encode()` that extracts 13 traits from a structured profile and appends them verbatim to every prompt segment" |
| "Optimize performance" | "Add LRU cache to `model_router.assign()` with `maxsize=128` — reduces redundant model loads" |
| "Prevent drift" | "Create `ContinuityHomeostat.correct()` that checks `mass >= 2.0` and `segment > 2` before injecting a correction clause" |
| "Add error handling" | "Wrap `api.call()` in `try/except` with retry logic (3 attempts, exponential backoff, log on failure)" |
| "Make it faster" | "Replace `Gemma-12B` on `film_dna` stage with `Phi-4-mini` at `T=0.3`, reducing latency from 17s to 0.7s" |
| "Refactor this" | "Extract `parse_config()` from `app.py:200-250` into `src/config/parser.py` with typed return schema" |

### Step 4: Path Selection

Select the execution path with the lowest estimated token-to-execution ratio:
```
estimated_tokens = path_depth * 50 * complexity_factor
token_to_execution_ratio = estimated_tokens / expected_output_lines
```

---

## 5. Phase 2: Normalize — Domain-Driven Implementation

### Language Barrier Resolution

When working across languages, type systems, or frameworks:

1. **Convert to Universal AST:** Normalize code to universal operations: `def`, `class`, `func`, `fn`, `let`, `var`, `import`
2. **Detect Semantic Drift:** Compare source and target representations. Flag any meaning-altering transformations.
3. **Bridge Type Systems:** Use gradual typing patterns. Map between type constructs (e.g., `interface` → `protocol` → `trait`).
4. **Defer Idiomatization:** Apply language-specific idioms only in the final output step (Late Idiomatization). Premature idiomatization wastes tokens on transformations that may be discarded.

### Select Domain Pattern

Choose the appropriate coding pattern from the [Domain Mappings](#8-domain-mappings--10-coding-patterns) that best fits the task. Each domain maps to a concrete architecture pattern.

### Semantic Drift Detection

```python
def detect_semantic_drift(source: str, target: str, threshold: float = 0.7) -> list[Drift]:
    """Flag meaning-altering differences between source and target representations."""
```

For short queries producing long code, use symbolic execution as a tiebreaker — low word overlap is expected, not drift.

---

## 6. Phase 3: Optimize — Bottleneck Management

### Token Budget Computation

Compute the token budget before executing tool calls:
```
estimated_tokens = depth * 50 * complexity_factor
token_budget = min(estimated_tokens, max_tokens)
```

### Parallelization

Identify independent tool calls via dependency graph analysis and run them in parallel:
- Calls that read but don't write the same data → parallel
- Calls in a sequence where output feeds input → serial
- Granularity: each call should span 50–200 lines

### Context Compression

Compress historical context at a 3:1 target ratio, retaining only:
- Variable and function declarations
- Module structure
- Import statements
- Error messages

Compression beyond 3:1 drops latent dependencies — keep full window for the last 2 iterations.

### Temperature Control

| Stage Type | Temperature | Rationale |
|---|---|---|
| Template filling, data transforms | 0.1–0.3 | No creativity needed |
| Code generation with specs | 0.3–0.5 | Follow structure, moderate variation |
| Creative code, novel solutions | 0.7–1.2 | Exploration needed |
| Brainstorming, alternative approaches | 1.2–1.5 | Maximum variation |

### Performance Budget

Every component has a latency budget. If it exceeds its budget:
- It must self-report the overrun
- It must not block dependent components (timeout + fallback)

---

## 7. Phase 4: Verify — Industrial Gates

### Gate 1: Specificity Engine (Final Check)

Re-run the Specificity Engine on the final implementation before publication. This verifies the output matches what was planned in Phase 1.

| Criteria | Pass/Fail |
|---|---|
| Names a file (exact path relative to project root) | YES / NO |
| Names a function/class/module | YES / NO |
| Inputs and outputs are typed (concrete types, not Any) | YES / NO |
| Can be tested (test plan with ≥3 cases exists) | YES / NO |
| Call site is identified (file + function + approximate line) | YES / NO |

**Rejection rule:** Any NO → reject. Return to Phase 1 if the spec has drifted.

### Gate 2: Industrial Complexity Gates

| Metric | Threshold | Action |
|---|---|---|
| Cyclomatic complexity per module | < 3 | Refactor if exceeded |
| Module size | < 50 lines | Split if exceeded |
| Test coverage | > 80% | Add tests if below |
| Redundancy score | 0.0 | Eliminate duplicates |

### Gate 3: Intent Alignment

Compute the alignment score between the user's original intent and the final generated code:
```
alignment = similarity(user_intent, generated_code)
if alignment > 0.85:  publish()
elif alignment > 0.70: request_review()
else:                  escalate() and regenerate()
```

### Gate 4: Verify — Escalate — Publish Cycle

```
while not_published:
    if all_gates_pass() and alignment > 0.7:
        publish()
    elif can_fix():
        fix()
    else:
        escalate()  # document why gates failed
```

---

## 8. Domain Mappings — 10 Coding Patterns

Each domain maps to a concrete coding pattern. Select the best pattern in Phase 2.

### Domain 1: Biology — Mycelial Distribution

**Pattern:** Replace monolithic components with distributed specialist modules communicating via typed ports.
- No module shall have more than one responsibility
- Modules communicate through typed interfaces, not shared state
- A coordinator (router) assembles outputs, not a central planner

**When to use:** Any system where a single "god class" or monolithic handler is doing too much.

### Domain 2: Physics — Maxwell's Demon

**Pattern:** Sort data into labeled dimensions rather than fusing/summarizing. Preserve structure by grouping related fields under clear labels.
- Use labeled sections/blocks instead of prose summaries
- Each dimension has its own schema
- The final output is a sorted array of structured blocks, not a paragraph

**When to use:** Template filling, prompt assembly, report generation — any place where structured input gets flattened into text.

### Domain 3: Chemistry — Catalytic Templates

**Pattern:** Static templates that never mutate. Data flows through the template; the template itself is constant.
- Templates are read-only after creation
- Template format is decoupled from data sources
- A template may be versioned but never edited in-place during execution

**When to use:** Code generation, prompt templates, document scaffolding, config file generation.

### Domain 4: Biomechanics — Joints Over Levers

**Pattern:** Composition over inheritance. Build from small, composable joints (functions, protocols, interfaces) rather than deep inheritance levers.
- Prefer composition / delegation / strategy pattern over inheritance
- Maximum inheritance depth: 2 levels
- Interfaces are narrow (≤3 methods)

**When to use:** Any class hierarchy that exceeds 2 levels of depth.

### Domain 5: Philosophy — Decentralized Decision Making

**Pattern:** No single component makes all decisions. Decisions are distributed to the component with the most relevant context.
- The module that owns the data makes decisions about that data
- Coordinator modules route, they don't decide content
- Decision logic lives close to the data it acts on

**When to use:** Pipeline architectures, orchestration systems, multi-agent systems.

### Domain 6: Psychology — Object Permanence & State Schema

**Pattern:** Objects continue to exist even when not actively referenced. Maintain a world schema of all persistent objects and their states.
- Every persistent object has a `last_seen` timestamp
- Objects that haven't been referenced retain their last known state
- State is explicitly reset, not implicitly forgotten

**When to use:** Session management, game state, long-running workflows, multi-turn conversations.

### Domain 7: Medicine — Homeostatic Regulation

**Pattern:** Monitor critical values, detect deviation from set points, apply corrective feedback.
- Define set points (expected values) for all critical state
- Monitor actual values at each cycle
- If deviation exceeds threshold, inject correction
- Corrections are logged for audit

**Implementation skeleton:**
```python
class Homeostat:
    set_points: dict[str, Any]
    tolerance: dict[str, float]

    def check(self, actual: dict[str, Any]) -> list[Correction]:
        corrections = []
        for key, expected in self.set_points.items():
            if key in actual and abs(actual[key] - expected) > self.tolerance.get(key, 0):
                corrections.append(Correction(key, actual[key], expected))
        return corrections
```

**When to use:** State reconciliation, data sync, continuity enforcement, configuration drift detection.

### Domain 8: Economics — VCG Auction for Resource Allocation

**Pattern:** When multiple resources/models/algorithms can handle a task, use a truthful auction to select the best one.
- Each candidate bids based on measurable performance metrics
- Winner pays the second-highest bid (truthful bidding)
- Bids are based on real measurements, not estimates

**Bid formula:** `bid = speed × reliability / cost`

**When to use:** Multi-model orchestration, API gateway routing, algorithm selection, cache eviction.

### Domain 9: Cryptography — Integrity Chains

**Pattern:** Verify data integrity through hashing/checksum chains. Each step includes the hash of the previous step.
- Each state transition produces a hash of (new_state + previous_hash)
- Integrity is verified before each operation
- A mismatch triggers explicit remediation, not silent continuation

**When to use:** Data pipelines, ETL, state machines, event sourcing, audit trails.

### Domain -1: Parsimony — Occam's Razor

**Pattern:** The simplest solution that passes all tests is preferred. Every abstraction must justify its existence.
- Do not add a domain pattern unless it measurably improves some metric (IRR, latency, maintainability)
- If a solution uses >3 domain patterns, two must be removed
- Favor standard library over dependencies
- Do not add a class when a function suffices
- Do not add a function when inline code suffices (once)

**This is the negative domain.** It votes NAY on every proposal. Proposals must overcome its objection with measurable evidence, not theoretical benefit.

---

## 9. Coding Constraints

These constraints apply to all code written under this methodology.

### 9.1 Lossless Transforms Preferred
Prefer structured → structured transformations. When a lossy transform is unavoidable:
- Mark it explicitly: `# LOSSLY: reason`
- Measure the IRR for that stage
- Document what was lost

### 9.2 Interface Rigor
- Every function has typed parameters and return type
- No `Any` unless the value is truly any type
- No `**kwargs` without documented schema
- Dict values must have documented key schemas

### 9.3 Test Coverage Requirements
Every module must have:
- 1+ normal path test
- 1+ edge case test
- 1+ failure mode test

### 9.4 No Silent Degradation
If a system cannot fulfill its contract:
- It must raise an explicit error
- Or return a structured error result (never `None` to mean "something went wrong")
- Or log a warning and fall back to a documented degraded mode

### 9.5 Temperature Control
- Template filling stages: `temperature = 0.3` (no creativity needed)
- Creative stages: `temperature = 0.7–1.5` as needed
- Never use default temperature without justification

---

## 10. Unified PR Checklist

Every pull request must pass this checklist before review.

### Phase 1 Check (Predetermine)
- [ ] Intent parsed into atomic sub-tasks
- [ ] Execution paths enumerated (≤30 branches)
- [ ] Optimal path selected by token-to-execution ratio
- [ ] 3–5 failure modes identified with mitigations
- [ ] Force-Down Protocol steps 1–6 completed
- [ ] Specificity Engine applied — all 5 criteria pass before code written

### Phase 2 Check (Normalize)
- [ ] Language barriers resolved (AST normalized)
- [ ] Domain pattern selected from 10 mappings
- [ ] Semantic drift checked (threshold ≥ 0.7)
- [ ] Idiomatization deferred to final output

### Phase 3 Check (Optimize)
- [ ] Token budget computed and not exceeded
- [ ] Independent calls parallelized
- [ ] Granularity: each call 50–200 lines
- [ ] Context compressed at ≤3:1 ratio
- [ ] Temperature set appropriately for each stage

### Phase 4 Check (Verify)
- [ ] Specificity Engine — all 5 criteria pass (final verification)
- [ ] Cyclomatic complexity < 3 per module
- [ ] Module size < 50 lines per module
- [ ] Test coverage > 80%
- [ ] Redundancy score = 0.0
- [ ] Intent alignment > 0.7
- [ ] No silent degradation paths
- [ ] Lossy stages are explicitly marked

---

## 11. Priority Matrix

| Priority | Pattern | Effort | Impact | Why |
|---|---|---|---|---|
| 1 | Temperature reduction | Minutes | High | Single change, biggest IRR gain |
| 2 | Static templates | Low | High | Eliminates source of most lossy summarization |
| 3 | Homeostatic monitoring | Medium | High | Catches drift before it compounds |
| 4 | Modular decomposition | High | High | Replaces god classes with specialist modules |
| 5 | Integrity chains | Medium | Medium | Audit trail for pipeline debugging |
| 6 | VCG auctions | High | Medium | Optimization — only needed when >1 resource |
| 7 | Immune memory | High | Medium | Optimization — only needed after drift patterns emerge |
| 8 | Predetermination automation | Medium | High | Reduces planning overhead on complex tasks |
| 9 | Language barrier resolution | High | Medium | Cross-language polyglot codebases |

---

## 12. Failure Modes & Pitfalls

| Failure Mode | Context | Mitigation |
|---|---|---|
| **Over-planning** | Phase 1 — state enumeration beyond 30 branches | Hard cap at 30. After that, proceed with best current path. |
| **False drift positives** | Phase 2 — short queries produce low word overlap with long generated code | Use symbolic execution as tiebreaker. Low overlap isn't drift. |
| **Premature idiomatization** | Phase 2 — injecting language-specific patterns before bottleneck optimization | Defer all idiomatic transforms to the final output step. |
| **Compression loss** | Phase 3 — aggressive compression (> 3:1) drops latent dependencies | Keep full window for last 2 iterations. Hard cap at 3:1. |
| **Over-applying the protocol** | All phases — using the 4-phase workflow on trivial single-file edits | Consult Section 2. Use Domain -1 directly for simple tasks. |
| **Silent degradation** | Phase 4 — system fails without reporting | Enforce no-silent-degradation constraint. Every failure must be explicit. |
| **Abstraction without evidence** | All phases — Domain -1 violation | Require measurable evidence (IRR, latency, maintainability) before adding any pattern. |
| **Specificity drift** | Phase 1 → Phase 4 — the implementation diverges from the spec | Apply Specificity Engine at BOTH Phase 1 (veto) and Phase 4 (verify). |

---

*Every insight terminates in code. Every path is predetermined before execution. No abstraction without a file path.*
