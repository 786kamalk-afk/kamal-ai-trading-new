# main.py
"""
AI Trading Terminal - Main Entrypoint
- Tries to launch the Textual TUI if available (better UX).
- Falls back to a console interactive menu if TUI not available.
- Loads trader profile and AI policy files from profiles/ and config/
- Uses cli.router.Router if present, otherwise uses a safe stub Router.

Save this file at the project root and run:
    python main.py
"""

from __future__ import annotations
import sys
import os
import json
import pathlib
from typing import Any, Dict, Optional

ROOT = pathlib.Path(__file__).parent

# ---- Helpers: load YAML safely ----
def safe_load_yaml(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml
    except Exception:
        # minimal fallback JSON-like loader for simple YAML (best-effort)
        try:
            txt = path.read_text(encoding="utf-8")
            # if file is JSON, parse it
            import json as _json
            return _json.loads(txt)
        except Exception:
            return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return {}

# ---- Router: try to import existing router (preferred) ----
class StubRouter:
    """Safe router stub if cli.router.Router not available"""
    def __init__(self, profile: Dict[str, Any], policies: Dict[str, Any]):
        self.profile = profile
        self.policies = policies
        self._last_proposal = None

    def handle(self, cmd: str, **kw: Any) -> Dict[str, Any]:
        cmd = cmd.lower()
        if cmd == "propose":
            symbol = kw.get("symbol", "NIFTY")
            direction = kw.get("direction", "BUY")
            # simple stub proposal
            prop = {
                "action": "trade_proposal",
                "symbol": symbol,
                "direction": direction,
                "score": {"value": 0.5, "confidence": 0.6},
                "size": {"qty": 1, "risk_pct": 0.1},
                "stop": {"type": "fixed", "stop": None},
                "needs_confirm": True,
                "explanation": {"reasons": ["stub"], "score": {}},
            }
            self._last_proposal = prop
            return prop
        if cmd == "execute":
            proposal = kw.get("proposal") or self._last_proposal
            if not proposal:
                return {"status": "error", "message": "No proposal to execute"}
            # simulate order placement
            return {"status": "submitted", "broker_ref": {"order_id": "stub-123"}}
        raise ValueError(f"Unknown command: {cmd}")

def load_router(profile: Dict[str, Any], policies: Dict[str, Any]):
    try:
        from cli.router import Router as UserRouter  # type: ignore
        r = UserRouter()
        return r
    except Exception:
        return StubRouter(profile, policies)

# ---- Load profile & policies ----
PROFILE_PATH = ROOT / "profiles" / "trader_profile.yaml"
POLICIES_PATH = ROOT / "config" / "ai_policies.yaml"

profile = safe_load_yaml(PROFILE_PATH)
policies = safe_load_yaml(POLICIES_PATH)

router = load_router(profile, policies)

# ---- Utility functions used by both TUI and console ----
def safe_print(msg: str):
    try:
        print(msg)
    except Exception:
        sys.stdout.write(msg + "\n")

def confirm_prompt(prompt: str = "Confirm (y/N): ") -> bool:
    ans = input(prompt).strip().lower()
    return ans in ("y", "yes")

# ---- Core feature implementations (wire these to real logic) ----
def portfolio_view():
    """
    Replace this function to fetch real portfolio data.
    """
    safe_print("\n📊 Portfolio / Account Snapshot\n" + "-" * 40)
    # TODO: connect to users / account module
    # Example placeholders:
    safe_print("Balance: ₹100,000")
    safe_print("Holdings:")
    safe_print(" - NIFTY FUT: 2 lots")
    safe_print(" - RELIANCE: 10 shares")
    safe_print("-" * 40)
    safe_print("Tip: Use Trade -> Propose to get AI suggestions.\n")

def trade_propose_flow():
    safe_print("\n💹 Trade — Propose a new trade")
    symbol = input("Symbol (e.g. NIFTY): ").strip().upper()
    if not symbol:
        safe_print("Aborting: Symbol required.")
        return
    direction = input("Direction [BUY/SELL] (default BUY): ").strip().upper() or "BUY"
    # call router
    try:
        prop = router.handle("propose", symbol=symbol, direction=direction)
    except Exception as e:
        safe_print(f"Error proposing trade: {e}")
        return
    # show proposal summary
    safe_print("\n🔍 Proposal Summary")
    safe_print(f"Symbol: {prop.get('symbol')}")
    safe_print(f"Direction: {prop.get('direction')}")
    score = prop.get("score", {})
    safe_print(f"Score: {score.get('value', 0)} (confidence {score.get('confidence', 0)})")
    size = prop.get("size", {})
    safe_print(f"Suggested quantity: {size.get('qty')}  (risk {size.get('risk_pct')})")
    safe_print(f"Stops: {prop.get('stop')}")
    reasons = prop.get("explanation", {}).get("reasons", [])
    if reasons:
        safe_print("Reasons: " + "; ".join(reasons))
    # Confirmation based on policies & proposal
    needs_confirm = prop.get("needs_confirm", True)
    if needs_confirm:
        safe_print("\n⚠️ This order needs confirmation (policy).")
        ok = confirm_prompt("Place order now? (y/N): ")
        if not ok:
            safe_print("Order cancelled by user.")
            return
    # Execute
    try:
        res = router.handle("execute", proposal=prop)
        safe_print(f"Order Response: {res}")
    except Exception as e:
        safe_print(f"Execution error: {e}")

def trade_menu():
    while True:
        safe_print("\nTrade Menu")
        safe_print("[1] Propose trade (AI)")
        safe_print("[2] Execute last proposal (if any)")
        safe_print("[0] Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            trade_propose_flow()
        elif ch == "2":
            try:
                last = getattr(router, "_last_proposal", None)
                if not last:
                    safe_print("No proposal available. Use 'Propose trade' first.")
                else:
                    ok = confirm_prompt("Execute last proposal now? (y/N): ")
                    if ok:
                        res = router.handle("execute", proposal=last)
                        safe_print(f"Order Response: {res}")
            except Exception as e:
                safe_print(f"Execution error: {e}")
        elif ch == "0":
            return
        else:
            safe_print("Invalid choice. Try again.")

def ai_advice_flow():
    safe_print("\n🤖 AI Advice")
    symbol = input("Symbol (leave empty for general advice): ").strip().upper()
    if not symbol:
        # general advice: call router maybe with a scan
        # If router has a scan method, you could call it; otherwise show placeholder
        safe_print("General advice: Keep positions sized to risk tolerance; review open stops.")
        return
    try:
        prop = router.handle("propose", symbol=symbol, direction="BUY")
        safe_print(f"AI Suggestion for {symbol}: {prop.get('direction')} | score {prop.get('score')}")
        safe_print("Explanation: " + str(prop.get("explanation", {})))
    except Exception as e:
        safe_print(f"AI error: {e}")

def backtest_flow():
    safe_print("\n📈 Backtest (starter)")
    strat = input("Strategy name (e.g. sma_crossover): ").strip()
    if not strat:
        safe_print("No strategy given. Aborting.")
        return
    # TODO: wire to backtesting.backtest_engine
    safe_print(f"Running quick backtest for {strat} (stub) ...")
    safe_print("Result: Return +12% | Max Drawdown -6% (placeholder)")

def config_menu():
    safe_print("\n⚙️ Config")
    safe_print("[1] Show loaded profile")
    safe_print("[2] Show loaded AI policies")
    safe_print("[0] Back")
    ch = input("Choice: ").strip()
    if ch == "1":
        safe_print(json.dumps(profile or {}, indent=2))
    elif ch == "2":
        safe_print(json.dumps(policies or {}, indent=2))
    elif ch == "0":
        return
    else:
        safe_print("Invalid choice.")

def help_guide():
    safe_print("\n📖 Help / Guide\n" + "-" * 40)
    safe_print("Welcome to the AI Trading Terminal.")
    safe_print("Use the number keys to navigate menus. Each menu contains tips.")
    safe_print("Core workflows:")
    safe_print(" - Portfolio: view holdings & balance")
    safe_print(" - Trade: propose (AI) -> confirm -> execute")
    safe_print(" - AI Advice: get suggestions for a symbol")
    safe_print(" - Backtest: run a strategy on historical data")
    safe_print("Safety:")
    safe_print(" - Orders require confirmation based on policies.")
    safe_print(" - Panic rules and daily loss limits are enforced by risk manager (if wired).")
    safe_print("-" * 40 + "\n")

# ---- Console fallback main loop ----
def console_main():
    safe_print("\nStarting AI Trading Terminal (console mode)\n")
    while True:
        safe_print("\n===============================")
        safe_print("     AI Trading Terminal 🚀")
        safe_print("===============================\n")
        safe_print("[1] 📊 Portfolio")
        safe_print("[2] 💹 Trade")
        safe_print("[3] 🤖 AI Advice")
        safe_print("[4] 📈 Backtest")
        safe_print("[5] ⚙️ Config")
        safe_print("[6] 📖 Help / Guide")
        safe_print("[0] ❌ Exit")
        safe_print("-------------------------------")
        choice = input("👉 Select Option: ").strip()
        if choice == "1":
            portfolio_view()
        elif choice == "2":
            trade_menu()
        elif choice == "3":
            ai_advice_flow()
        elif choice == "4":
            backtest_flow()
        elif choice == "5":
            config_menu()
        elif choice == "6":
            help_guide()
        elif choice == "0":
            safe_print("👋 Exiting... Goodbye Trader!")
            return
        else:
            safe_print("❌ Invalid choice. Try again. (Press 6 for Help)")

# ---- Try launching Textual TUI if available ----
def launch_app():
    # Prefer textual TUI if user provided cli.tui.TraderTUI
    try:
        from cli.tui import TraderTUI  # type: ignore
    except Exception:
        TraderTUI = None

    if TraderTUI is not None:
        try:
            # run textual TUI (it handles keyboard, hotkeys, panes)
            TraderTUI().run()
            return
        except Exception as e:
            safe_print(f"Textual TUI failed to start: {e}")
            safe_print("Falling back to console mode.\n")

    # Fallback: console
    console_main()

# ---- Entrypoint ----
if __name__ == "__main__":
    # quick sanity: show where profile/policies loaded from
    safe_print(f"Profile loaded from: {PROFILE_PATH} (exists={PROFILE_PATH.exists()})")
    safe_print(f"Policies loaded from: {POLICIES_PATH} (exists={POLICIES_PATH.exists()})")
    safe_print("Launching terminal... (press Ctrl+C to exit)\n")
    try:
        launch_app()
    except KeyboardInterrupt:
        safe_print("\nInterrupted by user. Exiting.")
    except Exception as exc:
        safe_print(f"Fatal error: {exc}")
        raise
