# cli/tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, DataTable
from textual.containers import Horizontal, Vertical
from datetime import datetime
from .router import Router

class TraderTUI(App):
    CSS_PATH = None
    BINDINGS = [
        ("b", "buy_market", "Buy Market"),
        ("s", "sell_market", "Sell Market"),
        ("/", "toggle_chat", "Chat"),
        ("X", "close_all", "Flatten"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical():
                self.signals = DataTable(id="signals")
                yield self.signals
                self.log = Static("", id="log")
                yield self.log
            self.chat = Input(placeholder="Ask AI: e.g. propose BUY NIFTY", id="chat")
            yield self.chat
        yield Footer()

    def on_mount(self):
        self.router = Router()
        self.signals.add_columns("Time", "Symbol", "Dir", "Score", "Confidence")
        self.log_update("Ready. Press '/' to chat.")

    def log_update(self, msg: str):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log.update(f"[{stamp}] {msg}\n" + str(self.log.renderable))

    async def action_toggle_chat(self):
        await self.set_focus(self.chat)

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        q = message.value.strip()
        if not q:
            return
        try:
            parts = q.split()
            if parts[0].lower() == "propose":
                direction = parts[1].upper()
                symbol = parts[2].upper()
                prop = self.router.handle("propose", direction=direction, symbol=symbol)
                self._last_proposal = prop
                score_val = prop.get('score', {}).get('value', 0)
                conf = prop.get('score', {}).get('confidence', 0)
                self.signals.add_row(datetime.now().strftime("%H:%M:%S"), symbol, direction, f"{score_val:.2f}", f"{conf:.2f}")
                self.log_update(f"AI proposes {direction} {symbol} | size={prop['size'].get('qty')} | needs_confirm={prop['needs_confirm']}")
            elif parts[0].lower() == "execute":
                res = self.router.handle("execute", proposal=getattr(self, "_last_proposal", {}))
                self.log_update(f"Order: {res}")
            else:
                self.log_update("Unknown command. Try: 'propose BUY NIFTY' then 'execute'")
        except Exception as e:
            self.log_update(f"Error: {e}")

    async def action_buy_market(self):
        symbol = "NIFTY"
        prop = self.router.handle("propose", direction="BUY", symbol=symbol)
        self._last_proposal = prop
        self.log_update(f"Hotkey BUY propose {symbol} done.")

    async def action_sell_market(self):
        symbol = "NIFTY"
        prop = self.router.handle("propose", direction="SELL", symbol=symbol)
        self._last_proposal = prop
        self.log_update(f"Hotkey SELL propose {symbol} done.")

    async def action_close_all(self):
        self.log_update("Close all requested (wire to order_manager flatten) …")
