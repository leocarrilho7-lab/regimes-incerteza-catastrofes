# PT Evidence Verification Agent — Especificação MoE Ensemble

> **Versão:** 0.1 (design) | **Status:** A implementar na sessão v.8.6
> **Benchmark:** QCA Pipeline intercoder_debate.py (4-LLM adversarial)

## Problema

Os testes atuais do PT Pipeline (18/19 PASS) verificam apenas estrutura e lógica matemática.
Nenhum teste verifica se as evidências correspondem a documentos reais na Bibliografia Utilizada.
Isso compromete a validade do Process Tracing (Beach & Pedersen 2019, p.146-152).

## Arquitetura MoE (Mixture of Experts) Ensemble

### Princípio

Três agentes especializados verificam independentemente cada peça de evidência,
com um Judge que consolida. Adaptação do `intercoder_debate.py` do QCA Pipeline
(Propose → Critique → Resolve → Judge) para verificação documental.

### Agentes

```
┌─────────────────────────────────────────────────────────┐
│                  EVIDENCE VERIFICATION MoE               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  INPUT: evidence_raw/**/*.json (87+ itens de evidência) │
│  INPUT: Bibliografia Utilizada (1093 PDFs indexados)     │
│  INPUT: mechanism_spec.json (fingerprints esperados)     │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Expert 1:     │  │ Expert 2:     │  │ Expert 3:     │  │
│  │ DOC VERIFIER  │  │ FACT CHECKER  │  │ GAP DETECTOR  │  │
│  │               │  │               │  │               │  │
│  │ Para cada     │  │ Para cada     │  │ Para cada     │  │
│  │ evidência:    │  │ evidência:    │  │ fingerprint:  │  │
│  │ - Busca na    │  │ - WebSearch   │  │ - Conta qtd   │  │
│  │   Bibliografia│  │   do claim    │  │   evidências  │  │
│  │   via hsearch │  │ - Verifica    │  │ - Se zero →   │  │
│  │ - Confirma    │  │   datas, nomes│  │   busca       │  │
│  │   que fonte   │  │   números     │  │   exaustiva   │  │
│  │   existe      │  │ - Cruza com   │  │   na Bibliog. │  │
│  │ - Score 0-1   │  │   SIGBM/ANM   │  │ - Registra    │  │
│  │               │  │ - Score 0-1   │  │   busca vazia │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         └────────┬────────┘                 │           │
│                  ▼                          │           │
│         ┌──────────────┐                   │           │
│         │ JUDGE:        │◄──────────────────┘           │
│         │ Consolida     │                               │
│         │ scores dos 3  │                               │
│         │ experts       │                               │
│         │               │                               │
│         │ Output:       │                               │
│         │ - verified.csv│                               │
│         │ - gaps.csv    │                               │
│         │ - alerts.json │                               │
│         └──────────────┘                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Expert 1: Document Verifier (DOC_VERIFIER)

**Função:** Para cada evidência no tier file, verifica se o documento fonte existe
na Bibliografia Utilizada.

**Inputs:**
- `evidence_item.source` (ex: "CPI Brumadinho, Depoimento Eng. X, p. 45")
- Bibliografia indexada via `hsearch` (ChromaDB + Whoosh, 1093 PDFs)

**Processo:**
1. Extrair título/autor/ano da fonte citada
2. `hsearch search "{título} {autor}"` na Bibliografia
3. Se encontrado: ler trecho relevante com `lsearch page`
4. Verificar se o conteúdo do trecho suporta o claim da evidência
5. Score: 1.0 (verificado no documento), 0.5 (documento existe mas trecho não localizado),
   0.0 (documento não encontrado na Bibliografia)

**Tool:** `hybrid_search.py` (já integrado em pt_auto_evidence.py)

### Expert 2: Fact Checker (FACT_CHECKER)

**Função:** Verifica claims factuais contra fontes externas.

**Inputs:**
- `evidence_item.description` (claim factual)
- WebSearch API (via Claude)
- SIGBM CSV (dados ANM 04/04/2026)

**Processo:**
1. Extrair claims verificáveis (datas, números, nomes)
2. Para datas/números: cruzar com SIGBM CSV
3. Para claims qualitativos: WebSearch de verificação
4. Score: 1.0 (confirmado por fonte independente), 0.5 (plausível mas não verificado),
   0.0 (contradito por fonte independente)

**Regra BLOQUEANTE:** Se score = 0.0, evidência deve ser removida ou reclassificada.

### Expert 3: Gap Detector (GAP_DETECTOR)

**Função:** Identifica fingerprints do mecanismo que NÃO têm evidência documentada.

**Inputs:**
- `mechanism_spec.json` (16 fingerprints × 7 casos = 112 combinações)
- `evidence_raw/**/*.json` (evidências existentes)

**Processo:**
1. Para cada (caso × fingerprint): contar evidências encontradas
2. Se zero: buscar na Bibliografia via hsearch
3. Se Bibliografia tem documento potencial mas não foi codificado: ALERTA
4. Se nenhuma fonte encontrada: registrar como GAP com justificativa

**Output:** `evidence_gaps.csv` com:
- case_id, fingerprint_id, n_evidence, n_sources_searched, gap_justified (Y/N)

**Requisito Beach & Pedersen (2019):** Toda ausência de evidência deve ser documentada
explicitamente, distinguindo "buscou e não encontrou" de "não buscou".

### Judge: Consolidador

**Função:** Agrega scores dos 3 experts e decide status final de cada evidência.

**Regras de decisão:**
- Score médio ≥ 0.7: VERIFIED (evidência sólida)
- Score médio 0.4-0.7: PROVISIONAL (aceitável mas precisa reforço)
- Score médio < 0.4: FLAGGED (deve ser revisada manualmente)
- Qualquer expert com 0.0: ALERT (contradição ou fabricação detectada)

**Output:**
- `evidence_verified.csv`: todas as evidências com scores
- `evidence_gaps.csv`: fingerprints sem evidência
- `verification_alerts.json`: contradições e fabricações detectadas
- `verification_summary.md`: relatório narrativo

### Integração no Pipeline

```python
# Novo script: pt_03_evidence_verification.py
# Inserir entre Fase 2c e Fase 3 no pt_run_pipeline.py

