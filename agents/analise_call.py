"""Agente analise de call — extrai insights de transcricoes de reunioes."""
from __future__ import annotations
from core.llm import chat

SYSTEM = """Voce e um especialista em analise de calls de vendas. Analise a transcricao
e retorne um relatorio estruturado em JSON:

{
  "resumo": "3-4 linhas do que foi discutido",
  "interesse": "alto|medio|baixo",
  "objecoes": ["lista de objecoes levantadas"],
  "dores": ["principais dores identificadas"],
  "orcamento_mencionado": "valor ou null",
  "prazo_mencionado": "prazo ou null",
  "decisor_presente": true/false,
  "proximo_passo": "acao acordada",
  "probabilidade_fechamento": 0-100,
  "recomendacoes": ["3 acoes para aumentar chance de fechamento"]
}"""


def analisar(transcricao: str) -> dict:
    historico = [{"role": "user", "content": f"Analise esta transcricao:\n\n{transcricao}"}]
    resposta = chat(SYSTEM, historico, max_tokens=1024)
    import json, re
    m = re.search(r"\{.*\}", resposta, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"resumo": resposta, "probabilidade_fechamento": 0}
