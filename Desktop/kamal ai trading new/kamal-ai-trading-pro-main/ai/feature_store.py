from __future__ import annotations
from collections import deque
from typing import Deque, Dict, List

class RollingFeatureComputer:
    def __init__(self, window_sizes: List[int] = [3, 8, 21]):
        self.windows: Dict[int, Deque[float]] = {w: deque(maxlen=w) for w in window_sizes}

    def update(self, price: float):
        for q in self.windows.values():
            q.append(price)

    def features(self) -> Dict[str, float]:
        out = {}
        for w, q in self.windows.items():
            if len(q) == 0:
                out[f"ma_{w}"] = 0.0
            else:
                out[f"ma_{w}"] = sum(q) / len(q)
        if len(self.windows[next(iter(self.windows))]) > 0:
            last = next(iter(self.windows.values()))[-1]
            out["momentum_8"] = last - out.get("ma_8", last)
        else:
            out["momentum_8"] = 0.0
        return out
