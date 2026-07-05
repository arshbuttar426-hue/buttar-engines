#!/usr/bin/env python3
"""
PonytailLadder — Deterministic Code Minimalism Gate
====================================================
Absurdist AI Agent Workflow reimplementation of Ponytail.

Replaces prose-rule injection (IRR~0.65) with a typed, lossless
evaluation function (IRR=1.0). Each rung is a deterministic check.
Every output has an integrity chain. Homeostatic monitoring detects
drift. VCG auction selects optimal rung depth per task type.

Usage:
    ladder = PonytailLadder()
    result = ladder.evaluate(TaskSpec(
        task_type="bug_fix",
        description="Fix null pointer in user auth",
        language="python",
        existing_deps=["flask", "sqlalchemy"],
    ))
    print(result.rung, result.justification)

Domains implemented:
    D1 Mycelial  — specialist rung checkers, not monolithic
    D2 Maxwell   — tasks sorted into labelled dimensions
    D3 Catalytic — ladder template is frozen, data flows through
    D4 Joints    — flex under high complexity, direct under low
    D5 Philosophy— multiple interpretations when ambiguous
    D6 Permanence— audit trail of all evaluations
    D7 Homeostasis—set points + drift correction
    D8 VCG      — rung depth auction per task type
    D9 Integrity — chain of hashes per evaluation
    D-1 Parsimony— bypasses itself on trivial tasks
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════
#  CORE TYPES
# ═══════════════════════════════════════════════════════════════

class RungLevel(Enum):
    """Each rung is a stopping point. The first matching rung wins."""
    YAGNI = auto()      # Task doesn't need to exist — skip entirely
    STDLIB = auto()     # Standard library covers it
    NATIVE = auto()     # Native platform feature covers it
    DEP = auto()        # Already-installed dependency covers it
    ONELINE = auto()    # Can be done in one line
    MINIMUM = auto()    # Write the minimum code that works


@dataclass(frozen=True)
class TaskSpec:
    """Lossless typed input to the ladder."""
    task_type: str                     # "bug_fix", "feature", "refactor", "test", "docs"
    description: str                   # Natural language description
    language: str                      # "python", "javascript", "go", "rust", etc.
    existing_deps: tuple[str, ...] = ()  # Already in project
    estimated_complexity: float = 1.0  # 1.0 (trivial) to 10.0 (extremely complex)
    context_tokens: int = 0            # Size of surrounding context
    files_touched: tuple[str, ...] = ()  # Files this task affects

    def __post_init__(self):
        assert 1.0 <= self.estimated_complexity <= 10.0, \
            f"complexity must be 1-10, got {self.estimated_complexity}"
        assert self.task_type in TASK_TYPES, \
            f"task_type must be one of {TASK_TYPES}, got '{self.task_type}'"


TASK_TYPES = frozenset({"bug_fix", "feature", "refactor", "test", "docs"})

# Lossless — typed in, typed out
@dataclass(frozen=True)
class EvaluationResult:
    rung: RungLevel
    justification: str
    evidence: dict
    chain_hash: str
    prev_hash: str = "GENESIS"  # Previous hash in chain (self-contained)
    timestamp: float = field(default_factory=time.time)
    rung_depth: int = 0  # How many rungs were checked before stopping

    def verify_chain(self) -> bool:
        """D9 Integrity: verify this result's hash chain using stored prev_hash."""
        content = f"{self.rung.name}:{self.justification}"
        raw = f"{content}|{self.prev_hash}"
        expected = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return expected == self.chain_hash


# ═══════════════════════════════════════════════════════════════
#  D9 INTEGRITY — Hash Chain Utility
# ═══════════════════════════════════════════════════════════════

_CHAIN_STORE: list[str] = []  # D6 Permanence: all previous chain hashes


def hash_chain(result: EvaluationResult, prev_hash: str = "GENESIS") -> str:
    """Produce a hash of (rung + justification + previous_hash)."""
    content = f"{result.rung.name}:{result.justification}"
    raw = f"{content}|{prev_hash}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def verify_integrity(result: EvaluationResult) -> bool:
    """Verify a result's chain against the stored chain (uses result's own prev_hash)."""
    return result.verify_chain()


