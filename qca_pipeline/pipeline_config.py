"""
pipeline_config.py -- Single source of truth for QCA/PT pipeline paths and versions.
All Python scripts should import from here instead of hardcoding paths.
"""
import os
from pathlib import Path

# --- Version & Dataset ---
DATASET_VERSION = "v9"
PIPELINE_VERSION = "v.8.6"
EXCEL_FILENAME = f"Base_Barragens_{DATASET_VERSION}.xlsx"

# --- Base Paths ---
PIPELINE_DIR = Path(os.environ.get("QCA_PIPELINE_DIR", "."))
TESE_BASE = Path(os.environ.get("TESE_BASE_DIR", "."))

# --- Derived Paths ---
RELATORIOS_DIR = TESE_BASE / "Relatórios"
BARRAGENS_DIR = RELATORIOS_DIR / "barragens"
OUTPUT_BASE = RELATORIOS_DIR / "output"
OUTDIR = OUTPUT_BASE / f"QCA {PIPELINE_VERSION}"
XLSX_PATH = BARRAGENS_DIR / EXCEL_FILENAME
THESIS_DIR = OUTDIR / "thesis"
ICR_DIR = OUTDIR / "intercoder"
PT_DIR = PIPELINE_DIR / "process_tracing"
PT_OUTPUT_DIR = OUTPUT_BASE / "Process Tracing v.2"
ML_DIR = PIPELINE_DIR / "ml_enhance"

# --- Python Executable ---
PYTHON_EXE = os.environ.get("PYTHON_EXE", "python")

# --- Ensure directories exist ---
for d in [OUTDIR, THESIS_DIR, ICR_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def get_case_count():
    """Read case count dynamically from Excel."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(XLSX_PATH), read_only=True, data_only=True)
        ws = wb["Variáveis Fuzzy"]
        n = ws.max_row - 1  # minus header
        wb.close()
        return n
    except Exception:
        return None


# Convenience: set env vars so R scripts and subprocesses can read them
os.environ["QCA_OUTDIR"] = str(OUTDIR)
os.environ["QCA_XLSX_PATH"] = str(XLSX_PATH)
os.environ["QCA_PIPELINE_DIR"] = str(PIPELINE_DIR)
os.environ["QCA_DATASET_VERSION"] = DATASET_VERSION
os.environ["QCA_PIPELINE_VERSION"] = PIPELINE_VERSION
