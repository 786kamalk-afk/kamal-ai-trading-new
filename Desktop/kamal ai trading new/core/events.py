from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

def new_id() -> str:
    return str(uuid4())

@dataclass(frozen=True)
class MarketBar:
    symbol: str
    ts: datetime
    o: float
    h: float
    l: float
    c: float
    v: float

@dataclass(frozen=True)
class Signal:
    id: str
    symbol: str
    ts: datetime
    kind: str
    strength: float
    meta: Dict[str, Any]

@dataclass(frozen=True)
class OrderIntent:
    id: str
    symbol: str
    qty: float
    side: str
    price: Optional[float]
    type: str
    meta: Dict[str, Any]

@dataclass(frozen=True)
class TradeFill:
    order_id: str
    executed_qty: float
    avg_price: float
    ts: datetime
    meta: Dict[str, Any]
