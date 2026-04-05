#!/usr/bin/env python3
"""TDD tests for pt_01_mechanism_spec.py — mechanism specification validation."""
import sys, os, json, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pt_01_mechanism_spec import BRAZILIAN_CASES, MECHANISM, VAN_EVERA_TESTS, BAYESIAN_CONFIG


def test_n_cases_is_7():
    """Sul Superior (SS) must be the 7th case."""
    assert len(BRAZILIAN_CASES) == 7, f"Expected 7 cases, got {len(BRAZILIAN_CASES)}"


def test_all_case_ids_unique():
    ids = [c["case_id"] for c in BRAZILIAN_CASES]
    assert len(ids) == len(set(ids)), f"Duplicate case IDs: {ids}"


def test_sul_superior_present():
    ss = [c for c in BRAZILIAN_CASES if c["case_id"] == "SS"]
    assert len(ss) == 1, "Sul Superior (SS) not found in BRAZILIAN_CASES"
    assert ss[0]["CAT"] == 0.17, f"SS CAT should be 0.17, got {ss[0]['CAT']}"
    assert ss[0]["ENF"] == 0.83, f"SS ENF should be 0.83"


def test_all_cases_have_required_fields():
    required = {"case_id", "name", "classification", "pathway", "CAT", "DIV", "REG", "ENF", "ORG", "POL", "year"}
    for case in BRAZILIAN_CASES:
        missing = required - set(case.keys())
        assert not missing, f"Case {case.get('case_id', '?')}: missing fields {missing}"


def test_all_parts_have_fingerprints():
    for part in MECHANISM["parts"]:
        assert len(part["fingerprints"]) >= 1, f"{part['part_id']} has no fingerprints"


def test_priors_in_valid_range():
    for part in MECHANISM["parts"]:
        p = part["prior"]
        assert 0 < p < 1, f"{part['part_id']} prior={p} out of (0,1)"


def test_fingerprint_test_types_valid():
    valid_types = {"hoop", "smoking_gun", "straw_in_wind", "doubly_decisive"}
    for part in MECHANISM["parts"]:
        for fp in part["fingerprints"]:
            assert fp["van_evera_test"] in valid_types, \
                f"{part['part_id']}/{fp['id']}: invalid test type '{fp['van_evera_test']}'"


def test_sensitivity_bounds():
    for part in MECHANISM["parts"]:
        for fp in part["fingerprints"]:
            s = fp["sensitivity"]
            t = fp["type_i_error"]
            assert 0.10 <= s <= 0.99, f"{fp['id']}: sensitivity={s} out of [0.10,0.99]"
            assert 0.01 <= t <= 0.70, f"{fp['id']}: type_i={t} out of [0.01,0.70]"


def test_mechanism_has_4_main_parts_plus_pint():
    part_ids = [p["id"] for p in MECHANISM["parts"]]
    assert "P1" in part_ids
    assert "P2" in part_ids
    assert "P3" in part_ids
    assert "P4" in part_ids
    assert "P_INT" in part_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
