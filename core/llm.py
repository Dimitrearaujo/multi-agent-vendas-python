"""Wrapper Claude API — compartilhado por todos os agentes."""
import os
from anthropic import Anthropic

_client = None


def get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def chat(system: str, messages: list[dict], max_tokens: int = 1024) -> str:
    resp = get_client().messages.create(
        model=os.getenv("MODEL", "claude-sonnet-4-6"),
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return resp.content[0].text.strip()
