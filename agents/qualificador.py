"""Agente qualificador BANT — Budget, Authority, Need, Timeline."""
from __future__ import annotations
from core.llm import chat

SYSTEM = """Voce e um especialista em qualificacao de leads usando o framework BANT.
Avalie cada dimensao com base na conversa:

- Budget (Orcamento): O prospect tem verba disponivel?
- Authority (Autoridade): Esta falando com o decisor?
- Need (Necessidade): O problema e real e urgente?
- Timeline (Prazo): Quer resolver em quanto tempo?

Retorne JSON:
{
  "score": 0-100,
  "bant": {
    "budget": {"score": 0-25, "observacao": "..."},
    "authority": {"score": 0-25, "observacao": "..."},
    "need": {"score": 0-25, "observacao": "..."},
    "timeline": {"score": 0-25, "observacao": "..."}
  },
  "recomendacao": "qualificado|nutrir|desqualificar",
  "proximo_passo": "..."
}"""


def qualificar(historico: list[dict]) -> dict:
    resposta = chat(SYSTEM, historico, max_tokens=512)
    import json, re
    m = re.search(r"\{.*\}", resposta, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"score": 0, "recomendacao": "nutrir", "proximo_passo": resposta}
