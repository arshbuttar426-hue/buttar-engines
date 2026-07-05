# Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
# Unauthorized copying, distribution, or use of this work is prohibited.

#!/usr/bin/env python3
"""
================================================================================
FORENSIC INSTRUMENT — MAIN ENGINE
================================================================================
The beating heart. Initializes all organs, runs the cycle, enforces the law.

PILLARS ENFORCED:
All five pillars are enforced by the organs themselves. The engine is just
the conductor — it never bypasses an organ's checks.

FLOW:
1. Config -> 2. Codec -> 3. Ingestion -> 4. Registry -> 5. Feature Factory
-> 6. Validator -> 7. Risk Manager -> 8. Telemetry
================================================================================
"""

import os, sys, time, signal
from typing import Dict, List, Optional, Any

# Ensure organs are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from organs.config_loader import ConfigLoader, ParamClass
from organs.forensic_codec import ForensicCodec, FrozenCodecError, AnchorMismatchError
from organs.ingestion_gateway import IngestionGateway
from organs.collision_registry import CollisionRegistry
from organs.feature_factory import FeatureFactory
from organs.forensic_validator import ForensicValidator
from organs.risk_manager import RiskManager, PositionSignal, OrderSide
from organs.rederivation_protocol import RederivationProtocol
from organs.telemetry import Telemetry

# ------------------------------------------------------------------------------
# ENGINE
# ------------------------------------------------------------------------------

