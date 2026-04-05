##############################################################################
## run_pipeline.R -- Orchestrator for QCA Pipeline v7 (full run)
## Executa todas as fases em sequencia, com timing e status
##############################################################################

PIPELINE_DIR <- Sys.getenv("QCA_PIPELINE_DIR", "os.environ.get("QCA_PIPELINE_DIR", ".")")
# Source utils to get proper OUTDIR from centralized config
source(file.path(PIPELINE_DIR, "utils_v7.R"))
# OUTDIR already set by utils_v7.R

# Logging helper
run_step <- function(script_name, description) {
  script_path <- file.path(PIPELINE_DIR, script_name)
  if (!file.exists(script_path)) {
    cat(sprintf("[SKIP] %s - file not found\n", script_name))
    return(list(script = script_name, status = "SKIP", time_sec = 0,
                description = description, error = "File not found"))
  }

  cat(sprintf("\n========================================\n"))
  cat(sprintf("[START] %s\n", script_name))
  cat(sprintf("        %s\n", description))
  cat(sprintf("========================================\n"))

  t0 <- proc.time()
  result <- tryCatch(
    withCallingHandlers({
      source(script_path, local = new.env(parent = globalenv()))
      list(status = "OK", error = NA)
    }, warning = function(w) {
      # Capture first warning but let execution continue (no re-run)
      invokeRestart("muffleWarning")
    }),
    error = function(e) {
      list(status = "ERRO", error = conditionMessage(e))
    }
  )
  elapsed <- (proc.time() - t0)["elapsed"]

  cat(sprintf("[%s] %s (%.1f sec)\n", result$status, script_name, elapsed))
  if (!is.na(result$error) && result$status == "ERRO") {
    cat(sprintf("  Error: %s\n", result$error))
  }

  list(script = script_name, status = result$status,
       time_sec = round(as.numeric(elapsed), 1),
       description = description, error = result$error)
}

# ===== PIPELINE EXECUTION =====
results <- list()
pipeline_start <- proc.time()

# --- BLOCO A: Data Foundation ---
cat("\n\n################################################################\n")
cat("## BLOCO A: DATA FOUNDATION\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("00_ingest_v7.R",
  "Ingestao Excel v7_VF, validacao escala 7pts, ajuste 0.50->0.501")
results[[length(results) + 1]] <- run_step("00c_calibration.R",
  "Validacao de calibracao, distribuicoes, skewness")
results[[length(results) + 1]] <- run_step("00d_qca_eda.R",
  "EDA + Necessity screening 30 variaveis")

# --- BLOCO B: Descriptive Analytics (QUARANTINE) ---
cat("\n\n################################################################\n")
cat("## BLOCO B: DESCRIPTIVE ANALYTICS (QUARANTINE)\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("01_gower_v7.R",
  "Matriz de distancia Gower (N cases, fuzzy)")
results[[length(results) + 1]] <- run_step("03a_nmds_v7.R",
  "NMDS 2D visualization + facet plots")
results[[length(results) + 1]] <- run_step("03c_clustering_v7.R",
  "PAM k-means + Ward + clusterboot (Jaccard)")

# --- BLOCO C: Causal Analysis ---
cat("\n\n################################################################\n")
cat("## BLOCO C: CAUSAL ANALYSIS\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("05a_fsqca_v7.R",
  "fsQCA principal: necessity, truth table, 3 solutions CAT + ~CAT")
results[[length(results) + 1]] <- run_step("05b_cna_v7.R",
  "CNA co-principal: frscore, ASFs, convergence with fsQCA")
results[[length(results) + 1]] <- run_step("05e_twostep_v7.R",
  "Two-Step QCA: remote vs proximate, context analysis")
results[[length(results) + 1]] <- run_step("08_qca_delta_v7.R",
  "DELTA analysis: 15 temporal pairs, 4 quadrants")
results[[length(results) + 1]] <- run_step("05c_robustness_v7.R",
  "8 robustness tests: T1-T8 (incl.cut, alt conds, jackknife, bootstrap)")
# --- POST-ANALYSIS ---
cat("\n\n################################################################\n")
cat("## POST-ANALYSIS\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("10_clustering_insights.R",
  "Deep cluster analysis: profiles, heatmaps, deviants")
