from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import List, Literal, Dict, Any
import yaml

class SignalDef(BaseModel):
    name: str
    source: Literal['ohlc','ticker','orderbook']
    params: Dict[str, Any] = Field(default_factory=dict)

class Profile(BaseModel):
    broker: Literal['paper','kite','fyers','ib','ccxt']
    symbols: List[str]
    capital: float
    max_risk_per_trade: float = 0.01

    @model_validator(mode='before')
    def validate_capital(cls, values):
        cap = values.get('capital')
        if cap is None:
            raise ValueError('profile.capital is required')
        try:
            cap = float(cap)
        except Exception:
            raise ValueError('profile.capital must be a number')
        if cap <= 0:
            raise ValueError('profile.capital must be > 0')
        values['capital'] = cap
        return values

class Settings(BaseModel):
    signals: List[SignalDef]
    profile: Profile

def load_settings(path: str) -> Settings:
    with open(path, 'r', encoding='utf-8') as fh:
        raw = yaml.safe_load(fh)
    return Settings.model_validate(raw)
