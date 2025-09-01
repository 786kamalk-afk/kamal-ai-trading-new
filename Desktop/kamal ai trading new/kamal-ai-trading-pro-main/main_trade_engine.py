# main_trade_engine.py
import asyncio, yaml, pathlib, signal, time
from utils.logger import get_logger
from order_execution.order_manager import OrderManager
from order_execution.broker_api import BrokerAPIStub
from risk_management.risk_manager import RiskManager

log = get_logger("engine", log_file="logs/engine.log")
CFG = pathlib.Path("config/trading_config.yaml")
config = yaml.safe_load(CFG.read_text()) if CFG.exists() else {}

async def demo_signal_generator(order_mgr: OrderManager):
    """
    Demo generator that emits signals every few seconds (replace with real strategy/AI).
    """
    symbols = ["NIFTY", "RELIANCE", "TCS"]
    i = 0
    while True:
        # produce a signal
        sig = {
            "symbol": symbols[i % len(symbols)],
            "direction": "BUY" if (i % 2 == 0) else "SELL",
            "qty": 1 + (i % 3),
            "stop": 100.0,   # stub values; in real, compute SL price
            "risk_amount": 50.0,
            "meta": {"source": "demo_ai", "ts": time.time()}
        }
        log.info(f"Demo signal emitted: {sig}")
        await order_mgr.queue_order(sig)
        i += 1
        await asyncio.sleep(5)

async def main_loop():
    broker = BrokerAPIStub()
    order_mgr = OrderManager(broker=broker, config=config)
    await order_mgr.start()

    # start demo signal generator (for testing). Replace with real signal feed
    sig_task = asyncio.create_task(demo_signal_generator(order_mgr))

    # handle shutdown
    stop_event = asyncio.Event()
    def _shutdown(*_):
        log.info("Shutdown requested.")
        stop_event.set()
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            asyncio.get_running_loop().add_signal_handler(s, _shutdown)
        except Exception:
            pass

    await stop_event.wait()
    sig_task.cancel()
    await order_mgr.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        log.info("Interrupted by user")
    except Exception as e:
        log.exception("Engine crashed: %s", e)
