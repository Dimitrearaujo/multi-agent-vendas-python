"""Agente diagnostico — identifica o maior problema do empreendedor."""
from __future__ import annotations
from core.llm import chat

SYSTEM = """Voce e um especialista em diagnostico de negocios. Sua missao e identificar
com precisao o MAIOR problema que esta impedindo o crescimento do negocio do prospect.

Faca perguntas abertas e objetivas. Apos 3-5 respostas, sintetize o diagnostico em:
1. Problema principal (1 linha)
2. Causa raiz provavel
3. Impacto estimado (receita perdida, clientes perdidos, etc.)
4. Urgencia (alta/media/baixa)

Responda em JSON: {"pergunta": "...", "diagnostico": null}
Quando tiver informacao suficiente: {"pergunta": null, "diagnostico": {...}}"""


def run(historico: list[dict]) -> dict:
    resposta = chat(SYSTEM, historico, max_tokens=512)
    import json, re
    m = re.search(r"\{.*\}", resposta, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"pergunta": resposta, "diagnostico": None}
