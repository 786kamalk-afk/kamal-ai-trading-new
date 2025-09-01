import asyncio
from core.bus import global_bus
from core.events import Signal, MarketBar, OrderIntent

TOPIC_TICKS = 'ticks'
TOPIC_SIGNALS = 'signals'
TOPIC_ORDERS = 'orders'
TOPIC_FILLS = 'fills'
TOPIC_RISK = 'risk_alerts'

def publish_signal(signal: Signal) -> None:
    asyncio.create_task(global_bus.publish(TOPIC_SIGNALS, signal))

async def publish_signal_sync(signal: Signal) -> None:
    await global_bus.publish(TOPIC_SIGNALS, signal)

def get_signals_queue():
    return global_bus.topic(TOPIC_SIGNALS)

def publish_tick(market_bar: MarketBar) -> None:
    asyncio.create_task(global_bus.publish(TOPIC_TICKS, market_bar))

async def publish_order_intent(order: OrderIntent) -> None:
    await global_bus.publish(TOPIC_ORDERS, order)

async def consume_signals_forever(handler):
    q = get_signals_queue()
    while True:
        sig = await q.get()
        try:
            res = handler(sig)
            if asyncio.iscoroutine(res):
                await res
        finally:
            q.task_done()
