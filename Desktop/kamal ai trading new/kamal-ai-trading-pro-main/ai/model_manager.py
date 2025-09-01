from __future__ import annotations
from typing import Any
import joblib, os

class ModelManager:
    def __init__(self, model=None, model_path: str | None = None):
        self.model = model
        self.model_path = model_path

    def train(self, X, y):
        assert hasattr(self.model, "fit"), "model must implement fit"
        self.model.fit(X, y)

    def predict_proba(self, X):
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        preds = self.model.predict(X)
        return [[1 - p, p] for p in preds]

    def save(self, path: str | None = None):
        path = path or self.model_path
        if not path:
            raise ValueError("model_path not provided")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)

    def load(self, path: str | None = None):
        path = path or self.model_path
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Model not found: {path}")
        self.model = joblib.load(path)
        return self.model