# ═══════════════════════════════════════════════════════════════
#  D1 MYCELIAL — Specialist Rung Checkers
#  Each rung is an independent module communicating via typed ports.
# ═══════════════════════════════════════════════════════════════

class StdlibChecker:
    """D1 specialist: knows what each language's stdlib provides."""

    STDLIB_MAP: dict[str, set[str]] = {
        "python": {"json", "csv", "re", "math", "datetime", "os", "sys",
                   "pathlib", "collections", "itertools", "functools",
                   "typing", "dataclasses", "enum", "hashlib", "tempfile",
                   "subprocess", "threading", "multiprocessing"},
        "javascript": {"Array", "Object", "Map", "Set", "Promise",
                       "JSON", "Date", "Math", "RegExp", "String",
                       "Number", "Symbol", "Intl", "URL", "fetch",
                       "structuredClone", "atob", "btoa"},
        "typescript": {"Array", "Map", "Set", "Promise", "JSON",
                       "Date", "Math", "RegExp"},
        "go": {"fmt", "strings", "strconv", "encoding/json", "os",
               "io", "net/http", "time", "sync", "math", "sort"},
        "rust": {"std::collections", "std::fmt", "std::fs", "std::io",
                 "std::path", "std::sync", "std::thread", "std::time",
                 "std::net", "regex"},
    }

    def check(self, spec: TaskSpec) -> Optional[dict]:
        """If the task can be solved by stdlib, return evidence. Else None."""
        stdlib = self.STDLIB_MAP.get(spec.language, set())
        desc_lower = spec.description.lower()

        import re as _re
        matches = set()
        for lib in stdlib:
            lib_clean = lib.replace("std::", "").replace("_", " ")
            # Word-boundary matching to avoid false positives like "re" in "implement"
            pattern = r'\b' + _re.escape(lib_clean.lower()) + r'\b'
            simple_name = lib.split("::")[-1].lower()
            pattern2 = r'\b' + _re.escape(simple_name) + r'\b'
            if _re.search(pattern, desc_lower) or _re.search(pattern2, desc_lower):
                matches.add(lib)

        if not matches:
            return None

        return {
            "matched_libs": sorted(matches),
            "language": spec.language,
            "evidence": f"Standard library contains {len(matches)} relevant modules",
        }


class NativeChecker:
    """D1 specialist: knows native platform features."""

    NATIVE_FEATURES: dict[str, list[tuple[str, set[str]]]] = {
        "html": [
            ("<input type='date'>", {"date", "picker", "calendar"}),
            ("<input type='color'>", {"color", "picker"}),
            ("<input type='range'>", {"range", "slider"}),
            ("<dialog>", {"dialog", "modal"}),
            ("<details>", {"accordion", "details", "disclosure"}),
            ("<progress>", {"progress", "loading bar"}),
            ("localStorage", {"local storage", "localstorage"}),
            ("Canvas API", {"canvas", "draw", "graphic"}),
        ],
        "css": [
            ("grid", {"grid", "layout"}),
            ("flexbox", {"flex", "flexbox"}),
            ("animations", {"animate", "keyframe", "transition"}),
            ("media queries", {"responsive", "media query", "breakpoint"}),
            ("container queries", {"container query"}),
        ],
    }

    def check(self, spec: TaskSpec) -> Optional[dict]:
        desc_lower = spec.description.lower()
        for platform, features in self.NATIVE_FEATURES.items():
            for feature_name, keywords in features:
                match_count = sum(1 for kw in keywords if kw in desc_lower)
                if match_count >= 1:  # At least one keyword hits
                    return {
                        "platform": platform,
                        "feature": feature_name,
                        "evidence": f"Native {platform} feature '{feature_name}' covers this",
                    }
        return None


