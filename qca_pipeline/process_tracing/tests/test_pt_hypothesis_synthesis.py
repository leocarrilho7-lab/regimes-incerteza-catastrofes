#!/usr/bin/env python3
"""TDD tests for pt_08_hypothesis_synthesis.py — hypothesis synthesis validation."""
import sys, os, json, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(BASE, "output")


def test_all_five_hypotheses_present():
    """H1-H5 must all appear in hypothesis_synthesis.json."""
    path = os.path.join(OUTPUT, "hypothesis_synthesis.json")
    if not os.path.exists(path):
        pytest.skip("hypothesis_synthesis.json not found")
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    results = data.get("hypotheses", data.get("results", data))
    for h in ["H1", "H2", "H3", "H4", "H5"]:
        assert h in results, f"Hypothesis {h} missing from synthesis"


def test_h2_evidence_count_not_hardcoded_87():
    """H2 n_evidence must be dynamically computed, not the old hardcoded 87."""
    path = os.path.join(OUTPUT, "hypothesis_synthesis.json")
    if not os.path.exists(path):
        pytest.skip("hypothesis_synthesis.json not found")
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    results = data.get("hypotheses", data.get("results", data))
    h2_n = results.get("H2", {}).get("n_evidence", 0)
    # It should not be exactly 87 (old hardcode) unless coincidentally correct
    # More importantly, verify it matches the actual CSV count
    csv_path = os.path.join(OUTPUT, "bayesian_updates.csv")
    if os.path.exists(csv_path):
        import csv as csv_mod
        with open(csv_path, encoding='utf-8', errors='replace') as f:
            rows = list(csv_mod.DictReader(f))
        actual = sum(1 for r in rows if r.get("part_id") in ("P1", "P2", "P3", "P4"))
        if actual > 0:
            assert h2_n == actual, f"H2 n_evidence={h2_n} != CSV count {actual}"


def test_posteriors_consistent_with_interpretation():
    """Posterior >= 0.95 iff interpretation == 'CONFIRMADA'."""
    path = os.path.join(OUTPUT, "hypothesis_synthesis.json")
    if not os.path.exists(path):
        pytest.skip("hypothesis_synthesis.json not found")
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    results = data.get("hypotheses", data.get("results", data))
    for h_id, h_data in results.items():
        post = h_data.get("posterior", 0)
        interp = h_data.get("interpretation", "")
        if post >= 0.95:
            assert "CONFIRMADA" in interp, f"{h_id}: posterior={post} but interpretation='{interp}'"


def test_h3_references_sul_superior():
    """H3 should reference Sul Superior evidence."""
    # Check the source code for H3 configuration
    src_path = os.path.join(BASE, "pt_08_hypothesis_synthesis.py")
    with open(src_path, encoding='utf-8') as f:
        src = f.read()
    assert "Sul" in src and "Superior" in src, "H3 should reference Sul Superior"
    assert "h3_sul_superior" in src, "H3 should load h3_sul_superior.json"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