PHASES = [
    ("pt_01_mechanism_spec.py",       "Fase 1: Especificação do mecanismo"),
    ("save_supplement.py",            "Fase 2a: Suplemento evidências"),
    ("pt_auto_evidence.py",           "Fase 2b: Coleta automatizada"),
    ("reclassify_evidence.py",        "Fase 2c: Reclassificação fontes"),
    ("pt_03_evidence_verification.py","Fase 2d: Verificação MoE (NOVO)"),  # ← AQUI
    ("pt_04_bayesian_update.py",      "Fase 3: Atualização bayesiana"),
    # ... restante
]
```

### Testes TDD para Evidence Verification

```python
# tests/test_pt_evidence_verification.py

def test_all_evidence_has_source():
    """Every evidence item must have a non-empty source field."""

def test_verified_evidence_has_document_in_bibliography():
    """At least 80% of evidence items should be traceable to Bibliografia."""

def test_no_fabricated_citations():
    """No evidence should have FACT_CHECKER score = 0.0."""

def test_all_fingerprints_have_search_record():
    """Every (case × fingerprint) must have search_attempted=True in gaps.csv."""

def test_gap_coverage_above_threshold():
    """At least 11/12 observable implications covered (Tansey 2007)."""

def test_evidence_dates_precede_or_match_event():
    """Evidence dates must be <= case year (no anachronistic sources)."""
```

### Custo Estimado (OpenRouter)

- Expert 1 (DOC_VERIFIER): ~$0.50 (87 evidências × hsearch local, sem API)
- Expert 2 (FACT_CHECKER): ~$1.00 (87 × WebSearch, rate-limited)
- Expert 3 (GAP_DETECTOR): ~$0.30 (112 combinações × hsearch local)
- Judge: ~$0.20 (consolidação)
- **Total: ~$2.00** (dentro do budget restante de $3.00)

### Referências Metodológicas

- Beach, D. & Pedersen, R.B. (2019). Process-Tracing Methods, 2nd ed. Ch. 7-8.
- Bennett, A. (2010). Process Tracing and Causal Inference. Ch. 10.
- Rohlfing, I. (2012). Case Studies and Causal Inference. Ch. 8.
- Tansey, O. (2007). Process Tracing and Elite Interviewing. PS: Political Science.
- George, A. & Bennett, A. (2005). Case Studies and Theory Development. Ch. 10.
- Van Evera, S. (1997). Guide to Methods for Students of Political Science. Ch. 2.

### Benchmark QCA Pipeline

O QCA Pipeline usa intercoder_debate.py com 4 LLMs adversariais (Propose → Critique →
Resolve → Judge) para validar codificação fuzzy. O Evidence Verification MoE adapta esse
padrão para validação documental, com a diferença de que os experts operam sobre fontes
heterogêneas (PDFs, CSV, WebSearch) em vez de escala numérica.