class ForensicEngine:
    """
    Main orchestrator. One instance = one instrument.
    """

    def __init__(self, config_path: str = "config.json"):
        self.config = ConfigLoader(config_path)
        self.telemetry: Optional[Telemetry] = None

        # Initialize organs in dependency order
        self._init_codec()
        self._init_ingestion()
        self._init_registry()
        self._init_factory()
        self._init_validator()
        self._init_risk()
        self._init_rederivation()
        self._init_telemetry()

        self._running = False
        self._cycle_count = 0

    def _init_codec(self):
        """Initialize the sealed vault."""
        try:
            self.codec = ForensicCodec()
            print("[ENGINE] Codec initialized: " + self.codec.fingerprint)
            print("[ENGINE] Formula: " + self.codec.formula_str)
            print("[ENGINE] Anchors verified -- codec ACTIVE")
        except AnchorMismatchError as e:
            print("[ENGINE] CODEC ANCHOR MISMATCH: " + str(e))
            print("[ENGINE] System cannot start. Re-derivation required.")
            raise

    def _init_ingestion(self):
        """Initialize the airlock."""
        rate_limit = self.config.get("ingestion_rate_limit", 100)
        quarantine_max = self.config.get("quarantine_max_size", 100)
        self.gateway = IngestionGateway(self.codec, rate_limit, quarantine_max)
        print("[ENGINE] Ingestion gateway ready (rate_limit=" + str(rate_limit) + "/min)")

    def _init_registry(self):
        """Initialize collision-aware registry."""
        self.registry = CollisionRegistry(self.codec)
        print("[ENGINE] Collision registry ready")

    def _init_factory(self):
        """Initialize feature factory."""
        self.factory = FeatureFactory(self.codec, self.registry)
        print("[ENGINE] Feature factory ready")

    def _init_validator(self):
        """Initialize forensic validator."""
        min_acc = self.config.get("min_accuracy", 0.505)
        lambda_c = self.config.get("lambda_complexity", 0.3)
        max_formulas = self.config.get("max_formulas", 3000)

        self.validator = ForensicValidator(
            self.codec, self.registry, self.factory,
            min_accuracy=min_acc,
            lambda_complexity=lambda_c,
            balance_groups=True,
            max_formulas=max_formulas,
        )
        print("[ENGINE] Validator ready (min_acc=" + str(min_acc) + ", max_formulas=" + str(max_formulas) + ")")

    def _init_risk(self):
        """Initialize risk manager."""
        kelly = self.config.get("kelly_fraction", 0.5)
        max_pos = self.config.get("max_position", 0.20)
        tx_cost = self.config.get("transaction_cost", 0.0004)
        cb_dd = self.config.get("circuit_breaker_drawdown", -0.15)
        commit = self.config.get("commit_threshold", 0.0005)

        self.risk = RiskManager(
            self.codec, self.factory,
            kelly_fraction=kelly,
            max_position=max_pos,
            transaction_cost=tx_cost,
            circuit_breaker_drawdown=cb_dd,
            commit_threshold=commit,
        )
        print("[ENGINE] Risk manager ready (kelly=" + str(kelly) + ", max_pos=" + str(max_pos) + ")")

    def _init_rederivation(self):
        """Initialize re-derivation protocol."""
        self.rederivation = RederivationProtocol(self.codec)
        print("[ENGINE] Re-derivation protocol ready")

    def _init_telemetry(self):
        """Initialize telemetry."""
        log_dir = self.config.get("log_dir", "./logs")
        max_log_mb = self.config.get("max_log_size_mb", 100)

        self.telemetry = Telemetry(self.codec, log_dir, max_log_mb)
        self.telemetry.verified_log(
            "ENGINE", "INIT", "Forensic engine initialized",
            {
                "codec_fingerprint": self.codec.fingerprint,
                "codec_version": self.codec.version,
                "config_version": self.config.version,
            }
        )
        print("[ENGINE] Telemetry ready (log_dir=" + log_dir + ")")

    def ingest_symbol(self, symbol: str, corners: tuple,
                      known_value: Optional[float] = None,
                      source_id: str = "manual") -> Dict:
        """
        Ingest a single symbol through the full pipeline.

        Returns the complete forensic record.
        """
        # 1. Ingestion gateway
        record = self.gateway.ingest(symbol, corners, known_value, source_id)

        # 2. Register in collision registry
        if record.status.name == "ACCEPTED":
            self.registry.register(symbol, corners, known_value)

        # 3. Log
        if self.telemetry:
            self.telemetry.verified_log(
                "INGESTION", record.status.name,
                "Symbol " + symbol + " ingested",
                {
                    "symbol": symbol,
                    "corners": corners,
                    "codec_value": record.codec_value,
                    "group_id": record.collision_group_id,
                    "quality": record.quality,
                }
            )

        return {
            "record": record,
            "registry_stats": self.registry.get_stats(),
            "gateway_stats": self.gateway.get_stats(),
        }

    def validate(self, dataset: List[tuple]) -> Dict:
        """
        Run validation cycle on a dataset.

        dataset: List of (symbol, corners, target_value)
        """
        result = self.validator.evaluate(dataset)

        if self.telemetry:
            self.telemetry.verified_log(
                "VALIDATOR", "CYCLE_COMPLETE",
                "Validation cycle " + str(result.cycle) + " complete",
                {
                    "cycle": result.cycle,
                    "formulas_evaluated": result.formulas_evaluated,
                    "formulas_passed": result.formulas_passed,
                    "pareto_size": len(result.pareto_front),
                    "anchored_present": result.anchored_present,
                    "best_mse": result.best_mse,
                    "best_formula": result.best_formula_id,
                }
            )

        return {
            "result": result,
            "pareto_formulas": [
                {
                    "id": c.formula_id,
                    "expr": c.expression,
                    "mse": c.mse,
                    "accuracy": c.accuracy,
                    "anchored": c.is_anchored,
                }
                for c in result.pareto_front
            ],
        }

    def predict(self, symbol: str, corners: tuple,
                current_price: float,
                volatility: float = 0.01) -> Dict:
        """
        Full prediction pipeline: validator -> risk manager.
        """
        # 1. Validator ensemble prediction
        pred = self.validator.predict(symbol, corners)

        # 2. Build position signal
        signal = PositionSignal(
            prediction=pred["prediction"],
            confidence=pred["confidence"],
            ensemble_size=pred["ensemble_size"],
            collision_group_id=self.codec.get_collision_group(corners)["group_id"],
            symbol=symbol,
        )

        # 3. Risk evaluation
        decision = self.risk.evaluate_signal(signal, current_price, volatility)

        if self.telemetry:
            self.telemetry.verified_log(
                "RISK", "SIGNAL_EVALUATED",
                "Risk decision for " + symbol,
                {
                    "symbol": symbol,
                    "prediction": pred["prediction"],
                    "confidence": pred["confidence"],
                    "side": decision.side.name,
                    "size": decision.size,
                    "allowed": decision.allowed,
                    "reason": decision.reason,
                }
            )

        return {
            "prediction": pred,
            "signal": signal,
            "risk_decision": decision,
            "allowed": decision.allowed,
        }

    def health_check(self) -> Dict:
        """Full system health check."""
        return {
            "codec": {
                "frozen": self.codec.is_frozen(),
                "fingerprint": self.codec.fingerprint,
                "version": self.codec.version,
            },
            "registry": self.registry.get_stats(),
            "gateway": self.gateway.get_stats(),
            "factory": self.factory.check_codec_health(),
            "validator": self.validator.check_health(),
            "risk": self.risk.get_stats(),
            "telemetry": self.telemetry.get_stats() if self.telemetry else {},
            "config": {
                "version": self.config.version,
                "fingerprint": self.config.fingerprint,
            },
        }

    def get_status(self) -> str:
        """One-line status."""
        h = self.health_check()
        if h["codec"]["frozen"]:
            return "FROZEN -- Codec alarm active"
        if h["risk"]["circuit_broken"]:
            return "CIRCUIT BROKEN -- Risk halt"
        return "ACTIVE -- Cycle " + str(self._cycle_count) + ", Pareto " + str(h["validator"]["pareto_size"]) + " formulas"

# ------------------------------------------------------------------------------
# CLI ENTRY POINT
# ------------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("FORENSIC INSTRUMENT v1.0.0-constitution")
    print("=" * 60)

    # Ensure env vars
    if not os.environ.get("FORENSIC_CONFIG_KEY"):
        print("ERROR: FORENSIC_CONFIG_KEY not set")
        sys.exit(1)

    engine = ForensicEngine()
    print("")
    print(engine.get_status())
    print("")
    print("Engine ready. Use engine.ingest_symbol(), engine.validate(), engine.predict()")

    return engine

if __name__ == "__main__":
    engine = main()
