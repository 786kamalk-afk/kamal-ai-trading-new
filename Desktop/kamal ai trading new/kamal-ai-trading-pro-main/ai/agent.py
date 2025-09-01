from __future__ import annotations
import asyncio
from core.bus import global_bus
from core.events import MarketBar, Signal, OrderIntent
from signal_bus import publish_order_intent, get_signals_queue, TOPIC_TICKS
from ai.decision_maker import DecisionMaker
from ai.model_manager import ModelManager
from ai.llm_interface import RuleBasedExplainer
from ai.risk_gates import AccountSnapshot

class AutoTradeAgent:
    def __init__(self, model_manager: ModelManager, account: AccountSnapshot):
        self.model_manager = model_manager
        self.decision_maker = DecisionMaker(model_manager, RuleBasedExplainer())
        self.account = account
        self._running = False

    async def handle_tick(self, bar: MarketBar):
        res = await self.decision_maker.decide_from_price(bar.symbol, bar.c, self.account)
        if res.get("decision") == "ok":
            order: OrderIntent = res["order"]
            await publish_order_intent(order)

    async def run(self):
        q = global_bus.topic(TOPIC_TICKS)
        self._running = True
        while self._running:
            bar = await q.get()
            try:
                await self.handle_tick(bar)
            finally:
                q.task_done()

    def stop(self):
        self._running = False
