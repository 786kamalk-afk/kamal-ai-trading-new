from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

class RiskError(Exception): pass

@dataclass
class AccountState:
    capital: float
    exposure: float
    per_symbol_exposure: Dict[str, float]
    max_daily_loss: float
    daily_loss: float

def check_max_risk_per_trade(account: AccountState, order_notional: float, max_risk_per_trade: float):
    if order_notional > account.capital * max_risk_per_trade:
        raise RiskError(f"Order notional {order_notional} exceeds max risk per trade {max_risk_per_trade} of capital {account.capital}")

def check_total_exposure(account: AccountState, incoming_notional: float, max_total_exposure: float):
    if (account.exposure + incoming_notional) > max_total_exposure:
        raise RiskError("Total exposure would exceed allowed maximum")

def check_daily_loss(account: AccountState):
    if account.daily_loss > account.max_daily_loss:
        raise RiskError("Daily loss limit exceeded")
