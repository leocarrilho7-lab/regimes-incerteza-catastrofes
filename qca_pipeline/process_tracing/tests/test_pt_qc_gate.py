#!/usr/bin/env python3
"""Tests for pt_qc_gate.py — Phase 5c"""
import json, sys, os
from pathlib import Path
import pytest

BASE = Path(__file__).parent.parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))

@pytest.fixture
def qc_report():
    path = PT_OUTPUT / "pt_qc_report.json"
    if not path.exists():
        pytest.skip("pt_qc_report.json not found")
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def test_qc_gate_passes_with_valid_outputs(qc_report):
    """QC gate should pass when all outputs are valid."""
    assert qc_report["passed"] is True, \
        f"QC gate failed with {len(qc_report['blockers'])} blockers: " \
        f"{[b['check'] for b in qc_report['blockers']]}"

def test_qc_gate_has_all_checks(qc_report):
    """QC gate should run at least 7 checks."""
    assert qc_report["total_checks"] >= 7, \
        f"Only {qc_report['total_checks']} checks run (expected >= 7)"

def test_qc_gate_blocks_on_missing_files():
    """QC gate should detect missing required files."""
    # This is a structural test: we verify the checks list covers key files
    path = PT_OUTPUT / "pt_qc_report.json"
    if not path.exists():
        pytest.skip("pt_qc_report.json not found")
    with open(path, encoding='utf-8') as f:
        report = json.load(f)

    check_names = [c["check"] for c in report["checks"]]
    assert any("mechanism_spec" in c for c in check_names), "Missing mechanism_spec check"
    assert any("bayesian" in c for c in check_names), "Missing bayesian check"
    assert any("hypothesis" in c for c in check_names), "Missing hypothesis check"
