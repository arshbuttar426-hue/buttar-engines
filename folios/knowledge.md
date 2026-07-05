# ai-agentic-workflow — Knowledge Base

This project uses the **ai-agentic-workflow** 4-phase methodology for complex multi-step code generation.

## Agent

A Codebuff agent is defined at `.agents/ai-agentic-workflow.ts` with programmatic phase enforcement via `handleSteps`. Invoke it with:

```
@ai-agentic-workflow
```

## Thinking Guide

`AGENTS.md` contains the internal thought-process version of the workflow — use it for self-checking during complex tasks.

## When to Use This Workflow

**Applies to:**
- Multi-file, multi-step code generation
- Cross-language translation or polyglot codebases
- Architecture planning before tool execution
- Industrial-grade code requiring modularity + testability

**Skip for:**
- Simple single-file edits (overhead exceeds benefit)
- Read-only queries
- Interactive debugging sessions

## Quick Reference

```
Phase 1: Plan → Phase 2: Normalize → Phase 3: Optimize → Phase 4: Verify → Ship
   ↑                                                                            |
   └─────────────────────── If any gate fails, fix and recheck ────────────────┘
```

## Gate Thresholds (Phase 4)

| Gate | Threshold |
|---|---|
| Cyclomatic complexity | < 3 per function |
| Module size | < 50 lines per file |
| Test patterns | assert, test_, describe must be present |
| Intent alignment | > 0.85 (escalate), > 0.7 (hard block) |
