#!/usr/bin/env python3
"""Tests for pt_intercoder_evidence.py — Phase 8a"""
import csv, sys, os
from pathlib import Path
import pytest

BASE = Path(__file__).parent.parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))

@pytest.fixture
def intercoder_data():
    path = PT_OUTPUT / "evidence_intercoder.csv"
    if not path.exists():
        pytest.skip("evidence_intercoder.csv not found")
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _compute_kappa(data, categories=None):
    """Compute Cohen's Kappa from intercoder CSV."""
    if not data:
        return 0.0
    categories = categories or ["straw_in_wind", "hoop", "smoking_gun", "doubly_decisive"]
    ratings_a = [r["coder_a_test"] for r in data]
    ratings_b = [r["coder_b_test"] for r in data]
    n = len(ratings_a)
    agree = sum(1 for a, b in zip(ratings_a, ratings_b) if a == b)
    po = agree / n
    pe = sum((sum(1 for r in ratings_a if r == c) / n) * (sum(1 for r in ratings_b if r == c) / n) for c in categories)
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)

def _compute_gwet_ac1(data, categories=None):
    """Compute Gwet's AC1."""
    if not data:
        return 0.0
    categories = categories or ["straw_in_wind", "hoop", "smoking_gun", "doubly_decisive"]
    ratings_a = [r["coder_a_test"] for r in data]
    ratings_b = [r["coder_b_test"] for r in data]
    n = len(ratings_a)
    agree = sum(1 for a, b in zip(ratings_a, ratings_b) if a == b)
    po = agree / n
    q = len(categories)
    pi_k = [(sum(1 for r in ratings_a if r == c) + sum(1 for r in ratings_b if r == c)) / (2 * n) for c in categories]
    pe = sum(p * (1 - p) for p in pi_k) / (q - 1) if q > 1 else 0
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)

def test_kappa_above_threshold(intercoder_data):
    """Cohen's Kappa for van_evera_test should be >= 0.70."""
    kappa = _compute_kappa(intercoder_data)
    assert kappa >= 0.70, f"Cohen's Kappa = {kappa:.3f} < 0.70"

def test_gwet_ac1_above_threshold(intercoder_data):
    """Gwet's AC1 should be >= 0.70."""
    ac1 = _compute_gwet_ac1(intercoder_data)
    assert ac1 >= 0.70, f"Gwet's AC1 = {ac1:.3f} < 0.70"

def test_alpha_above_threshold(intercoder_data):
    """Krippendorff's Alpha for sensitivity should be >= 0.70."""
    if not intercoder_data:
        pytest.skip("No data")
    sens_a = [float(r["coder_a_sens"]) for r in intercoder_data]
    sens_b = [float(r["coder_b_sens"]) for r in intercoder_data]
    n = len(sens_a)
    if n < 2:
        pytest.skip("Not enough data")
    do = sum((a - b) ** 2 for a, b in zip(sens_a, sens_b)) / n
    all_vals = sens_a + sens_b
    mean = sum(all_vals) / len(all_vals)
    de = sum((v - mean) ** 2 for v in all_vals) / (len(all_vals) - 1)
    alpha = 1.0 - do / de if de > 0 else 1.0
    assert alpha >= 0.70, f"Krippendorff's Alpha (sensitivity) = {alpha:.3f} < 0.70"
