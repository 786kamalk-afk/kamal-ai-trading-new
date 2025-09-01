# tests/test_cli_smoke.py
import pytest
from cli.router import Router

def test_profile_and_policies_load():
    r = Router()
    assert r.copilot.ctx.profile is not None
    assert isinstance(r.copilot.ctx.policies, dict)
