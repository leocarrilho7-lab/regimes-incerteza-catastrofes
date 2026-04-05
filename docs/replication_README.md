# Replication Package — QCA Pipeline v.8.6 + PT Pipeline v.3

> Seguindo: Political Analysis Replication Guidelines (2025),
> APSA Guidelines for Reproducibility, Schneider & Wagemann (2012, Ch.10)

## Environment

| Component | Version | Notes |
|-----------|---------|-------|
| OS | Windows 11 Pro 10.0.22631 | |
| R | 4.5.2 (2025-10-31) | |
| Python | 3.13 | Primary; 3.10 as fallback |
| QCA package | 3.23 (Dusa 2019) | |
| cna package | latest | Coincidence Analysis |
| scikit-learn | 1.8.0 | ML enhancement |
| python-docx | latest | DOCX generation |
| openpyxl | latest | Excel I/O |
| chromadb | 1.5.5 | Semantic search (bibliography) |

## R Packages (install)

```r
install.packages(c("QCA", "cna", "ggplot2", "readxl", "writexl",
                    "cluster", "vegan", "fpc", "DiagrammeR",
                    "DiagrammeRsvg", "rsvg", "parallel", "jsonlite",
                    "irr", "DescTools"))
```

## Python Packages (install)

```bash
pip install scikit-learn python-docx openpyxl requests pandas numpy
```

## Execution Order

```bash
# 1. QCA Pipeline (33 steps, ~10 min)
Rscript qca_pipeline/run_pipeline.R

# 2. Process Tracing Pipeline (15 phases, ~15 min)
cd qca_pipeline/process_tracing
python pt_run_pipeline.py

# 3. Generate DOCX reports
cd qca_pipeline
python generate_v8_report.py
python generate_consolidated_chapter.py
```

## Directory Structure

```
qca_pipeline/
  00_ingest_v7.R          # Data ingestion + crossover adjustment
  00c_calibration.R       # Calibration validation
  00d_qca_eda.R           # EDA + necessity screening
  01_gower_v7.R           # Gower distance matrix
  03a_nmds_v7.R           # NMDS visualization
  03c_clustering_v7.R     # PAM + Ward clustering
  05a_fsqca_v7.R          # fsQCA: necessity + sufficiency
  05b_cna_v7.R            # CNA: coincidence analysis
  05c_robustness_v7.R     # 8 robustness tests (T1-T8)
  05e_twostep_v7.R        # Two-step QCA
  06_consolidate_v7.R     # Final consolidation
  08_qca_delta_v7.R       # DELTA temporal analysis
  10-16: Post-analysis    # Clustering, deviant cases, hypotheses
  21-31: Advanced         # Causal robustness, condition selection
  process_tracing/
    pt_01-pt_10: 15 PT phases
    tests/: 8 test files
  docs/
    Methodology_Justifications.md
    Pre_Registration.md
    Causal_DAG.md
```

## Random Seeds

All stochastic operations use `set.seed(42)` for reproducibility.
Robustness confirmed across seeds 42, 123, 999.
See docs/Methodology_Justifications.md section 8.

## Data

- Primary dataset: Base_Barragens_v9.xlsx (65 cases, 36 fuzzy variables)
- Scale: 7-point (0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.00)
- Crossover adjustment: 0.50 -> 0.501 (Ragin 2008)
- Evidence: evidence_raw/*.json (tier 1-3 + hypothesis-specific)

## LLM Usage

See DISCLOSURE.md in project root for complete AI transparency statement.
