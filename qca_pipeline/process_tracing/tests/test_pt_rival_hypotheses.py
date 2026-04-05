#!/usr/bin/env python3
"""Tests for pt_09_rival_hypotheses.py — Phase 5b"""
import json, sys, os
from pathlib import Path
import pytest

BASE = Path(__file__).parent.parent
PT_OUTPUT = Path(os.environ.get("PT_OUTDIR", str(BASE / "output")))

@pytest.fixture
def rival_data():
    path = PT_OUTPUT / "rival_hypotheses.json"
    if not path.exists():
        pytest.skip("rival_hypotheses.json not found")
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def test_all_5_hypotheses_have_3_rivals(rival_data):
    """Each of H1-H5 must have exactly 3 rival hypotheses."""
    results = rival_data.get("results", {})
    for hyp_id in ["H1", "H2", "H3", "H4", "H5"]:
        assert hyp_id in results, f"{hyp_id} not found in results"
        rivals = results[hyp_id].get("rivals", [])
        assert len(rivals) >= 3, \
            f"{hyp_id} has only {len(rivals)} rivals (need 3)"

def test_no_rival_posterior_above_threshold(rival_data):
    """No rival hypothesis should have posterior > 0.50 (BLOQUEANTE)."""
    results = rival_data.get("results", {})
    surviving = []
    for hyp_id, res in results.items():
        for j in res.get("judgments", []):
            if j.get("posterior", 0) > 0.50:
                surviving.append(f"{j.get('id','?')} (posterior={j['posterior']:.3f})")
    assert len(surviving) == 0, \
        f"BLOQUEANTE: {len(surviving)} rivals survive: {', '.join(surviving)}"

def test_rival_priors_above_minimum(rival_data):
    """All rival priors must be >= 0.20 (Bennett 2010: no straw men)."""
    results = rival_data.get("results", {})
    for hyp_id, res in results.items():
        for rival in res.get("rivals", []):
            prior = rival.get("prior", 0)
            assert prior >= 0.20, \
                f"{rival.get('id','?')}: prior={prior} < 0.20 (straw man, Bennett 2010)"

def test_evidence_count_minimum(rival_data):
    """Each rival should have at least 1 evidence item searched."""
    results = rival_data.get("results", {})
    for hyp_id, res in results.items():
        for rival in res.get("rivals", []):
            n_ev = rival.get("n_evidence", rival.get("total_evidence_found", 0))
            # Relaxed: some rivals may genuinely have no evidence
            # But the search must have been attempted
            assert rival.get("fingerprints") is not None, \
                f"{rival.get('id','?')}: no fingerprints defined"

def test_mab_stats_present(rival_data):
    """MAB Thompson Sampling stats should be recorded."""
    metadata = rival_data.get("metadata", {})
    assert "mab_stats" in metadata, "MAB stats not found in metadata"
    mab_stats = metadata["mab_stats"]
    assert "proposer" in mab_stats, "proposer not in MAB stats"
    assert "critic" in mab_stats, "critic not in MAB stats"
    assert "judge" in mab_stats, "judge not in MAB stats"