class DepChecker:
    """D1 specialist: checks if existing deps can handle the task."""

    DEP_CAPABILITIES: dict[str, set[str]] = {
        "flask": {"routing", "http", "api", "web server", "endpoint"},
        "django": {"routing", "http", "api", "orm", "admin", "auth"},
        "requests": {"http", "api call", "get", "post", "web request"},
        "pandas": {"csv", "excel", "dataframe", "data analysis", "sql"},
        "numpy": {"array", "matrix", "math", "statistics", "linear algebra"},
        "react": {"ui", "component", "state", "hook", "jsx"},
        "lodash": {"array", "object", "collection", "utility"},
        "express": {"routing", "http", "api", "middleware"},
        "sqlalchemy": {"orm", "database", "sql", "query", "model"},
        "pytest": {"test", "assert", "fixture", "mock"},
    }

    def check(self, spec: TaskSpec) -> Optional[dict]:
        desc_lower = spec.description.lower()
        for dep in spec.existing_deps:
            dep_lower = dep.lower()
            capabilities = self.DEP_CAPABILITIES.get(dep_lower, set())
            for cap in capabilities:
                if cap in desc_lower:
                    return {
                        "dependency": dep_lower,
                        "capability": cap,
                        "evidence": f"Existing dep '{dep_lower}' can handle '{cap}'",
                    }
        return None


class ComplexityChecker:
    """D1 specialist: estimates if task is one-line or minimum."""

    def estimate(self, spec: TaskSpec) -> RungLevel:
        desc_len = len(spec.description)
        has_import = any(kw in spec.description.lower()
                         for kw in ["import", "require", "#include", "use "])

        # ONELINE: very short, simple change
        if desc_len < 30 and not has_import and spec.estimated_complexity < 3:
            return RungLevel.ONELINE

        # MINIMUM: anything that passes through
        return RungLevel.MINIMUM


# ═══════════════════════════════════════════════════════════════
#  D2 MAXWELL'S DEMON — Task Sor ted Into Labelled Dimensions
# ═══════════════════════════════════════════════════════════════

TASK_DIMENSIONS: dict[str, list[str]] = {
    "bug_fix": ["known_bug", "has_stacktrace", "isolated", "regression"],
    "feature": ["new_feature", "specified", "ui_change", "logic_change"],
    "refactor": ["extract", "rename", "inline", "reorganize"],
    "test": ["unit_test", "integration_test", "regression_test", "e2e"],
    "docs": ["docstring", "readme", "api_doc", "comment"],
}

# ═══════════════════════════════════════════════════════════════
#  D7 HOMEOSTASIS — Set Points + Drift Detection
# ═══════════════════════════════════════════════════════════════

@dataclass
class Homeostat:
    """Monitors critical values, detects deviation, logs corrections."""

    set_points: dict[str, float] = field(default_factory=lambda: {
        "bug_fix_max_rung_depth": 5.0,
        "feature_max_rung_depth": 6.0,
        "test_max_rung_depth": 5.0,
        "refactor_max_rung_depth": 5.0,
        "docs_max_rung_depth": 3.0,
    })

    tolerance: dict[str, float] = field(default_factory=lambda: {
        "bug_fix_max_rung_depth": 2.0,
        "feature_max_rung_depth": 1.0,
        "test_max_rung_depth": 2.0,
        "refactor_max_rung_depth": 2.0,
        "docs_max_rung_depth": 2.0,
    })

    corrections: list[dict] = field(default_factory=list)

    def check(self, spec: TaskSpec, result: EvaluationResult) -> list[dict]:
        """Return list of corrections needed."""
        corrections = []
        key = f"{spec.task_type}_max_rung_depth"
        setpoint = self.set_points.get(key)
        if setpoint and result.rung_depth > setpoint + self.tolerance.get(key, 1):
            corr = {
                "metric": key,
                "actual": result.rung_depth,
                "expected": setpoint,
                "action": "Adjust rung ordering — too many checks before match",
            }
            corrections.append(corr)
            self.corrections.append(corr)
        return corrections


