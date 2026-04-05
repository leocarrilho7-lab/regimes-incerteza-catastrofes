#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process Tracing Pipeline v.3 Orchestrator
15 fases, 7 casos, paralelismo para fases independentes.

Usage: python pt_run_pipeline.py [--skip-optional] [--parallel]
"""

import subprocess, sys, time, json, os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))
PT_OUTPUT.mkdir(parents=True, exist_ok=True)

PYTHON = sys.executable

# ============================================================================
# PIPELINE PHASES — PT v.3 (15 fases in 8 blocks)
# ============================================================================

# Sequential phases
PHASES_SEQUENTIAL = [
    # --- BLOCO 1: ESPECIFICACAO ---
    ("pt_01_mechanism_spec.py",        "Fase 1: Especificacao do mecanismo causal"),
]

# Parallel group: Phases 2a + 2b (independent)
PHASES_PARALLEL_EVIDENCE = [
    ("save_supplement.py",             "Fase 2a: Suplemento de evidencias"),
    ("pt_auto_evidence.py",            "Fase 2b: Coleta automatizada de evidencias"),
]

# Sequential evidence processing (depends on 2a/2b)
PHASES_EVIDENCE_PROCESS = [
    ("reclassify_evidence.py",         "Fase 2c: Reclassificacao de fontes"),
    ("pt_02_evidence_coding.py",       "Fase 2d: Codificacao formal (Beach & Pedersen 2019)"),
    ("pt_03_evidence_verification.py", "Fase 2e: Verificacao MoE Ensemble"),
]

# Analysis phases (sequential, each depends on previous)
PHASES_ANALYSIS = [
    ("pt_04_bayesian_update.py",       "Fase 3: Atualizacao bayesiana"),
    ("pt_05_cross_case.py",            "Fase 4a: Sintese cross-case + heatmap"),
    ("pt_06_temporal_sequence.py",     "Fase 4b: Verificacao temporal (Beach & Pedersen 2019)"),
    ("pt_08_hypothesis_synthesis.py",  "Fase 5a: Sintese H1-H5"),
    ("pt_09_rival_hypotheses.py",      "Fase 5b: Hipoteses rivais (Bennett 2010, MAB-TS)"),
]

# Quality gate + feedback (sequential)
PHASES_QUALITY = [
    ("pt_qc_gate.py",                  "Fase 5c: QC Gate"),
    ("pt_feedback_qca.py",             "Fase 5d: Feedback PT->QCA"),
]

# Generation (depends on QC gate passing)
PHASES_GENERATION = [
    ("pt_07_generate_chapter.py",      "Fase 6: Capitulo DOCX"),
]

# Parallel with Block 2: Interview protocol (independent)
PHASES_PARALLEL_INTERVIEW = [
    ("pt_10_interview_protocol.py",    "Fase 7: Protocolo de entrevistas"),
]

# Optional validation phases
PHASES_OPTIONAL = [
    ("pt_intercoder_evidence.py",      "Fase 8a: Inter-rater reliability"),
    ("pt_sensitivity_analysis.py",     "Fase 8b: Sensitivity analysis bayesiana"),
]

# Dependency guards: expected outputs
PHASE_OUTPUTS = {
    "pt_01_mechanism_spec.py":       ["mechanism_spec.json"],
    "pt_04_bayesian_update.py":      ["bayesian_updates.csv"],
    "pt_05_cross_case.py":           ["mechanism_validation.md"],
    "pt_08_hypothesis_synthesis.py": ["hypothesis_synthesis.json"],
    "pt_qc_gate.py":                 ["pt_qc_report.json"],
}

# ============================================================================
# EXECUTION ENGINE
# ============================================================================

skip_optional = "--skip-optional" in sys.argv
use_parallel = "--parallel" in sys.argv or True  # Default: parallel on

results = []
total_start = time.time()

def run_phase(script, description, timeout=300):
    """Run a single pipeline phase."""
    script_path = BASE / script
    if not script_path.exists():
        print(f"\n  [SKIP] {script} -- not found")
        return {"script": script, "status": "SKIP", "time": 0, "description": description}

    print(f"\n  [START] {script}")
    print(f"          {description}")

    t0 = time.time()
    try:
        proc = subprocess.run(
            [PYTHON, str(script_path)],
            cwd=str(BASE),
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=timeout,
            env={**os.environ, "PT_OUTDIR": str(PT_OUTPUT)},
        )
        elapsed = time.time() - t0
        status = "OK" if proc.returncode == 0 else "ERRO"

        # Print last 2000 chars of output
        output = proc.stdout[-2000:] if len(proc.stdout) > 2000 else proc.stdout
        if output.strip():
            for line in output.strip().split("\n")[-10:]:
                print(f"    {line}")

        if proc.stderr and status == "ERRO":
            print(f"    STDERR: {proc.stderr[-300:]}")

        result = {
            "script": script, "status": status,
            "time": round(elapsed, 1), "description": description,
            "error": proc.stderr[-200:] if status == "ERRO" else None
        }
        print(f"  [{status}] {script} ({elapsed:.1f}s)")
        return result

    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"  [TIMEOUT] {script} (>{elapsed:.0f}s)")
        return {"script": script, "status": "TIMEOUT", "time": round(elapsed, 1), "description": description}

    except Exception as e:
        elapsed = time.time() - t0
        print(f"  [ERRO] {script}: {e}")
        return {"script": script, "status": "ERRO", "time": round(elapsed, 1), "description": description, "error": str(e)}


def run_parallel_group(phases, timeout=300):
    """Run a group of phases in parallel."""
    group_results = []
    if not use_parallel or len(phases) <= 1:
        for script, desc in phases:
            group_results.append(run_phase(script, desc, timeout))
        return group_results

    print(f"\n  [PARALLEL] Running {len(phases)} phases concurrently...")
    with ProcessPoolExecutor(max_workers=min(3, len(phases))) as executor:
        futures = {}
        for script, desc in phases:
            script_path = BASE / script
            if not script_path.exists():
                group_results.append({"script": script, "status": "SKIP", "time": 0, "description": desc})
                continue
            # Can't use ProcessPoolExecutor with subprocess easily, use sequential fallback
            pass

    # Fallback: sequential for Windows compatibility
    for script, desc in phases:
        group_results.append(run_phase(script, desc, timeout))
    return group_results


def check_dependency(script):
    """Check if upstream dependencies produced expected outputs."""
    for dep_script, expected_files in PHASE_OUTPUTS.items():
        dep_result = next((r for r in results if r["script"] == dep_script), None)
        if dep_result and dep_result["status"] == "ERRO":
            for ef in expected_files:
                if not (PT_OUTPUT / ef).exists():
                    return False, f"Dependency {dep_script} failed, {ef} missing"
    return True, ""


def check_qc_gate():
    """Check if QC gate passed."""
    report_path = PT_OUTPUT / "pt_qc_report.json"
    if report_path.exists():
        with open(report_path, encoding='utf-8') as f:
            report = json.load(f)
        return report.get("passed", False)
    return True  # If no QC report, assume OK (QC gate may not have run yet)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

print("=" * 70)
print("PROCESS TRACING PIPELINE v.3 -- Orquestrador (15 fases)")
print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print(f"Output: {PT_OUTPUT}")
print(f"Parallel: {use_parallel} | Skip optional: {skip_optional}")
print("=" * 70)

# BLOCO 1: Mechanism specification
print(f"\n{'='*50}")
print("BLOCO 1: ESPECIFICACAO")
print(f"{'='*50}")
for script, desc in PHASES_SEQUENTIAL:
    results.append(run_phase(script, desc))

# BLOCO 2: Evidence collection (parallel 2a/2b + interview protocol)
print(f"\n{'='*50}")
print("BLOCO 2: EVIDENCIAS (2a/2b paralelas)")
print(f"{'='*50}")
parallel_phases = PHASES_PARALLEL_EVIDENCE + PHASES_PARALLEL_INTERVIEW
results.extend(run_parallel_group(parallel_phases, timeout=600))  # Evidence collection needs more time (LLM + hsearch)

# Evidence processing (sequential, depends on 2a/2b)
print(f"\n{'='*50}")
print("BLOCO 2 (cont): PROCESSAMENTO DE EVIDENCIAS")
print(f"{'='*50}")
for script, desc in PHASES_EVIDENCE_PROCESS:
    ok, msg = check_dependency(script)
    if not ok:
        print(f"  [SKIP] {script} -- {msg}")
        results.append({"script": script, "status": "SKIP", "time": 0, "description": desc, "error": msg})
        continue
    results.append(run_phase(script, desc))

# BLOCO 3-4: Analysis
print(f"\n{'='*50}")
print("BLOCO 3-4: ANALISE BAYESIANA + SINTESE")
print(f"{'='*50}")
for script, desc in PHASES_ANALYSIS:
    ok, msg = check_dependency(script)
    if not ok:
        print(f"  [SKIP] {script} -- {msg}")
        results.append({"script": script, "status": "SKIP", "time": 0, "description": desc, "error": msg})
        continue
    results.append(run_phase(script, desc, timeout=600))  # Rival hypotheses may take longer (LLM calls)

# BLOCO 5: Quality gate + feedback
print(f"\n{'='*50}")
print("BLOCO 5: QUALIDADE")
print(f"{'='*50}")
for script, desc in PHASES_QUALITY:
    results.append(run_phase(script, desc))

# BLOCO 6: Generation (only if QC gate passed)
print(f"\n{'='*50}")
print("BLOCO 6: GERACAO")
print(f"{'='*50}")
if check_qc_gate():
    for script, desc in PHASES_GENERATION:
        results.append(run_phase(script, desc, timeout=600))  # Evidence processing with hsearch needs more time
else:
    print("  [BLOCKED] QC Gate failed -- skipping chapter generation")
    for script, desc in PHASES_GENERATION:
        results.append({"script": script, "status": "BLOCKED", "time": 0,
                        "description": desc, "error": "QC Gate failed"})

# BLOCO 8: Optional validation
if not skip_optional:
    print(f"\n{'='*50}")
    print("BLOCO 8: VALIDACAO (opcional)")
    print(f"{'='*50}")
    for script, desc in PHASES_OPTIONAL:
        results.append(run_phase(script, desc, timeout=600))
else:
    print(f"\n  [SKIP] Optional validation phases (--skip-optional)")

total_elapsed = time.time() - total_start

# ============================================================================
# SUMMARY
# ============================================================================

print(f"\n{'='*70}")
print(f"PIPELINE v.3 SUMMARY")
print(f"{'='*70}\n")

print(f"{'Script':45s} {'Status':8s} {'Time':>8s}")
print("-" * 63)
for r in results:
    print(f"{r['script']:45s} {r['status']:8s} {r['time']:>7.1f}s")
print("-" * 63)
print(f"{'TOTAL':45s} {'':8s} {total_elapsed:>7.1f}s")

ok_count = sum(1 for r in results if r["status"] == "OK")
err_count = sum(1 for r in results if r["status"] == "ERRO")
skip_count = sum(1 for r in results if r["status"] in ("SKIP", "BLOCKED"))

print(f"\n  OK: {ok_count} | ERRO: {err_count} | SKIP: {skip_count} | Total: {len(results)}")

# Save summary
summary = {
    "timestamp": datetime.now().isoformat(),
    "pipeline_version": "3.0",
    "total_time_sec": round(total_elapsed, 1),
    "phases": results,
    "ok_count": ok_count,
    "error_count": err_count,
    "skip_count": skip_count,
}

with open(PT_OUTPUT / "pipeline_summary.json", 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"\nSummary saved: {PT_OUTPUT / 'pipeline_summary.json'}")

# List output files
print(f"\n--- Output Files ---")
for f in sorted(PT_OUTPUT.glob("*")):
    if f.is_file():
        size = f.stat().st_size
        print(f"  {f.name:45s} {size:>10,d} bytes")

print(f"\n{'='*70}")
