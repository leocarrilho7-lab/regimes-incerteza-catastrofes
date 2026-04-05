# Data / Dados

## Primary Dataset

**File:** Base_Barragens_v9.xlsx (INCLUDED — no personal/sensitive data)
**Cases:** N=65 tailings dam incidents worldwide
**Variables:** 36 fuzzy-set variables on 7-point scale
**Scale:** 0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.00
**Crossover:** 0.50 adjusted to 0.501 (Ragin 2008)

## Core Conditions (INUS)

| Variable | Description (PT) | Description (EN) |
|----------|-----------------|------------------|
| DIV | Diversidade institucional | Institutional diversity |
| REG | Complexidade regulatoria | Regulatory complexity |
| ENF | Capacidade de enforcement | Enforcement capacity |
| ORG | Capacidade organizacional | Organizational capacity |
| POL | Politizacao | Politicization |
| CAT | Catastrofe (outcome) | Catastrophe (outcome) |

## Evidence Data

**Location:** evidence_raw/ (not included — available upon request)
**Format:** JSON files organized by tier and hypothesis
**Tiers:**
- Tier 1: Most-likely + typical catastrophic cases (Fundao, Brumadinho, Germano)
- Tier 2: Smaller cases (Herculano, Nova Lima, Mirai)
- Tier 3: Supplementary evidence
- H1-H5: Hypothesis-specific evidence files

## Data Access / Acesso aos Dados

The primary dataset (Base_Barragens_v9.xlsx) is included in this repository.
It contains only public information: corporate operators, technical parameters,
publicly reported incidents. No personal data (names, emails, CPF, addresses).

O dataset principal esta incluido neste repositorio.
Contem apenas informacoes publicas: operadores corporativos, parametros tecnicos,
incidentes publicamente reportados. Nenhum dado pessoal.

**Security scan:** Zero sensitive fields detected (no email, phone, CPF, CNPJ, addresses).
**Operators:** All corporate entities (Vale S.A., Samarco, BHP, etc.)
**Sources:** Academic publications, news reports, official documents.

## Sheets / Planilhas

| Sheet | Rows | Description |
|-------|------|-------------|
| Fichas dos Casos | 87 | Case descriptions (region, country, operator, deaths, causes) |
| Glossario Tecnico | 39 | Technical glossary |
| Guia de Calibracao | 31 | 7-point fuzzy calibration guide |
| Classificacao Causal | 31 | ICOLD causal classification |
| Modelo Causal | 29 | Causal model specification |
| Variaveis Fuzzy | 65 | Fuzzy-set membership scores (36 variables) |
| DELTA Pairs | 25 | Temporal DELTA pairs (15 jurisdictions) |
| CNA Ready | 65 | CNA-formatted data (6 core conditions + CAT) |
| SFC H4 | 231 | Structured Focused Comparison (11 jurisdictions x 21 questions) |