results[[length(results) + 1]] <- run_step("11_julia_black_test.R",
  "Julia Black framework mapping")
results[[length(results) + 1]] <- run_step("12_deviant_cases.R",
  "Classify deviant cases (coverage, anomalies)")
results[[length(results) + 1]] <- run_step("13_hypotheses_test.R",
  "Test H1-H5 hypotheses")
results[[length(results) + 1]] <- run_step("14_jurisdiction_selection.R",
  "Select jurisdictions for process tracing")
results[[length(results) + 1]] <- run_step("15_process_tracing_prep.R",
  "Brazilian case selection (most-likely, typical, deviant)")

# --- SFC H4 + DAG VISUALIZATION ---
cat("\n\n################################################################\n")
cat("## SFC H4 ANALYSIS + DAG VISUALIZATION\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("16_sfc_h4_analysis.R",
  "SFC H4: Structured Focused Comparison (11 jurisdicoes x 21 perguntas)")
results[[length(results) + 1]] <- run_step("17_cna_dag_visualization.R",
  "DAG Visualization: CNA models + fsQCA pathways (DiagrammeR)")

# --- TEMPORAL QCA (v7.1) ---
cat("\n\n################################################################\n")
cat("## TEMPORAL QCA: TSQCA + csQCA + tQCA (v7.1)\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("18_tsqca_robustness.R",
  "TSQCA: Threshold-Sweep QCA robustez sistematica (De Tos 2024)")
results[[length(results) + 1]] <- run_step("19_pretest_csqca_temporal.R",
  "Pre-teste csQCA temporal (Caren & Panofsky 2005)")
results[[length(results) + 1]] <- run_step("20_tqca_implementation.R",
  "tQCA: Temporal QCA com 15 pares DELTA (Caren & Panofsky 2005)")

# --- CONDITION SELECTION ---
cat("\n\n################################################################\n")
cat("## CONDITION SELECTION (23)\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("23_condition_selection_validation.R",
  "Condition selection: necessity screening 30 vars, superSubset")
results[[length(results) + 1]] <- run_step("23b_condition_selection_full.R",
  "Full condition selection: multiverse M1-M6, ranking")

# --- CAUSAL ROBUSTNESS ---
cat("\n\n################################################################\n")
cat("## CAUSAL ROBUSTNESS (Hipoteses Parciais)\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("21_causal_robustness.R",
  "Robustez causal: Skaaning sensitivity + Wilcoxon DELTA + STMM case selection")

# --- CONSOLIDATION (after ALL analysis scripts, so all CSVs exist) ---
cat("\n\n################################################################\n")
cat("## CONSOLIDATION\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("06_consolidate_v7.R",
  "Consolidacao final: Excel 8 sheets + relatorio")

# --- ML ENHANCEMENT (Python) ---
cat("\n\n################################################################\n")
cat("## ML ENHANCEMENT (Thompson Sampling + Ensemble)\n")
cat("################################################################\n")

PYTHON <- Sys.getenv("PYTHON_EXE", Sys.which("python"))
if (PYTHON == "" || !file.exists(PYTHON)) {
  PYTHON <- "python"
}
ML_DIR <- base::file.path(PIPELINE_DIR, "ml_enhance")

ml_phases <- c(
  "phase04_multi_importance.py",
  "phase05_thompson_robustness.py",
  "phase05_ensemble_voting.py",
  "phase23_condition_search.py",
  "phase06_enhanced_consolidate.py"
)

for (phase in ml_phases) {
  phase_path <- base::file.path(ML_DIR, phase)
  if (!file.exists(phase_path)) {
    cat(sprintf("[SKIP] ML:%s - not found\n", phase))
    results[[length(results) + 1]] <- list(
      script = paste0("ML:", phase), status = "SKIP",
      time_sec = 0, description = paste("ML Enhancement:", phase),
      error = "File not found")
    next
  }
  cat(sprintf("\n[ML] %s\n", phase))
  t0 <- proc.time()
  ret <- system2(PYTHON, phase_path, stdout = TRUE, stderr = TRUE)
  elapsed <- (proc.time() - t0)["elapsed"]
  exit_code <- attr(ret, "status")
  status <- ifelse(is.null(exit_code) || exit_code == 0, "OK", "ERRO")
  cat(paste(ret, collapse = "\n"), "\n")
  cat(sprintf("[%s] ML:%s (%.1f sec)\n", status, phase, elapsed))
  results[[length(results) + 1]] <- list(
    script = paste0("ML:", phase), status = status,
    time_sec = round(as.numeric(elapsed), 1),
    description = paste("ML Enhancement:", phase),
    error = if (status == "ERRO") paste(tail(ret, 3), collapse = " ") else NA
  )
}

