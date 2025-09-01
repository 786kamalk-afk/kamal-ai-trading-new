from dataclasses import dataclass
from typing import Dict, Any, Optional
import pandas as pd

@dataclass
class Signal:
    side: str
    confidence: float
    symbol: str
    price: float
    meta: Dict[str, Any]

class IntradayStrategy:
    def generate(self, df: pd.DataFrame, symbol: str) -> Optional[Signal]:
        if len(df) < 50:
            return None
        df = df.copy()
        df["ma_fast"] = df["close"].rolling(9).mean()
        df["ma_slow"] = df["close"].rolling(21).mean()
        rsi = self._rsi(df["close"], 14).iloc[-1]
        price = float(df["close"].iloc[-1])
        side = None
        if df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1] and rsi < 70:
            side = "buy"
        elif df["ma_fast"].iloc[-1] < df["ma_slow"].iloc[-1] and rsi > 30:
            side = "sell"
        if side:
            conf = float(max(0.0, min(1.0, 1 - abs(50-rsi)/50)))
            return Signal(side=side, confidence=conf, symbol=symbol, price=price, meta={"rsi": float(rsi)})
        return None

    def _rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / (loss.replace(0, 1e-9))
        return 100 - (100 / (1 + rs))
