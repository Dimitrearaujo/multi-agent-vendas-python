"""Orquestrador — fluxo completo de vendas com os 5 agentes."""
from __future__ import annotations
import os
import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from agents import diagnostico, qualificador, analise_call, orcamento, simulador


def fluxo_diagnostico_interativo() -> None:
    """Modo interativo: diagnostico + qualificacao + proposta."""
    print("=== Agente de Diagnostico ===")
    print("Pressione Ctrl+C para encerrar\n")

    historico: list[dict] = []
    diag_resultado = None

    # Fase 1: Diagnostico
    historico.append({"role": "user", "content": "Ola, pode me contar sobre seu negocio?"})
    while True:
        resultado = diagnostico.run(historico)
        if resultado.get("diagnostico"):
            diag_resultado = resultado["diagnostico"]
            print("\n=== DIAGNOSTICO ===")
            print(json.dumps(diag_resultado, indent=2, ensure_ascii=False))
            break

        pergunta = resultado.get("pergunta", "")
        if not pergunta:
            break

        print(f"\nAgente: {pergunta}")
        resposta = input("Voce: ").strip()
        if not resposta:
            break

        historico.append({"role": "assistant", "content": pergunta})
        historico.append({"role": "user", "content": resposta})

    if not diag_resultado:
        print("Diagnostico incompleto.")
        return

    # Fase 2: Qualificacao BANT
    print("\n=== QUALIFICACAO BANT ===")
    bant = qualificador.qualificar(historico)
    print(json.dumps(bant, indent=2, ensure_ascii=False))

    if bant.get("recomendacao") != "qualificado":
        print(f"\nProspect nao qualificado: {bant.get('proximo_passo', '')}")
        return

    # Fase 3: Orcamento
    print("\n=== GERANDO PROPOSTA ===")
    nome = input("Nome do cliente/empresa: ").strip()
    dados_cliente = {"nome": nome, "segmento": "servicos"}
    proposta = orcamento.gerar(diag_resultado, dados_cliente)
    print(json.dumps(proposta, indent=2, ensure_ascii=False))


def fluxo_analise_call(arquivo_transcricao: str) -> None:
    """Analisa transcricao de reuniao."""
    texto = Path(arquivo_transcricao).read_text(encoding="utf-8")
    print("=== ANALISANDO CALL ===")
    resultado = analise_call.analisar(texto)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


def fluxo_simulador(produto: str = "automacao IA para pequenos negocios") -> None:
    """Treino interativo de objecoes."""
    print("=== SIMULADOR DE OBJECOES ===")
    objecoes = simulador.listar_objecoes()
    for i, obj in enumerate(objecoes, 1):
        print(f"[{i}] {obj}")

    escolha = input("\nEscolha uma objecao (numero) ou digite a sua: ").strip()
    try:
        objecao = objecoes[int(escolha) - 1]
    except (ValueError, IndexError):
        objecao = escolha

    print(f"\nProspect: {simulador.simular_objecao(objecao, produto)}")
    resposta = input("\nSua resposta: ").strip()
    if resposta:
        feedback = simulador.avaliar_resposta(objecao, resposta)
        print(f"\nCoach: {feedback}")


if __name__ == "__main__":
    import sys
    modo = sys.argv[1] if len(sys.argv) > 1 else "diagnostico"

    if modo == "diagnostico":
        fluxo_diagnostico_interativo()
    elif modo == "call" and len(sys.argv) > 2:
        fluxo_analise_call(sys.argv[2])
    elif modo == "simulador":
        produto = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "automacao IA"
        fluxo_simulador(produto)
    else:
        print("Uso:")
        print("  python orchestrator.py diagnostico")
        print("  python orchestrator.py call transcricao.txt")
        print("  python orchestrator.py simulador 'seu produto aqui'")