# --- QC GATE ---
cat("\n\n################################################################\n")
cat("## QC GATE (Quality Control)\n")
cat("################################################################\n")

qc_script <- file.path(PIPELINE_DIR, "qc_pipeline_gate.py")
if (file.exists(qc_script)) {
  t0 <- proc.time()
  qc_ret <- system2(PYTHON, qc_script, stdout = TRUE, stderr = TRUE)
  elapsed <- (proc.time() - t0)["elapsed"]
  exit_code <- attr(qc_ret, "status")
  qc_status <- ifelse(is.null(exit_code) || exit_code == 0, "OK", "WARN")
  cat(paste(qc_ret, collapse = "\n"), "\n")
  results[[length(results) + 1]] <- list(
    script = "qc_pipeline_gate.py", status = qc_status,
    time_sec = round(as.numeric(elapsed), 1),
    description = "Quality Control Gate",
    error = if (qc_status == "WARN") "QC Gate detectou issues" else NA
  )
} else {
  cat("[SKIP] qc_pipeline_gate.py not found\n")
}

# --- INTERCODER + EXTENDED ANALYSIS (28-31) ---
cat("\n\n################################################################\n")
cat("## INTERCODER + EXTENDED ANALYSIS\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("28_intercoder_reliability.R",
  "Intercoder reliability: Kappa, Alpha, ICC, heatmaps")
results[[length(results) + 1]] <- run_step("29_tjqca_stages.R",
  "TJ-QCA: 6 Brazilian cases x 6 temporal stages")
results[[length(results) + 1]] <- run_step("30_longitudinal_qca_h4.R",
  "Longitudinal QCA: H4 institutional learning test")
results[[length(results) + 1]] <- run_step("31_methodology_validation.R",
  "Methodology validation: Rutten, Bennett, Hall, SetMethods")

# --- PROCESS TRACING (Python) ---
cat("\n\n################################################################\n")
cat("## PROCESS TRACING\n")
cat("################################################################\n")

PT_DIR <- file.path(PIPELINE_DIR, "process_tracing")
pt_scripts <- c("pt_04_bayesian_update.py", "pt_07_generate_chapter.py")
for (pt in pt_scripts) {
  pt_path <- file.path(PT_DIR, pt)
  if (!file.exists(pt_path)) {
    cat(sprintf("[SKIP] PT:%s - not found\n", pt))
    results[[length(results) + 1]] <- list(
      script = paste0("PT:", pt), status = "SKIP",
      time_sec = 0, description = paste("Process Tracing:", pt),
      error = "File not found")
    next
  }
  cat(sprintf("\n[PT] %s\n", pt))
  t0 <- proc.time()
  ret <- system2(PYTHON, pt_path, stdout = TRUE, stderr = TRUE)
  elapsed <- (proc.time() - t0)["elapsed"]
  exit_code <- attr(ret, "status")
  status <- ifelse(is.null(exit_code) || exit_code == 0, "OK", "ERRO")
  cat(paste(ret, collapse = "\n"), "\n")
  cat(sprintf("[%s] PT:%s (%.1f sec)\n", status, pt, elapsed))
  results[[length(results) + 1]] <- list(
    script = paste0("PT:", pt), status = status,
    time_sec = round(as.numeric(elapsed), 1),
    description = paste("Process Tracing:", pt),
    error = if (status == "ERRO") paste(tail(ret, 3), collapse = " ") else NA
  )
}

# --- DOCX REPORT GENERATION ---
cat("\n\n################################################################\n")
cat("## DOCX REPORT GENERATION\n")
cat("################################################################\n")

