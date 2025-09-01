AI Extension (starter)

What I added:
- ai/llm_interface.py: LLM adapter pattern + rule-based explainer
- ai/model_manager.py: persistent model wrapper
- ai/feature_store.py: rolling feature computer
- ai/risk_gates.py: AI-friendly risk guardrails
- ai/decision_maker.py: core decision logic that combines model + LLM + risk
- ai/agent.py: AutoTradeAgent glue (subscribes ticks -> decisions -> publishes orders)
- ui/textual_app.py: animated terminal dashboard skeleton (Textual + Rich)

How to wire into existing repo:
1. Place ai/ folder under your package root (next to core/, order_execution/)
2. Ensure `core.events` and `signal_bus` import paths resolve (they should in the patched repo)
3. Start a simple agent in an async task:

    from ai.model_manager import ModelManager
    from ai.agent import AutoTradeAgent
    from ai.risk_gates import AccountSnapshot
    import asyncio

    mm = ModelManager(model=YourTrainedSklearnModel())
    acct = AccountSnapshot(capital=100000, exposure=0.0, per_symbol_exposure={}, max_risk_per_trade=0.02, max_total_exposure=50000, daily_loss=0, max_daily_loss=1000)
    agent = AutoTradeAgent(mm, acct)
    asyncio.create_task(agent.run())

Safety note: Always test in paper mode. Use robust logging, circuit-breakers, and full backtests before any real capital is used.
