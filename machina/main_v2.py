# main_v2.py
# DREAMSWAP — Bootstrap and async pipeline (FIXED)
# All sync stages wrapped in asyncio.to_thread() to prevent event loop starvation.

import asyncio
import time
import traceback

from exchange import stream_ticks
from router import Router
from orbital_module import OrbitalModule
from momentum_module import MomentumModule
from aggregator import Aggregator
from risk import RiskManager
from execution import ExecutionEngine
from journal import Journal
from dashboard import Dashboard


class PipelineReport:
    def __init__(self, tick_timestamp, tick_price):
        self.tick_timestamp = float(tick_timestamp)
        self.tick_price = float(tick_price)
        self.stages = []
        self.trade_executed = False
        self.final_order = None
        self.final_fill = None
        self.exceptions = []
        self.latency_ms = 0.0

    def add_stage(self, stage, decision, reason, details=None):
        self.stages.append({
            "stage": str(stage),
            "decision": str(decision),
            "reason": str(reason),
            "details": details or {},
        })

    def add_exception(self, source, exception):
        self.exceptions.append({
            "source": str(source),
            "error": str(exception),
        })

    def to_dict(self):
        return {
            "tick_timestamp": self.tick_timestamp,
            "tick_price": self.tick_price,
            "stages": self.stages,
            "trade_executed": self.trade_executed,
            "exceptions": self.exceptions,
            "latency_ms": self.latency_ms,
        }


