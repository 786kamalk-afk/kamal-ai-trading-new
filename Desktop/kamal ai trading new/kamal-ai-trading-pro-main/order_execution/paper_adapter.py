from __future__ import annotations
from .broker_base import BrokerInterface, OrderRequest, OrderResponse
from datetime import datetime
from threading import Lock
import uuid

class PaperBroker(BrokerInterface):
    def __init__(self):
        self._orders = {}
        self._positions = {}
        self._lock = Lock()

    def _new_broker_id(self):
        return f"paper-{uuid.uuid4()}"

    def place_order(self, req: OrderRequest) -> OrderResponse:
        with self._lock:
            broker_id = self._new_broker_id()
            filled_qty = req.qty
            avg_price = req.price if req.price is not None else 0.0
            status = "FILLED"
            resp = OrderResponse(
                client_order_id=req.client_order_id,
                broker_order_id=broker_id,
                status=status,
                filled_qty=filled_qty,
                avg_price=avg_price,
                ts=datetime.utcnow(),
                meta={"sim": True},
            )
            self._orders[broker_id] = resp
            pos = self._positions.get(req.symbol, 0.0)
            if req.side.upper() == "BUY": pos += filled_qty
            else: pos -= filled_qty
            self._positions[req.symbol] = pos
            return resp

    def cancel_order(self, broker_order_id: str) -> OrderResponse:
        with self._lock:
            if broker_order_id not in self._orders:
                return OrderResponse(client_order_id="", broker_order_id=broker_order_id, status="UNKNOWN", ts=datetime.utcnow(), meta={})
            o = self._orders[broker_order_id]
            if o.status in ("FILLED","CANCELLED"): return o
            o.status = "CANCELLED"
            return o

    def get_order(self, broker_order_id: str) -> OrderResponse:
        return self._orders.get(broker_order_id)

    def get_positions(self) -> dict:
        return dict(self._positions)
