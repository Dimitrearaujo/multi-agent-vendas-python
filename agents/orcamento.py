"""Agente gerador de orcamento — monta proposta comercial personalizada."""
from __future__ import annotations
from core.llm import chat
from datetime import datetime

SYSTEM = """Voce e um especialista em propostas comerciais. Com base no diagnostico
e nas informacoes do cliente, monte uma proposta clara e persuasiva.

Retorne JSON:
{
  "titulo": "Titulo da proposta",
  "cliente": "Nome do cliente/empresa",
  "data": "DD/MM/YYYY",
  "problema_identificado": "...",
  "solucao_proposta": "...",
  "entregaveis": ["lista do que sera entregue"],
  "investimento": {
    "setup": 0,
    "mensalidade": 0,
    "total_3_meses": 0
  },
  "roi_estimado": "...",
  "prazo_implantacao": "...",
  "validade_proposta": "7 dias",
  "cta": "Frase de chamada para acao"
}"""


def gerar(diagnostico: dict, dados_cliente: dict) -> dict:
    contexto = (
        f"Diagnostico do cliente:\n{diagnostico}\n\n"
        f"Dados do cliente:\n{dados_cliente}\n\n"
        f"Data atual: {datetime.now().strftime('%d/%m/%Y')}"
    )
    historico = [{"role": "user", "content": contexto}]
    resposta = chat(SYSTEM, historico, max_tokens=1024)
    import json, re
    m = re.search(r"\{.*\}", resposta, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"titulo": "Proposta Comercial", "cta": resposta}
