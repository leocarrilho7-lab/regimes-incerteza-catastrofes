# Pipeline DAG — Automated vs Human Components
# DAG do Pipeline — Componentes Automatizados vs Humanos

## Legend / Legenda
- [H] = Human decision / Decisao humana
- [A] = Automated (script) / Automatizado
- [LLM] = LLM-assisted / Assistido por LLM
- [H+A] = Human-guided automation / Automacao guiada por humano

## QCA Pipeline v.8.6 (33 steps)

```
[H] Theory & Hypotheses (H1-H5)
 |
[H] Condition Selection (DIV, REG, ENF, ORG, POL)
 |
[H] Calibration Guide (7-point fuzzy scale)
 |
[A] 00_ingest_v7.R ──── Data ingestion + crossover 0.50->0.501
 |
[A] 00c_calibration.R ── Calibration validation + skewness
 |
[A] 00d_qca_eda.R ───── EDA + necessity screening (30 vars)
 |
[A] 01_gower_v7.R ───── Gower distance matrix
 |
[A] 03a/03c ──────────── NMDS + Clustering (PAM + Ward)
 |
[A] 05a_fsqca_v7.R ──── fsQCA: necessity + truth table + 3 solutions
 |                        Parameters: [H] incl.cut=0.80, n.cut=1
 |                        Directional expectations: [H] dir.exp pre-specified
 |
[A] 05b_cna_v7.R ────── CNA: coincidence analysis (convergence check)
 |
[A] 05c_robustness_v7.R ── 8 robustness tests (T1-T8)
 |                          [A] T5 Jackknife, T6 Bootstrap B=200
 |
[A] 05e_twostep_v7.R ── Two-step QCA (remote vs proximate)
 |
[A] 06_consolidate_v7.R ── Final consolidation (dynamic from outputs)
 |
[A] 08_qca_delta_v7.R ── DELTA temporal analysis (15 pairs)
 |
[A] 10-16 ───────────── Post-analysis (clustering, deviant cases, hypotheses)
 |
[LLM] 28_intercoder_reliability.R
 |     Uses: intercoder_debate.py (4-LLM adversarial debate)
 |     Models: Gemini Flash + DeepSeek V3.2
 |     Human oversight: [H] Kappa/Alpha thresholds, [H] final validation
 |
[A] 21-31 ───────────── Advanced analysis (causal robustness, condition selection)
 |
[H] Interpretation ──── All results interpreted by researcher
```

## Process Tracing Pipeline v.3 (15 phases)

```
[A] Phase 1: pt_01_mechanism_spec.py
 |   Reads: [A] QCA output (deviant_cases_classified.csv) — REQUIRED
 |   Reads: [A] QCA benchmark (bootstrap, necessity, jackknife, CSA, consensus)
 |   Structure: [H] Mechanism parts (P1-P4) defined by researcher
 |
[A] Phase 2a: save_supplement.py ─── Evidence supplement
[LLM] Phase 2b: pt_auto_evidence.py ── LLM-assisted evidence collection
 |     Model: Gemini 2.0 Flash
 |     Human oversight: [H] Evidence reviewed before use
 |
[A] Phase 2c: reclassify_evidence.py ── Source type reclassification
 |
[A] Phase 2d: pt_02_evidence_coding.py ── Formal coding matrix (112 combos)
 |     Uses: hybrid_search (local, no LLM)
 |
[A] Phase 2e: pt_03_evidence_verification.py ── MoE Ensemble (3 experts)
 |     Expert 1 (DOC_VERIFIER): local bibliography search
 |     Expert 2 (FACT_CHECKER): known facts validation
 |     Expert 3 (GAP_DETECTOR): coverage analysis
 |     No LLM calls — all local computation
 |
[A] Phase 3: pt_04_bayesian_update.py ── Bayesian updating
 |     Priors: [H] specified per mechanism part with justification
 |     QCA benchmark: [A] bootstrap weights adjust sensitivity
 |     Convergence diagnostics: [A] saturation detection
 |
[A] Phase 4a: pt_05_cross_case.py ── Cross-case heatmap
[A] Phase 4b: pt_06_temporal_sequence.py ── Temporal ordering P1->P2->P3->P4
 |
[A] Phase 5a: pt_08_hypothesis_synthesis.py ── H1-H5 synthesis
 |
[LLM] Phase 5b: pt_09_rival_hypotheses.py ── 15 rival hypotheses
 |     Architecture: Propose (LLM) -> Critic (LLM) -> Search (local) -> Judge (LLM)
 |     Model selection: [A] MAB Thompson Sampling (adaptive, 6 arms)
 |     Human oversight: [H] All rivals reviewed for plausibility
 |
[A] Phase 5c: pt_qc_gate.py ── Quality control (7 checks, BLOCKER if fails)
[A] Phase 5d: pt_feedback_qca.py ── PT->QCA consistency check
 |
[A] Phase 6: pt_07_generate_chapter.py ── DOCX chapter generation
 |     Accent guardrail: [A] 100+ Portuguese diacritics patterns
 |
[LLM] Phase 8a: pt_intercoder_evidence.py ── 2-LLM intercoder reliability
[A] Phase 8b: pt_sensitivity_analysis.py ── Prior sensitivity (+/-0.10, +/-0.20)
```

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| Fully automated [A] | 38 steps | 79% |
| LLM-assisted [LLM] | 4 steps | 8% |
| Human decisions [H] | 6 decisions | 13% |
| **Total** | **48** | **100%** |

## Key Human Decisions (non-automatable)

1. **Theory & hypotheses** (H1-H5): derived from literature review
2. **Condition selection** (5 core conditions): theoretical justification
3. **Calibration anchors** (7-point scale): domain expertise
4. **Directional expectations** (dir.exp): pre-specified from theory
5. **Threshold choices** (incl.cut, n.cut): methodological justification
6. **Interpretation of results**: all conclusions are researcher's
