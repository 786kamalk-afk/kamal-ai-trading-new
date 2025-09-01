from __future__ import annotations
from typing import Protocol, runtime_checkable

@runtime_checkable
class LLMInterface(Protocol):
    async def explain(self, prompt: str, max_tokens: int = 256) -> str: ...

class RuleBasedExplainer:
    async def explain(self, prompt: str, max_tokens: int = 256) -> str:
        p = prompt.lower()
        if "why buy" in p or "why enter" in p:
            return "Model signals BUY because momentum is positive and risk checks pass."
        if "why sell" in p or "why exit" in p:
            return "Model signals SELL because momentum faded and target reached."
        return "No strong textual explanation could be inferred from the prompt."

class OpenAIAdapter:
    def __init__(self, client=None):
        self.client = client

    async def explain(self, prompt: str, max_tokens: int = 256) -> str:
        try:
            import openai
        except Exception as e:
            raise RuntimeError("OpenAI SDK not available — install openai or use RuleBasedExplainer")
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.1,
        )
        return resp.choices[0].message.content