Sys.setenv(QCA_OUTDIR = OUTDIR)
docx_scripts <- c("generate_consolidated_chapter.py", "generate_v8_report.py")
for (ds in docx_scripts) {
  ds_path <- file.path(PIPELINE_DIR, ds)
  if (!file.exists(ds_path)) {
    cat(sprintf("[SKIP] DOCX:%s - not found\n", ds))
    results[[length(results) + 1]] <- list(
      script = paste0("DOCX:", ds), status = "SKIP",
      time_sec = 0, description = paste("DOCX Report:", ds),
      error = "File not found")
    next
  }
  cat(sprintf("\n[DOCX] %s\n", ds))
  t0 <- proc.time()
  ret <- system2(PYTHON, ds_path, stdout = TRUE, stderr = TRUE)
  elapsed <- (proc.time() - t0)["elapsed"]
  exit_code <- attr(ret, "status")
  status <- ifelse(is.null(exit_code) || exit_code == 0, "OK", "ERRO")
  cat(paste(ret, collapse = "\n"), "\n")
  cat(sprintf("[%s] DOCX:%s (%.1f sec)\n", status, ds, elapsed))
  results[[length(results) + 1]] <- list(
    script = paste0("DOCX:", ds), status = status,
    time_sec = round(as.numeric(elapsed), 1),
    description = paste("DOCX Report:", ds),
    error = if (status == "ERRO") paste(tail(ret, 3), collapse = " ") else NA
  )
}

# --- FINAL AUDIT ---
cat("\n\n################################################################\n")
cat("## AUDIT\n")
cat("################################################################\n")
results[[length(results) + 1]] <- run_step("99_validate_v7.R",
  "Auditoria final: validacao Excel, escalas, NAs")

# ===== SUMMARY =====
pipeline_elapsed <- (proc.time() - pipeline_start)["elapsed"]

cat("\n\n================================================================\n")
cat("== PIPELINE EXECUTION SUMMARY\n")
cat("================================================================\n\n")

# Table
cat(sprintf("%-40s %-6s %8s\n", "SCRIPT", "STATUS", "TIME(s)"))
cat(paste(rep("-", 58), collapse = ""), "\n")
for (r in results) {
  cat(sprintf("%-40s %-6s %8.1f\n", r$script, r$status, r$time_sec))
}
cat(paste(rep("-", 58), collapse = ""), "\n")
cat(sprintf("%-40s %-6s %8.1f\n", "TOTAL", "", as.numeric(pipeline_elapsed)))

# Errors
errors <- Filter(function(r) r$status == "ERRO", results)
if (length(errors) > 0) {
  cat("\n--- ERRORS ---\n")
  for (e in errors) {
    cat(sprintf("  %s: %s\n", e$script, e$error))
  }
}

# Bottlenecks (top 5 by time)
sorted <- results[order(-sapply(results, function(r) r$time_sec))]
cat("\n--- BOTTLENECKS (top 5 by time) ---\n")
for (i in 1:min(5, length(sorted))) {
  r <- sorted[[i]]
  cat(sprintf("  #%d: %s (%.1f sec) - %s\n", i, r$script, r$time_sec, r$description))
}

# Save summary to JSON
summary_data <- list(
  timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  total_time_sec = round(as.numeric(pipeline_elapsed), 1),
  total_scripts = length(results),
  ok_count = sum(sapply(results, function(r) r$status == "OK")),
  warn_count = sum(sapply(results, function(r) r$status == "WARN")),
  error_count = sum(sapply(results, function(r) r$status == "ERRO")),
  skip_count = sum(sapply(results, function(r) r$status == "SKIP")),
  steps = results
)
jsonlite::write_json(summary_data, file.path(OUTDIR, "pipeline_run_summary.json"),
                     pretty = TRUE, auto_unbox = TRUE)
cat(sprintf("\n[OK] Summary saved to %s\n", file.path(OUTDIR, "pipeline_run_summary.json")))
cat(sprintf("\nPipeline completed in %.1f seconds (%.1f minutes)\n",
            as.numeric(pipeline_elapsed), as.numeric(pipeline_elapsed) / 60))
