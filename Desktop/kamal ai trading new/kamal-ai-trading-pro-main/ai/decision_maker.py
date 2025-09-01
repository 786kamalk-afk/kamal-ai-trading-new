from __future__ import annotations
from typing import Any, Dict
from core.events import OrderIntent, new_id
from ai.feature_store import RollingFeatureComputer
from ai.model_manager import ModelManager
from ai.llm_interface import LLMInterface, RuleBasedExplainer
from ai.risk_gates import gate_pretrade, AccountSnapshot, RiskError

class DecisionMaker:
    def __init__(self, model_manager: ModelManager, llm: LLMInterface | None = None):
        self.model_manager = model_manager
        self.llm = llm or RuleBasedExplainer()
        self.featureer = RollingFeatureComputer()

    async def decide_from_price(self, symbol: str, price: float, account: AccountSnapshot) -> Dict[str, Any]:
        self.featureer.update(price)
        feats = self.featureer.features()
        try:
            score = float(self.model_manager.predict_proba([list(feats.values())])[0][1])
        except Exception:
            score = 0.0
        desired_notional = account.capital * 0.02 * score
        try:
            gate_pretrade(account, desired_notional)
        except RiskError as e:
            return {"decision": "blocked", "reason": str(e), "score": score, "feats": feats}
        prompt = f"Explain concisely why a trade with symbol={symbol}, price={price}, features={feats}, score={score} is a good idea."
        explanation = await self.llm.explain(prompt)
        order = OrderIntent(id=new_id(), symbol=symbol, qty=round(desired_notional / (price if price>0 else 1), 6), side="BUY" if score>0.5 else "SELL", price=None, type="MARKET", meta={"score": score, "explanation": explanation})
        return {"decision": "ok", "order": order, "explanation": explanation, "score": score, "feats": feats}
