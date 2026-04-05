# Rival Hypotheses Testing — Especificação Metodológica

> **Versão:** 1.0 | **Status:** Design aprovado, implementação pendente
> **Referências:** Bennett (2010), Van Evera (1997), Beach & Pedersen (2019, Cap. 7-8)

## Princípio

O script `pt_09_rival_hypotheses.py` NÃO deve conter hipóteses rivais hardcoded.
Em vez disso, deve usar um agente LLM (Propose → Critique → Judge) para:

1. **GERAR** hipóteses rivais automaticamente a partir do mecanismo principal
2. **CALIBRAR** priors e fingerprints para cada rival
3. **BUSCAR** evidências que suportem cada rival (na Bibliografia + WebSearch)
4. **ATUALIZAR** posteriors bayesianos
5. **JULGAR** se alguma rival sobrevive (posterior > 0.50)

## Arquitetura do Agente

```
┌─────────────────────────────────────────────────────┐
│              RIVAL HYPOTHESIS AGENT                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  INPUT: mechanism_spec.json (mecanismo principal)    │
│  INPUT: evidence_raw/**/*.json (evidências P1-P4)    │
│  INPUT: bayesian_updates.csv (posteriors do PT)      │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ PROPOSER (LLM 1):                            │   │
│  │ "Dado o mecanismo X com pathway Y,            │   │
│  │  proponha 3 explicações alternativas           │   │
│  │  mutuamente exclusivas que explicariam o       │   │
│  │  mesmo outcome (CAT) sem o mecanismo X.        │   │
│  │  Para cada rival, defina:                      │   │
│  │  - Tese (1 parágrafo)                         │   │
│  │  - Prior calibrado (0.20-0.50) com justif.    │   │
│  │  - 4 fingerprints com testes Van Evera        │   │
│  │  - Evidência que CONFIRMARIA a rival          │   │
│  │  - Evidência que REFUTARIA a rival"           │   │
│  └──────────────┬───────────────────────────────┘   │
│                 │                                    │
│                 ▼                                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ CRITIC (LLM 2):                               │   │
│  │ "Avalie as 3 rivais propostas:                │   │
│  │  - Os priors são calibrados corretamente?     │   │
│  │  - Os fingerprints são realmente diagnósticos?│   │
│  │  - Há steel-manning suficiente?               │   │
│  │  - As rivais são mutuamente exclusivas?       │   │
│  │  - Alguma rival está fraca demais (straw man)?│   │
│  │  Sugira correções e reforce as rivais."       │   │
│  └──────────────┬───────────────────────────────┘   │
│                 │                                    │
│                 ▼                                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ EVIDENCE SEARCHER:                            │   │
│  │ Para cada fingerprint de cada rival:          │   │
│  │  1. Buscar na Bibliografia (hsearch)          │   │
│  │  2. Buscar via WebSearch                      │   │
│  │  3. Registrar evidência encontrada ou não     │   │
│  │  4. Atribuir sensitivity/type_i               │   │
│  └──────────────┬───────────────────────────────┘   │
│                 │                                    │
│                 ▼                                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ JUDGE (LLM 3):                                │   │
│  │ Dado posteriors bayesianos de cada rival:     │   │
│  │  - Se posterior > 0.50: ALERTA (rival vive)   │   │
│  │  - Se posterior 0.20-0.50: ATENÇÃO            │   │
│  │  - Se posterior < 0.20: REFUTADA              │   │
│  │  Produzir relatório final com diagnóstico     │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  OUTPUT: rival_hypotheses.json                       │
│  OUTPUT: rival_hypotheses_report.md                  │
└─────────────────────────────────────────────────────┘
```

## Exemplo de Prompt para PROPOSER

