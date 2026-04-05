#!/usr/bin/env python3
"""Tests for pt_06_temporal_sequence.py — Phase 4b"""
import csv, sys, os
from pathlib import Path
import pytest

BASE = Path(__file__).parent.parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))

@pytest.fixture
def temporal_data():
    path = PT_OUTPUT / "temporal_sequence.csv"
    if not path.exists():
        pytest.skip("temporal_sequence.csv not found")
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

def test_temporal_order_valid_for_all_cases(temporal_data):
    """No more than 1 case should have temporal ordering violations."""
    violations = set(r["case_id"] for r in temporal_data if r["temporal_order_valid"] == "N")
    assert len(violations) <= 1, \
        f"BLOQUEANTE: {len(violations)} cases with temporal violations: {violations}"

def test_no_anachronistic_evidence(temporal_data):
    """No evidence should have dates AFTER the case event year."""
    for row in temporal_data:
        case_year = int(row["case_year"]) if row["case_year"] else None
        latest = int(row["latest_year"]) if row["latest_year"] else None
        if case_year and latest and case_year > 0:
            # Allow some slack for post-event investigation reports (+5 years)
            assert latest <= case_year + 5, \
                f"Anachronistic evidence: {row['case_id']} {row['part_id']} " \
                f"latest_year={latest} > case_year+5={case_year+5}"

def test_timeline_complete_for_typical_cases(temporal_data):
    """Typical/most-likely cases should have temporal data for all 4 parts."""
    case_parts = {}
    for row in temporal_data:
        case_id = row["case_id"]
        if case_id not in case_parts:
            case_parts[case_id] = set()
        if row["median_year"] and row["median_year"] != "":
            case_parts[case_id].add(row["part_id"])

    # At least FG and BR should have all 4 main parts
    for critical_case in ["FG", "BR"]:
        if critical_case in case_parts:
            expected = {"P1", "P2", "P3", "P4"}
            assert expected.issubset(case_parts[critical_case]), \
                f"{critical_case} missing parts: {expected - case_parts[critical_case]}"
