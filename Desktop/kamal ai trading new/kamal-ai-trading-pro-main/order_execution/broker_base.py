from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional
from datetime import datetime

@dataclass
class OrderRequest:
    client_order_id: str
    symbol: str
    qty: float
    side: str
    type: str
    price: Optional[float] = None
    meta: Dict[str, Any] = None

@dataclass
class OrderResponse:
    client_order_id: str
    broker_order_id: Optional[str]
    status: str
    filled_qty: float = 0.0
    avg_price: Optional[float] = None
    ts: datetime = datetime.utcnow()
    meta: Dict[str, Any] = None

class BrokerInterface(Protocol):
    def place_order(self, req: OrderRequest) -> OrderResponse: ...
    def cancel_order(self, broker_order_id: str) -> OrderResponse: ...
    def get_order(self, broker_order_id: str) -> OrderResponse: ...
    def get_positions(self) -> Dict[str, Any]: ...