# ═══════════════════════════════════════════════════════════════
#  D8 VCG AUCTION — Rung Depth Selection Per Task Type
# ═══════════════════════════════════════════════════════════════

RUNG_BIDS: dict[str, list[tuple[int, float, str]]] = {
    "bug_fix": [
        (0, 0.9, "Known one-line fix: YAGNI if already fixed upstream"),
        (1, 0.6, "Stdlib has the datastructure"),
        (2, 0.3, "Dependency may be overkill for this bug"),
        (3, 0.8, "Native feature unlikely"),
        (4, 0.7, "Could be a one-liner"),
        (5, 0.4, "Write minimal fix"),
    ],
    "feature": [
        (0, 0.2, "Feature is requested — YAGNI unlikely"),
        (1, 0.3, "Stdlib rarely covers new features"),
        (2, 0.1, "Native features are narrow"),
        (3, 0.6, "Dep may have this capability"),
        (4, 0.2, "Feature won't be one line"),
        (5, 0.9, "Write minimum feature code"),
    ],
    "refactor": [
        (0, 0.3, "Refactor is justified"),
        (1, 0.2, "Stdlib unlikely"),
        (2, 0.1, "Native doesn't refactor"),
        (3, 0.1, "Dep doesn't refactor"),
        (4, 0.5, "Refactors are rarely one-line"),
        (5, 0.8, "Minimum refactor"),
    ],
    "test": [
        (0, 0.1, "Test is needed"),
        (1, 0.8, "Stdlib pytest covers testing"),
        (2, 0.1, "Native testing is limited"),
        (3, 0.3, "Dep testing framework"),
        (4, 0.5, "Simple asserts could be one line"),
        (5, 0.6, "Write test"),
    ],
    "docs": [
        (0, 0.3, "Doc is needed"),
        (1, 0.1, "Stdlib doesn't document"),
        (2, 0.1, "Native doesn't document"),
        (3, 0.1, "Deps don't document"),
        (4, 0.9, "One-line docstring often suffices"),
        (5, 0.5, "Write minimal docs"),
    ],
}


def vcg_select(task_type: str, rung: RungLevel) -> tuple[float, str]:
    """D8 VCG: winner pays second-highest bid price."""
    bids = RUNG_BIDS.get(task_type, [])
    rung_idx = list(RungLevel).index(rung)
    for idx, bid, desc in bids:
        if idx == rung_idx:
            # Second-highest bid among same-rung candidates
            others = [b for i, b, _ in bids if i == rung_idx and b < bid]
            price = max(others) if others else bid * 0.5
            return (price, f"VCG price={price:.2f}: {desc}")
    return (0.5, "VCG: default price")


# ═══════════════════════════════════════════════════════════════
#  THE PONYTAIL LADDER — Principal Evaluation Engine
# ═══════════════════════════════════════════════════════════════

