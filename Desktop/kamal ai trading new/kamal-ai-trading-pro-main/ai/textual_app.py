from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive
import asyncio

class OrdersPanel(Static):
    orders: reactive[list] = reactive([])

    def add_order(self, txt: str):
        self.orders = self.orders + [txt]
        self.update("\n".join(self.orders[-10:]))

class TradingDashboard(App):
    CSS = """
    Screen {
      align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield OrdersPanel(id="orders")
        yield Footer()

    async def on_mount(self) -> None:
        panel = self.query_one(OrdersPanel)
        async def simulate():
            i = 0
            while True:
                panel.add_order(f"[#{i}] sample order at price {100+i}")
                i += 1
                await asyncio.sleep(1.2)
        self.set_timer(0.5, simulate)

if __name__ == "__main__":
    TradingDashboard().run()