```
Você é um metodologista de process tracing (Beach & Pedersen 2019).

MECANISMO PRINCIPAL: {mechanism_spec.json resumido}
PATHWAY QCA: DIV*~ENF*ORG → CAT
POSTERIORS: Todas as 5 partes confirmadas (>0.95) para 5/7 casos

TAREFA: Proponha exatamente 3 hipóteses rivais que:
1. Explicariam o MESMO outcome (CAT alto) sem o mecanismo principal
2. Sejam mutuamente exclusivas entre si
3. Sejam steel-manned (a versão mais forte possível de cada rival)
4. Tenham fundamento na literatura de engenharia de barragens ou regulação

Para cada rival, forneça em JSON:
{
  "id": "HR1",
  "name": "Nome curto",
  "thesis": "Tese completa (1 parágrafo)",
  "prior": float [0.20-0.50],
  "prior_justification": "Por que este prior?",
  "fingerprints": [
    {
      "id": "HR1a",
      "description": "Observable implication",
      "van_evera_test": "hoop|smoking_gun|straw_in_wind|doubly_decisive",
      "sensitivity": float,
      "type_i_error": float,
      "confirms_rival": "O que significaria se encontrada",
      "refutes_rival": "O que significaria se NÃO encontrada"
    }
  ],
  "key_evidence_for": "Evidência que confirmaria esta rival",
  "key_evidence_against": "Evidência que refutaria esta rival"
}
```

## Exemplo de Prompt para CRITIC

```
Você é um revisor metodológico adversarial (Bennett 2010).

HIPÓTESES RIVAIS PROPOSTAS: {output do PROPOSER}

Avalie CADA rival com rigor máximo:
1. O prior está calibrado corretamente? (muito baixo = straw man)
2. Os fingerprints são genuinamente diagnósticos?
3. A rival foi steel-manned? (apresentada na versão mais forte possível?)
4. Os sensitivity/type_i são realistas?
5. A rival é testável com evidências disponíveis?

REGRAS DE STEEL-MANNING:
- Se o prior está < 0.25, justifique por que não deveria ser maior
- Se algum fingerprint tem type_i > 0.50, é diagnóstico demais para a rival
- Se nenhum fingerprint é hoop test, a rival nunca pode ser refutada

Retorne as 3 rivais CORRIGIDAS com priors e fingerprints ajustados.
```

## Calibração de Priors — Diretrizes

| Faixa | Quando usar | Exemplo |
|-------|------------|---------|
| 0.45-0.50 | Rival tem suporte significativo na literatura | HR1 se painéis isentassem regulação |
| 0.30-0.45 | Rival plausível mas com contra-evidências conhecidas | HR2 (negligência documentada mas padrão existe) |
| 0.20-0.30 | Rival teoricamente possível mas empiricamente fraca | HR3 (muitas upstream sobrevivem) |
| < 0.20 | Straw man — NÃO USAR (invalida o teste) | — |

**Regra Bennett (2010):** Priors de rivais devem ser ≥ 0.20 para que o teste não seja trivial.

## Rivais Esperadas (não hardcoded, mas como referência de qualidade)

### HR1: Falha Técnica Pura
- Prior esperado: ~0.35
- Refutação esperada: Morgenstern et al. (2016) identificam falha regulatória; CPI documenta TÜV SÜD atestando estabilidade com dados contrários
- Posterior esperado: < 0.15

### HR2: Negligência Idiossincrática
- Prior esperado: ~0.30
- Refutação esperada: Padrão P1-P4 se repete em operadores diferentes; Vale opera sem colapso em jurisdições com regulação forte (Canadá pós-Mount Polley)
- Posterior esperado: < 0.20

### HR3: Determinismo Estrutural
- Prior esperado: ~0.25
- Refutação esperada: 45 upstream ativas sem colapso (SIGBM); El Mauro (Chile) upstream com regulação forte e sem colapso
- Posterior esperado: < 0.10

## Integração com Pipeline

```python
# pt_09_rival_hypotheses.py
# Fase 5b no orquestrador (após hypothesis_synthesis, antes de QC gate)

# 1. Carregar mecanismo e evidências existentes
# 2. Agente PROPOSER gera 3 rivais via LLM
# 3. Agente CRITIC valida e ajusta
# 4. Para cada fingerprint rival: buscar evidência (hsearch + WebSearch)
# 5. Bayesian update para cada rival
# 6. JUDGE consolida e produz relatório
# 7. Se qualquer rival > 0.50: BLOQUEANTE (pipeline para)
```