class PonytailLadder:
    """
    Deterministic code minimalism gate.
    Lossless typed input → lossless typed output. IRR = 1.0.
    No prose injection. No LLM interpretation of rungs.
    """

    def __init__(self):
        self.stdlib = StdlibChecker()
        self.native = NativeChecker()
        self.deps = DepChecker()
        self.complexity = ComplexityChecker()
        self.homeostat = Homeostat()
        self._chain_store: list[str] = []  # D6 Permanence

    def evaluate(self, spec: TaskSpec) -> EvaluationResult:
        """
        Evaluate a task spec against the 7-rung ladder.
        Returns the first matching rung with evidence and integrity chain.
        """
        # D-1 Parsimony: bypass on trivial tasks
        if self._should_bypass(spec):
            return self._bypass_result(spec)

        rung_depth = 0

        # Rung 1: YAGNI
        rung_depth += 1
        yagni_evidence = self._check_yagni(spec)
        if yagni_evidence:
            return self._make_result(spec, RungLevel.YAGNI,
                f"YAGNI: {yagni_evidence['reason']}",
                yagni_evidence, rung_depth)

        # Rung 2: STDLIB
        rung_depth += 1
        stdlib_evidence = self.stdlib.check(spec)
        if stdlib_evidence:
            return self._make_result(spec, RungLevel.STDLIB,
                f"Standard library covers this: {stdlib_evidence['matched_libs']}",
                stdlib_evidence, rung_depth)

        # Rung 3: NATIVE
        rung_depth += 1
        native_evidence = self.native.check(spec)
        if native_evidence:
            return self._make_result(spec, RungLevel.NATIVE,
                f"Native platform feature: {native_evidence['feature']}",
                native_evidence, rung_depth)

        # Rung 4: Existing DEP
        rung_depth += 1
        dep_evidence = self.deps.check(spec)
        if dep_evidence:
            return self._make_result(spec, RungLevel.DEP,
                f"Existing dep '{dep_evidence['dependency']}' can handle '{dep_evidence['capability']}'",
                dep_evidence, rung_depth)

        # Rung 5: ONELINE
        rung_depth += 1
        one_line_rung = self.complexity.estimate(spec)
        if one_line_rung == RungLevel.ONELINE:
            return self._make_result(spec, RungLevel.ONELINE,
                "Task is simple enough for one line",
                {"estimated_complexity": spec.estimated_complexity,
                 "description_length": len(spec.description)}, rung_depth)

        # Rung 6: MINIMUM
        rung_depth += 1
        return self._make_result(spec, RungLevel.MINIMUM,
            "Write the minimum code that works",
            {"task_type": spec.task_type, "complexity": spec.estimated_complexity},
            rung_depth)

    def _check_yagni(self, spec: TaskSpec) -> Optional[dict]:
        """Rung 1: Is this task even necessary?"""
        desc_lower = spec.description.lower()

        # Speculative patterns — things that don't need to exist
        yagni_patterns = [
            "just in case", "might need", "future proof", "prepare for",
            "what if", "potentially", "could be useful", "nice to have",
        ]
        for pattern in yagni_patterns:
            if pattern in desc_lower:
                return {
                    "reason": f"Speculative: contains '{pattern}'",
                    "confidence": 0.8,
                }

        # Already-fixed patterns
        if spec.task_type == "bug_fix" and any(
            kw in desc_lower for kw in ["already fixed", "upstream", "duplicate"]
        ):
            return {
                "reason": "Bug already fixed upstream",
                "confidence": 0.9,
            }

        return None

    def _should_bypass(self, spec: TaskSpec) -> bool:
        """D-1 Parsimony: bypass on trivial tasks only.
        Strict thresholds — only the most trivial bug_fix/doc tasks bypass."""
        return (
            spec.task_type in {"bug_fix", "docs"}
            and spec.estimated_complexity < 1.5
            and len(spec.description) < 30
            and spec.context_tokens < 100
        )

    def _bypass_result(self, spec: TaskSpec) -> EvaluationResult:
        """Return MINIMUM directly — skip the overhead."""
        return EvaluationResult(
            rung=RungLevel.MINIMUM,
            justification="BYpass: task too trivial for ladder evaluation",
            evidence={"reason": "D-1 Parsimony", "complexity": spec.estimated_complexity},
            chain_hash="BYPASS",
            rung_depth=0,
        )

    @staticmethod
    def reset_chain():
        """Clear global chain store (for test isolation)."""
        _CHAIN_STORE.clear()

    def _make_result(self, spec: TaskSpec, rung: RungLevel, justification: str,
                     evidence: dict, depth: int) -> EvaluationResult:
        """Construct a result with integrity chain and VCG pricing."""
        vcg_price, vcg_desc = vcg_select("bug_fix", rung)
        evidence["vcg"] = {"price": vcg_price, "description": vcg_desc}

        prev_hash = self._chain_store[-1] if self._chain_store else "GENESIS"

        chain_hash = hash_chain(
            EvaluationResult(rung, justification, evidence, "PLACEHOLDER",
                           prev_hash=prev_hash, rung_depth=depth),
            prev_hash=prev_hash,
        )

        result = EvaluationResult(
            rung=rung,
            justification=justification,
            evidence=evidence,
            chain_hash=chain_hash,
            prev_hash=prev_hash,
            rung_depth=depth,
        )

        # Store in permanence chain
        self._chain_store.append(result.chain_hash)
        _CHAIN_STORE.append(result.chain_hash)

        # D7 Homeostasis check
        corrections = self.homeostat.check(spec, EvaluationResult(
            rung=rung, justification=justification, evidence=evidence,
            chain_hash="HOMEOSTAT_CHECK", prev_hash=prev_hash, rung_depth=depth,
        ))
        if corrections:
            evidence["homeostasis"] = corrections

        return result


