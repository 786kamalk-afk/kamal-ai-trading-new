import pytest
import datetime
from core.events import new_id, Signal
from signal_bus import publish_signal, get_signals_queue
from ai.decision_maker import decide_action

@pytest.mark.asyncio
async def test_signal_to_decision():
    # Create a dummy signal
    sig = Signal(
        id=new_id(),
        symbol="AAPL",
        ts=datetime.datetime.utcnow(),
        kind="BUY_TEST",
        strength=0.9,
        meta={}
    )
    publish_signal(sig)

    q = get_signals_queue()
    got = await q.get()
    assert got.symbol == "AAPL"

    # Pass signal into AI decision maker
    action = decide_action([got])
    assert action in ["BUY", "SELL", "HOLD"]
