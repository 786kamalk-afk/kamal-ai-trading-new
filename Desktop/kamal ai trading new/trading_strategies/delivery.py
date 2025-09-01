from dataclasses import dataclass
from typing import Dict, Any, Optional
import pandas as pd

@dataclass
class SwingSignal:
    side: str
    confidence: float
    symbol: str
    entry: float
    stop: float
    target: float
    meta: Dict[str, Any]

class DeliveryStrategy:
    def generate(self, df: pd.DataFrame, symbol: str) -> Optional[SwingSignal]:
        if len(df) < 100:
            return None
        df = df.copy()
        high_20 = df["high"].rolling(20).max().iloc[-2]
        low_20 = df["low"].rolling(20).min().iloc[-2]
        atr = self._atr(df, 14).iloc[-1]
        price = float(df["close"].iloc[-1])
        if price > high_20:
            side = "buy"
            entry = price
            stop = price - 2 * atr
            target = price + 4 * atr
        elif price < low_20:
            side = "sell"
            entry = price
            stop = price + 2 * atr
            target = price - 4 * atr
        else:
            return None
        conf = 0.6
        return SwingSignal(side=side, confidence=conf, symbol=symbol, entry=entry, stop=stop, target=target, meta={"atr": float(atr)})

    def _atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean()