async def main():
    modules = [OrbitalModule(), MomentumModule()]
    router = Router(modules)
    aggregator = Aggregator()
    risk = RiskManager(symbol="BTCUSDT")
    execution = ExecutionEngine(mode="DRY_RUN")
    journal = Journal(db_path="trading_v2.db")
    dashboard = Dashboard(host="0.0.0.0", port=8081)

    dashboard_task = asyncio.create_task(dashboard.start())
    telemetry_interval = 1.0
    last_telemetry_time = 0.0

    try:
        async for tick, exchange_stats in stream_ticks():
            cycle_start = time.time()
            report = PipelineReport(tick.timestamp, tick.price)

            try:
                await asyncio.to_thread(journal.log_tick, tick)

                await asyncio.to_thread(dashboard.broadcast_tick,
                    tick.price, tick.bid, tick.ask, tick.funding_rate,
                    tick.volume, 0.0, "S%d" % router.state)

                outputs, router_reason = await asyncio.to_thread(router.on_tick, tick)
                report.add_stage("router", "processed" if outputs else "filtered", router_reason, {
                    "state": router.state,
                    "output_count": len(outputs),
                })

                for transition in router.telemetry.get_decisions():
                    await asyncio.to_thread(journal.log_router_state,
                        transition["from_state"], transition["to_state"],
                        transition["reason"], transition["details"])

                for o in outputs:
                    await asyncio.to_thread(journal.log_signal, o)

                await asyncio.to_thread(dashboard.broadcast_signals, outputs)

                consensus, aggregator_reason = await asyncio.to_thread(aggregator.aggregate, outputs)
                report.add_stage("aggregator", "consensus" if consensus else "hold", aggregator_reason, {
                    "action": getattr(consensus, "action", 0) if consensus else None,
                    "confidence": getattr(consensus, "confidence", 0.0) if consensus else 0.0,
                })

                if consensus is not None:
                    order, risk_reason = await asyncio.to_thread(risk.evaluate, consensus, tick.price)
                    report.add_stage("risk", "approved" if order else "rejected", risk_reason, {
                        "halted": risk.halted,
                        "drawdown_pct": risk.portfolio.drawdown_pct,
                        "position_quantity": risk.position.quantity,
                    })

                    await asyncio.to_thread(journal.log_risk_decision,
                        "approved" if order else "rejected", risk_reason,
                        getattr(consensus, "module_name", ""),
                        getattr(consensus, "confidence", 0.0),
                        risk.position.quantity,
                        risk.portfolio.total_value,
                        risk.portfolio.drawdown_pct)

                    await asyncio.to_thread(dashboard.broadcast_order, order)

                    if order is not None:
                        fill, execution_reason = await execution.execute(order)
                        report.add_stage("execution", "filled" if fill else "rejected", execution_reason, {
                            "mode": execution.mode,
                        })

                        if fill is not None:
                            report.trade_executed = True
                            report.final_order = order
                            report.final_fill = fill

                            old_qty = risk.position.quantity
                            old_entry = risk.last_trade_entry_price
                            old_stake = risk.last_trade_stake
                            budget_before = risk.reward_budget

                            await asyncio.to_thread(risk.update_position, fill)
                            await asyncio.to_thread(risk.update_portfolio,
                                risk.portfolio.total_value,
                                risk.portfolio.available_margin,
                                risk.portfolio.total_margin)
                            await asyncio.to_thread(router.update_portfolio, risk.portfolio.total_value)

                            await asyncio.to_thread(journal.log_trade, order, fill, risk_reason)
                            await asyncio.to_thread(dashboard.broadcast_fill, fill)

                            await asyncio.to_thread(journal.log_execution_decision,
                                "filled", execution_reason, fill.order_id,
                                execution.telemetry.get_stats().get("avg_latency_ms", 0.0))

                            if old_qty != 0 and risk.position.quantity == 0:
                                realized = risk.reward_budget - budget_before
                                side = "LONG" if old_qty > 0 else "SHORT"
                                await asyncio.to_thread(journal.log_reward_trade,
                                    side, old_entry, fill.price, old_stake,
                                    realized, budget_before, risk.reward_budget)
                                await asyncio.to_thread(dashboard.broadcast_reward_state,
                                    risk.reward_budget, risk.last_trade_entry_price,
                                    risk.last_trade_stake, risk.total_realized_pnl)
                        else:
                            await asyncio.to_thread(journal.log_execution_decision,
                                "rejected", execution_reason)
                else:
                    report.add_stage("risk", "skipped", "no_aggregator_output")

                await asyncio.to_thread(dashboard.broadcast_position, risk.position,
                    risk.last_trade_entry_price, risk.last_trade_stake)
                await asyncio.to_thread(dashboard.broadcast_portfolio, risk.portfolio)
                await asyncio.to_thread(dashboard.broadcast_reward_state,
                    risk.reward_budget, risk.last_trade_entry_price,
                    risk.last_trade_stake, risk.total_realized_pnl)

            except Exception as e:
                error_msg = f"{type(e).__name__}: {e}"
                report.add_exception("main_loop", error_msg)
                await asyncio.to_thread(journal.log_exception, "main_loop", e, {"tick_price": tick.price})
                await asyncio.to_thread(dashboard.broadcast_error, error_msg, "main_loop")
                traceback.print_exc()

            report.latency_ms = (time.time() - cycle_start) * 1000.0
            await asyncio.to_thread(journal.log_pipeline_report, report)
            await asyncio.to_thread(dashboard.broadcast_pipeline_report, report.to_dict())

            now = time.time()
            if now - last_telemetry_time >= telemetry_interval:
                last_telemetry_time = now
                await asyncio.to_thread(dashboard.broadcast_telemetry, "exchange", exchange_stats)
                await asyncio.to_thread(dashboard.broadcast_telemetry, "router", router.telemetry.get_stats())
                await asyncio.to_thread(dashboard.broadcast_telemetry, "aggregator", aggregator.telemetry.get_stats())
                await asyncio.to_thread(dashboard.broadcast_telemetry, "risk", risk.telemetry.get_stats())
                await asyncio.to_thread(dashboard.broadcast_telemetry, "execution", execution.telemetry.get_stats())

    except Exception as e:
        await asyncio.to_thread(journal.log_exception, "main_fatal", e)
        await asyncio.to_thread(dashboard.broadcast_error, f"Fatal: {e}", "main")
        traceback.print_exc()
        raise
    finally:
        dashboard_task.cancel()
        try:
            await dashboard_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[main_v2] Shutdown requested.")
