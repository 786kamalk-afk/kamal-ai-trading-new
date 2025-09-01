# cli/router.py
from typing import Dict, Any
from .copilot import Copilot, CopilotContext
import yaml, pathlib

PROFILE = pathlib.Path("profiles/trader_profile.yaml")
POLICIES = pathlib.Path("config/ai_policies.yaml")

class Router:
    def __init__(self):
        if PROFILE.exists():
            with open(PROFILE, "r", encoding="utf-8") as fh:
                profile = yaml.safe_load(fh)
        else:
            profile = {}
        if POLICIES.exists():
            with open(POLICIES, "r", encoding="utf-8") as fh:
                policies = yaml.safe_load(fh)
        else:
            policies = {}
        self.copilot = Copilot(CopilotContext(profile, policies))

    def handle(self, cmd: str, **kw: Any) -> Dict[str, Any]:
        cmd = cmd.lower().strip()
        if cmd == "propose":
            return self.copilot.propose_trade(symbol=kw["symbol"], direction=kw["direction"])
        if cmd == "execute":
            return self.copilot.execute_order(kw["proposal"])
        raise ValueError(f"Unknown command: {cmd}")
