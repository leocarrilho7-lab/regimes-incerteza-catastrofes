# Regimes de Incerteza e Catástrofes Regulatórias
# Uncertainty Regimes and Regulatory Catastrophes

> **PT-BR:** Pipeline computacional para análise configuracional (QCA) e Process Tracing bayesiano de catástrofes regulatórias em barragens de rejeitos.
>
> **EN:** Computational pipeline for configurational analysis (QCA) and Bayesian Process Tracing of regulatory catastrophes in tailings dams.

---

## Tese de Doutorado / Doctoral Thesis

**Instituição / Institution:** FGV — Fundação Getulio Vargas
**Programa / Program:** Direito da Regulação / Regulatory Law
**Autor / Author:** Leonardo Carrilho

---

## Arquitetura / Architecture

### QCA Pipeline v.8.6 (33 etapas / steps — R)

```
00: Ingestão + Calibração + EDA / Ingestion + Calibration + EDA
01-03: Distância Gower + NMDS + Clustering / Gower Distance + NMDS + Clustering
05: fsQCA + CNA + Two-Step + Robustez (8 testes) / fsQCA + CNA + Two-Step + Robustness (8 tests)
06: Consolidação / Consolidation
08-16: DELTA + Casos Desviantes + Hipóteses + SFC / DELTA + Deviant Cases + Hypotheses + SFC
21-31: Robustez Causal + Seleção de Condições + Intercoder / Causal Robustness + Condition Selection + Intercoder
```

### Process Tracing Pipeline v.3 (15 fases / phases — Python)

```
Phase 1: Especificação do mecanismo causal / Causal mechanism specification
Phases 2a-2e: Coleta + Codificação + Verificação / Collection + Coding + Verification (MoE Ensemble)
Phase 3: Atualização bayesiana / Bayesian updating (Rohlfing 2012)
Phases 4a-4b: Síntese cross-case + Verificação temporal / Cross-case + Temporal verification
Phases 5a-5d: Hipóteses + Rivais (MAB-TS) + QC Gate + Feedback / Hypotheses + Rivals + QC + Feedback
Phase 6: Geração de capítulo DOCX / Chapter DOCX generation
Phases 8a-8b: Confiabilidade intercoder + Análise de sensibilidade / Intercoder + Sensitivity
```

## Metodologia / Methodology

| Método / Method | Referência / Reference |
|-----------------|----------------------|
| QCA (Fuzzy-Set) | Ragin (2008), Schneider & Wagemann (2012), Dusa (2019) |
| Process Tracing (Bayesian) | Beach & Pedersen (2019), Rohlfing (2012), Bennett (2010) |
| Van Evera Tests | Van Evera (1997) — straw-in-wind, hoop, smoking gun, doubly decisive |
| Rival Hypotheses (MAB-TS) | Bennett (2010) — 15 rivais via LLM adversarial debate |
| Robustness | 8 tests (T1-T8), bootstrap B=200, jackknife N=65 |
| Multi-Method | Schneider & Rohlfing (2013), Lieberman (2005) |

## Uso de IA / AI Usage

Este projeto utiliza modelos de linguagem (LLMs) como ferramentas auxiliares, conforme:
- **Portaria CNPq n. 2.664/2026** (Política de Integridade na Atividade Científica)
- **Diretrizes CAPES** (2025) para uso de IA em pesquisa
- **Diretrizes para Uso Ético de IAG** (Sampaio, Sabbatini & Limongi, 2025)

This project uses language models (LLMs) as auxiliary tools, in compliance with Brazilian research integrity policies (CNPq Ordinance 2.664/2026, CAPES 2025 Guidelines).

Ver / See: [DISCLOSURE.md](DISCLOSURE.md)

## Acesso ao Código / Code Access

| Componente / Component | Acesso / Access | Justificativa / Rationale |
|------------------------|-----------------|---------------------------|
| Arquitetura e documentação / Architecture & docs | Público / Public | Transparência / Transparency |
| Código completo / Full code (R + Python) | Sob solicitação / Upon request | Em aperfeiçoamento / Under development |
| Dataset | Sob solicitação / Upon request | Dados sensíveis / Sensitive data |

O código-fonte completo será disponibilizado integralmente após a defesa da tese.
Full source code will be made available after thesis defense.

## Reprodutibilidade / Reproducibility

Ver / See: [docs/replication_README.md](docs/replication_README.md)

**Requisitos mínimos / Minimum requirements:**
- R 4.5.2 + QCA (3.23), cna, ggplot2, cluster, vegan, parallel
- Python 3.13 + scikit-learn (1.8.0), python-docx, openpyxl, requests
- N=65 cases, 36 fuzzy variables, 7-point scale

## Licença / License

- Código / Code: MIT License (após publicação / after publication)
- Dados / Data: Acesso restrito / Restricted access
- Documentação / Documentation: CC-BY-4.0
