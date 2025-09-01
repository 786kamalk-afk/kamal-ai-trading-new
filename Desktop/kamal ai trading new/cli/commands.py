# cli/commands.py
import typer
from .router import Router
import json

app = typer.Typer(add_completion=False)
router = Router()

@app.command()
def propose(symbol: str, direction: str = typer.Argument(..., help="BUY/SELL")):
    """Propose a trade and print JSON."""
    prop = router.handle("propose", symbol=symbol, direction=direction)
    typer.echo(json.dumps(prop, indent=2))

@app.command()
def execute():
    """Execute the last proposal (demo)."""
    typer.echo("Execution would happen here (use TUI to run).")

if __name__ == "__main__":
    app()
