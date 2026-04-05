# Pre-Registration — QCA Analysis of Regulatory Catastrophes

> Documento de pre-registro: hipoteses, condicoes, direcoes e thresholds
> especificados ANTES da analise empirica de dados.
> Referencia: Qualificacao de doutorado (FGV, 2024)

---

## 1. Hipoteses

| ID | Hipotese | Tipo PT | Refutacao |
|----|----------|---------|-----------|
| H1 | Diversidade institucional (DIV) como condicao INUS para catastrofe | Theory-testing | Jurisdicoes com alta DIV e sem catastrofes |
| H2 | Subestimacao sistematica: DIV*~ENF*ORG como pathway suficiente | Theory-testing | Mecanismo P1-P4 nao opera em casos com pathway |
| H3 | Interrupcao causal no caso Sul Superior (explaining-outcome) | Explaining-outcome | SS tem mesmas condicoes mas intervencao pos-Brumadinho impediu CAT |
| H4 | Aprendizado institucional pos-catastrofe reduz CAT via DELTA temporal | Theory-building | Jurisdicoes com reconhecimento de incerteza tem taxas equivalentes |
| H5 | Condicoes de escopo ASYM*IRREV*UNC_DEEP delimitam o mecanismo | Scope-condition | Setor com 3 condicoes e sem catastrofe |

## 2. Condicoes Core (selecao teorica)

| Condicao | Operacionalizacao | Direcao esperada | Base teorica |
|----------|------------------|-------------------|-------------|
| DIV | Diversidade institucional regulatoria | + (presenca -> CAT) | Dunlop & Radaelli 2013 |
| REG | Complexidade do framework regulatorio | + (presenca -> CAT) | Baldwin et al. 2012 |
| ENF | Capacidade de enforcement | - (AUSENCIA -> CAT) | Modelo de subestimacao |
| ORG | Capacidade organizacional do operador | + (presenca -> CAT) | Vaughan 1996 |
| POL | Politizacao do setor | + (presenca -> CAT) | Lodge & Wegrich 2012 |

**Condicao excluida:** GRAV (circularidade com outcome CAT)

## 3. Thresholds Pre-Especificados

| Parametro | Valor | Referencia |
|-----------|-------|-----------|
| inclN (necessidade) | 0.90 | Schneider & Wagemann 2012, p.143 |
| incl.cut (suficiencia) | 0.80 | Ragin 2008, p.44-48 |
| n.cut (frequencia) | 1 | N=65, ratio N/k=2.03 |
| Bootstrap B | 200 | Thomann & Maggetti 2020 |
| Bayesian confirmation | 0.95 | Rohlfing 2012, p.183 |

## 4. Expectativas Direcionais

```
dir.exp = c(DIV=1, REG=1, ENF=0, ORG=1, POL=1)
```

Especificadas com base no modelo teorico do Capitulo 2 (Secao 2.3).
ENF=0 indica que a AUSENCIA de enforcement contribui para a catastrofe.

## 5. Testes de Robustez Planejados

1. T1: Variacao de incl.cut [0.75, 0.90]
2. T2: Condicoes alternativas (subsets + swaps + random)
3. T3: Variacao de n.cut [1, 2, 3]
4. T4: Calibration shifts [+-0.02, +-0.05]
5. T5: Jackknife leave-one-out (N=65)
6. T6: Bootstrap (B=200)
7. T7: PRI.cut sensitivity [0.50, 0.85]
8. T8: Escala 5-pontos vs 7-pontos

## 6. Data

- Dataset: Base_Barragens_v9.xlsx (N=65, 36 variaveis fuzzy)
- Escala: 7-pontos (0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.00)
- Crossover adjustment: 0.50 -> 0.501 (Ragin 2008)
