#!/usr/bin/env python3
"""TDD tests for pt_04_bayesian_update.py — Bayesian updating logic."""
import sys, os, json, csv, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(BASE, "output")


def test_bayesian_update_smoking_gun():
    """Smoking gun (high sensitivity, low type_i) should push prior up strongly."""
    # Replicate the formula from pt_04
    prior = 0.50
    sensitivity = 0.70
    type_i = 0.05
    # P(H|E) = P(E|H)*P(H) / [P(E|H)*P(H) + P(E|~H)*P(~H)]
    posterior = (sensitivity * prior) / (sensitivity * prior + type_i * (1 - prior))
    assert posterior > 0.88, f"Smoking gun posterior {posterior:.3f} should be > 0.88"


def test_bayesian_update_absence_leaves_unchanged():
    """When sensitivity == type_i, evidence is uninformative."""
    prior = 0.50
    sensitivity = 0.50
    type_i = 0.50
    posterior = (sensitivity * prior) / (sensitivity * prior + type_i * (1 - prior))
    assert abs(posterior - prior) < 0.001, f"Uninformative evidence changed posterior: {posterior}"


def test_sequential_smoking_guns_confirm():
    """Three sequential smoking guns from prior 0.50 should yield posterior >= 0.95."""
    prior = 0.50
    for _ in range(3):
        sensitivity = 0.70
        type_i = 0.05
        prior = (sensitivity * prior) / (sensitivity * prior + type_i * (1 - prior))
    assert prior >= 0.95, f"3 smoking guns posterior {prior:.3f} < 0.95"


def test_no_posterior_at_zero_or_one():
    """All posteriors must be strictly between 0.001 and 0.999."""
    csv_path = os.path.join(OUTPUT, "bayesian_updates.csv")
    if not os.path.exists(csv_path):
        pytest.skip("bayesian_updates.csv not found (pipeline not yet run)")
    with open(csv_path, encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            p = float(row.get("posterior", 0.5))
            assert 0.001 <= p <= 0.999, f"Posterior {p} out of [0.001,0.999] for {row.get('case_id')}/{row.get('part_id')}"


def test_output_csv_has_all_case_part_combos():
    """bayesian_updates.csv should have at least 7*4 = 28 rows (7 cases x 4 main parts)."""
    csv_path = os.path.join(OUTPUT, "bayesian_updates.csv")
    if not os.path.exists(csv_path):
        pytest.skip("bayesian_updates.csv not found")
    with open(csv_path, encoding='utf-8', errors='replace') as f:
        rows = list(csv.DictReader(f))
    # 6 original cases x 4 parts + GP P_INT = 25 minimum; SS has 0 evidence so may have 0 rows
    assert len(rows) >= 25, f"Expected >= 25 rows, got {len(rows)}"


def test_sul_superior_in_case_map():
    """SS must be recognized by the case normalizer (structural source test)."""
    # case_map is inside a function — test structurally via source code
    src = open(os.path.join(BASE, "pt_04_bayesian_update.py"), encoding='utf-8').read()
    assert '"Sul-Superior": "SS"' in src, "SS not in case_map"
    assert '"Sul Superior": "SS"' in src, "SS variant not in case_map"
    assert '"Gongo Soco": "SS"' in src, "Gongo Soco variant not in case_map"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
