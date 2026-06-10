"""Agente simulador de objecoes — treina vendedores contra objecoes comuns."""
from __future__ import annotations
from core.llm import chat

OBJECOES_COMUNS = [
    "Ta caro, nao tenho orcamento agora",
    "Preciso pensar mais antes de decidir",
    "Ja tenho uma solucao parecida",
    "Nao sei se isso funciona para o meu negocio",
    "Meu socio precisa aprovar primeiro",
    "Pode me mandar um email com mais detalhes",
]

SYSTEM_PROSPECT = """Voce e um prospect (cliente potencial) cético e resistente.
Levante objecoes realistas baseadas na sua situacao. Seja direto e um pouco desconfiado,
como um dono de negocio ocupado que nao quer perder tempo."""

SYSTEM_COACH = """Voce e um coach de vendas especialista. Avalie a resposta do vendedor
a objecao do prospect e de feedback construtivo:

1. O que foi bom na resposta
2. O que poderia melhorar
3. Uma resposta modelo para essa objecao

Seja objetivo e pratico. Max 200 palavras."""


def simular_objecao(objecao: str, contexto_produto: str) -> str:
    historico = [
        {"role": "user", "content": f"Produto: {contexto_produto}\nObjecao: {objecao}"},
    ]
    return chat(SYSTEM_PROSPECT, historico, max_tokens=200)


def avaliar_resposta(objecao: str, resposta_vendedor: str) -> str:
    historico = [
        {"role": "user", "content": f"Objecao: {objecao}\nResposta do vendedor: {resposta_vendedor}"},
    ]
    return chat(SYSTEM_COACH, historico, max_tokens=400)


def listar_objecoes() -> list[str]:
    return OBJECOES_COMUNS