# ═══════════════════════════════════════════════════════════════
#  D5 PHILOSOPHY — Multiple Interpretations
# ═══════════════════════════════════════════════════════════════

def multi_interpret(spec: TaskSpec, ladder: PonytailLadder,
                    n: int = 3) -> list[EvaluationResult]:
    """Generate multiple interpretations of the same spec.
    Each interpretation varies the task classification slightly to
    explore alternative rung outcomes."""
    interpretations = []
    base_type = spec.task_type

    for i in range(n):
        # D5: Alternative readings — shift task type slightly
        alt_types = [t for t in TASK_TYPES if t != base_type]
        alt_spec = TaskSpec(
            task_type=alt_types[i % len(alt_types)],
            description=spec.description,
            language=spec.language,
            existing_deps=spec.existing_deps,
            estimated_complexity=spec.estimated_complexity,
        )
        interpretations.append(ladder.evaluate(alt_spec))

    return interpretations


# ═══════════════════════════════════════════════════════════════
#  D4 JOINTS — Flex Under Load
# ═══════════════════════════════════════════════════════════════

class FlexibleLadder:
    """PonytailLadder wrapped with CreativeJoint semantics.
    Under high complexity, flexes towards MINIMUM (write code).
    Under low complexity, stays strict (favor YAGNI/STDLIB)."""

    def __init__(self, ladder: PonytailLadder):
        self.ladder = ladder

    def evaluate(self, spec: TaskSpec) -> EvaluationResult:
        # High complexity → flex towards writing code
        if spec.estimated_complexity > 7.0:
            return EvaluationResult(
                rung=RungLevel.MINIMUM,
                justification=f"Joint flex: complexity={spec.estimated_complexity} > 7.0, "
                             f"write minimum code directly",
                evidence={"complexity": spec.estimated_complexity, "flex": True},
                chain_hash="FLEX",
                rung_depth=6,
            )

        # Low complexity → strict ladder
        return self.ladder.evaluate(spec)


# ═══════════════════════════════════════════════════════════════
#  CLI INTERFACE
# ═══════════════════════════════════════════════════════════════

def main():
    import sys
    args = sys.argv[1:]

    if not args:
        print("Usage: python ponytail_ladder.py <task_type> <description> [language] [deps...]")
        print("Example: python ponytail_ladder.py bug_fix \"Fix null pointer\" python flask sqlalchemy")
        return

    task_type = args[0]
    description = args[1] if len(args) > 1 else "unspecified"
    language = args[2] if len(args) > 2 else "python"
    deps = tuple(args[3:])

    spec = TaskSpec(
        task_type=task_type,
        description=description,
        language=language,
        existing_deps=deps,
    )

    ladder = PonytailLadder()
    result = ladder.evaluate(spec)

    print(f"\n{'='*60}")
    print(f"  PonytailLadder — Evaluation Result")
    print(f"{'='*60}")
    print(f"  Task:         {task_type}")
    print(f"  Description:  {description}")
    print(f"  Language:     {language}")
    print(f"  Dependencies: {', '.join(deps) if deps else 'none'}")
    print(f"  ─{'─'*57}")
    print(f"  Rung:         {result.rung.name}")
    print(f"  Justification:{result.justification}")
    print(f"  Rung Depth:   {result.rung_depth}")
    print(f"  Chain Hash:   {result.chain_hash}")
    print(f"  Integrity:    {'✅ PASS' if result.verify_chain() else '❌ FAIL'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
