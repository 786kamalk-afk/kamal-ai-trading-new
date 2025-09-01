from __future__ import annotations
from typing import Dict
from dataclasses import dataclass

class RiskError(Exception):
    pass

@dataclass
class AccountSnapshot:
    capital: float
    exposure: float
    per_symbol_exposure: Dict[str, float]
    max_risk_per_trade: float
    max_total_exposure: float
    daily_loss: float
    max_daily_loss: float

def gate_pretrade(account: AccountSnapshot, notional: float) -> None:
    if notional > account.capital * account.max_risk_per_trade:
        raise RiskError("pretrade: exceed per-trade risk cap")
    if (account.exposure + notional) > account.max_total_exposure:
        raise RiskError("pretrade: total exposure breach")
    if account.daily_loss > account.max_daily_loss:
        raise RiskError("pretrade: daily loss breached")
