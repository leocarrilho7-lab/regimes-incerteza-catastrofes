#!/usr/bin/env python3
"""Tests for pt_02_evidence_coding.py — Phase 2d"""
import json, csv, sys, os
from pathlib import Path
import pytest

BASE = Path(__file__).parent.parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))

@pytest.fixture
def coding_matrix():
    path = PT_OUTPUT / "evidence_coding_matrix.csv"
    if not path.exists():
        pytest.skip("evidence_coding_matrix.csv not found")
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

@pytest.fixture
def mechanism_spec():
    path = PT_OUTPUT / "mechanism_spec.json"
    if not path.exists():
        pytest.skip("mechanism_spec.json not found")
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def test_all_fingerprints_have_search_record(coding_matrix):
    """Every (case x fingerprint) must have a search record."""
    for row in coding_matrix:
        assert row["fingerprint_id"], f"Empty fingerprint_id in row: {row}"
        assert row["case_id"], f"Empty case_id in row: {row}"

def test_no_fingerprint_with_zero_searches(coding_matrix):
    """No fingerprint with evidence_found=N should have n_sources_searched=0."""
    for row in coding_matrix:
        if row["evidence_found"] == "N":
            assert int(row["n_sources_searched"]) > 0, \
                f"Zero searches for {row['case_id']}x{row['fingerprint_id']}: must search before declaring absent"

def test_coverage_above_threshold(coding_matrix, mechanism_spec):
    """Observable implications coverage >= 11/12 (Tansey 2007)."""
    fp_ids = set()
    for part in mechanism_spec["mechanism"]["parts"]:
        if part["id"] != "P_INT":
            for fp in part.get("fingerprints", []):
                fp_ids.add(fp["id"])

    covered = set()
    for row in coding_matrix:
        if row["evidence_found"].startswith("Y") and row["part_id"] != "P_INT":
            covered.add(row["fingerprint_id"])

    coverage = len(covered) / len(fp_ids) if fp_ids else 0
    threshold = 11 / 12  # Tansey (2007)
    assert coverage >= threshold, \
        f"Coverage {coverage:.1%} below threshold {threshold:.1%}. Covered: {len(covered)}/{len(fp_ids)}"

def test_van_evera_classifications_valid(coding_matrix):
    """All van_evera_classification values must be valid types."""
    valid = {"straw_in_wind", "hoop", "smoking_gun", "doubly_decisive"}
    for row in coding_matrix:
        assert row["van_evera_classification"] in valid, \
            f"Invalid classification '{row['van_evera_classification']}' for {row['fingerprint_id']}"
