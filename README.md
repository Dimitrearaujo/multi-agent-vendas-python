# Multi-Agent Vendas Python

![CI](https://github.com/Dimitrearaujo/multi-agent-vendas-python/actions/workflows/ci.yml/badge.svg)

Sistema multi-agente para automacao do processo comercial: 5 agentes IA especializados que operam em sequencia, do diagnostico ao fechamento.

## Agentes

| Agente | Missao |
|---|---|
| `diagnostico.py` | Identifica o maior problema do negocio via perguntas abertas |
| `qualificador.py` | Avaliacao BANT (Budget, Authority, Need, Timeline) com score 0-100 |
| `analise_call.py` | Extrai insights de transcricoes de reunioes |
| `orcamento.py` | Gera proposta comercial personalizada baseada no diagnostico |
| `simulador.py` | Treino de objecoes — prospect IA + coach que avalia suas respostas |

## Fluxo

```
Lead novo
    |
diagnostico.py
(3-5 perguntas)
    |
qualificador.py
(BANT score)
    |
score >= 60? ──NAO──> nutrir / desqualificar
    |
   SIM
    |
orcamento.py
(proposta JSON)
    |
analise_call.py ←── transcricao da reuniao
    |
simulador.py ←── treino pre-call
```

## Instalacao

```bash
git clone https://github.com/Dimitrearaujo/multi-agent-vendas-python
cd multi-agent-vendas-python
pip install -r requirements.txt

cp .env.example .env
# Edite .env com sua chave Anthropic
```

## Uso

```bash
# Fluxo completo interativo: diagnostico + BANT + proposta
python orchestrator.py diagnostico

# Analisar transcricao de reuniao
python orchestrator.py call reuniao.txt

# Treino de objecoes
python orchestrator.py simulador "automacao IA para clinicas"
```

## Uso dos agentes individualmente

```python
from agents import diagnostico, qualificador, orcamento

# Diagnostico
historico = [{"role": "user", "content": "Tenho uma clinica vet com 3 funcionarios"}]
resultado = diagnostico.run(historico)
# {"pergunta": "Qual e o maior problema hoje?", "diagnostico": null}

# Qualificacao BANT
bant = qualificador.qualificar(historico)
# {"score": 75, "recomendacao": "qualificado", ...}

# Gerar proposta
proposta = orcamento.gerar(diagnostico_resultado, {"nome": "Dr. Silva"})
```

## Estrutura

```
multi-agent-vendas-python/
   agents/
      diagnostico.py     # Perguntas + sintese do problema
      qualificador.py    # Score BANT
      analise_call.py    # Insights de reunioes
      orcamento.py       # Proposta comercial JSON
      simulador.py       # Treino de objecoes
   core/
      llm.py             # Wrapper Claude API
   orchestrator.py       # Fluxo interativo completo
```

## Licenca

MIT

---

<details>
<summary>🇺🇸 English</summary>

# Multi-Agent Sales Python

![CI](https://github.com/Dimitrearaujo/multi-agent-vendas-python/actions/workflows/ci.yml/badge.svg)

Multi-agent system for automating the sales process: 5 specialized AI agents operating in sequence, from diagnosis to closing.

## Agents

| Agent | Mission |
|---|---|
| `diagnostico.py` | Identifies the biggest business problem via open-ended questions |
| `qualificador.py` | BANT evaluation (Budget, Authority, Need, Timeline) with 0-100 score |
| `analise_call.py` | Extracts insights from meeting transcripts |
| `orcamento.py` | Generates a personalized commercial proposal based on diagnosis |
| `simulador.py` | Objection training — AI prospect + coach that evaluates your responses |

## Flow

```
New lead
    |
diagnostico.py
(3-5 questions)
    |
qualificador.py
(BANT score)
    |
score >= 60? ──NO──> nurture / disqualify
    |
  YES
    |
orcamento.py
(JSON proposal)
    |
analise_call.py <── meeting transcript
    |
simulador.py <── pre-call training
```

## Installation

```bash
git clone https://github.com/Dimitrearaujo/multi-agent-vendas-python
cd multi-agent-vendas-python
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your Anthropic key
```

## Usage

```bash
# Full interactive flow: diagnosis + BANT + proposal
python orchestrator.py diagnostico

# Analyze meeting transcript
python orchestrator.py call meeting.txt

# Objection training
python orchestrator.py simulador "AI automation for clinics"
```

## Individual agent usage

```python
from agents import diagnostico, qualificador, orcamento

# Diagnosis
history = [{"role": "user", "content": "I have a vet clinic with 3 employees"}]
result = diagnostico.run(history)
# {"question": "What's the biggest problem today?", "diagnosis": null}

# BANT qualification
bant = qualificador.qualificar(history)
# {"score": 75, "recommendation": "qualified", ...}

# Generate proposal
proposal = orcamento.gerar(diagnosis_result, {"name": "Dr. Silva"})
```

## Structure

```
multi-agent-vendas-python/
   agents/
      diagnostico.py     # Questions + problem synthesis
      qualificador.py    # BANT score
      analise_call.py    # Meeting insights
      orcamento.py       # Commercial proposal JSON
      simulador.py       # Objection training
   core/
      llm.py             # Claude API wrapper
   orchestrator.py       # Full interactive flow
```

## License

MIT

</details>

---

[← Back to profile](https://github.com/Dimitrearaujo)
