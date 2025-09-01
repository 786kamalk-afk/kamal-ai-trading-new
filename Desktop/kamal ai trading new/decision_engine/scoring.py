"""Auto-generated stub for decision_engine/scoring.py\nCreated 2025-08-29 12:00:30.\nReplace with real logic.\n"""
def score_signal(features: dict) -> float:
    return min(1.0, max(0.0, features.get("strength", 0.5)))
