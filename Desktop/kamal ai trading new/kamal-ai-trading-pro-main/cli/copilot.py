# cli/copilot.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

# NOTE: adapt these imports to match your repo's module names
# If your functions/classes are named differently, replace accordingly.
try:
    from decision_engine.meta_integration import combine_signals as _combine_signals
except Exception:
    def _combine_signals(symbol): return {"value": 0.5, "reasons": ["stub: no signals"], "confidence": 0.5}

try:
    from decision_engine.scoring import score_signal as _score_signal
except Exception:
    def _score_signal(signals): return {"value": signals.get("value", 0.5), "confidence": signals.get("confidence", 0.5)}

try:
    from risk_management.risk_manager import position_size as _position_size
except Exception:
    def _position_size(**kwargs): return {"qty": 1, "risk_pct": 0.1, "notional": 1000}

try:
    from risk_management.stop_rule_manager import build_stop as _build_stop
except Exception:
    def _build_stop(**kwargs): return {"stop": None, "type": "stub"}

try:
    from order_execution.order_manager import place_order as _place_order
except Exception:
    def _place_order(**kwargs): return {"status": "stub", "order_id": "stub-1"}

@dataclass
class CopilotContext:
    profile: Dict[str, Any]
    policies: Dict[str, Any]

class Copilot:
    def __init__(self, ctx: CopilotContext):
        self.ctx = ctx

    def propose_trade(self, symbol: str, direction: str) -> Dict[str, Any]:
        signals = _combine_signals(symbol)
        score = _score_signal(signals)

        max_risk_pct = self.ctx.profile.get("risk", {}).get("max_single_trade_risk_pct", 0.5)
        size_info = _position_size(symbol=symbol, direction=direction, risk_pct=max_risk_pct)

        stop = _build_stop(symbol=symbol, direction=direction,
                           trailing_multiplier=self.ctx.policies.get("ai_policies", {}).get("defaults", {}).get("sl_trailing_multiplier", 1.5))

        # Determine need for confirmation
        lower_conf = self.ctx.policies.get("ai_policies", {}).get("confirmations", {}).get("confirm_if_confidence_below", 0.7)
        always_confirm = self.ctx.policies.get("ai_policies", {}).get("confirmations", {}).get("always_confirm_real_orders", True)
        needs_confirm = True
        if score.get("confidence", 0) >= lower_conf:
            needs_confirm = always_confirm

        explanation = {
            "reasons": signals.get("reasons", []),
            "score": score,
            "risk": {
                "max_single_trade_risk_pct": max_risk_pct,
                "proposed_size": size_info.get("qty"),
            }
        }

        return {
            "action": "trade_proposal",
            "symbol": symbol,
            "direction": direction,
            "score": score,
            "size": size_info,
            "stop": stop,
            "needs_confirm": needs_confirm,
            "explanation": explanation,
        }

    def execute_order(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        # Here you can add panic_manager or risk checks before executing
        order_res = _place_order(
            symbol=proposal.get("symbol"),
            direction=proposal.get("direction"),
            qty=proposal.get("size", {}).get("qty"),
            stop=proposal.get("stop"),
            tif=self.ctx.policies.get("ai_policies", {}).get("defaults", {}).get("time_in_force", "DAY"),
        )
        return {"status": "submitted", "broker_ref": order_res}
