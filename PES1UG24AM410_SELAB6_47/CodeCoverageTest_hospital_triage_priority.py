import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {"is_accepting": accepting, "tier": tier,
            "icu_standby": icu, "patients": patients}


# ---------- process_triage_wards ----------
def test_single_normal_patient():
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_wards_not_list():
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_invalid_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_ward_not_accepting_is_skipped():
    wards = [make_ward([{"spo2": 98, "hr": 72}], accepting=False)]
    assert process_triage_wards(wards, 10)["status"] == "NO_URGENT_CASES"


def test_invalid_vitals_are_flagged_and_skipped():
    wards = [make_ward([{"spo2": 0, "hr": 70}, {"spo2": 95, "hr": 0}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_unconscious_patient_non_outpatient():
    wards = [make_ward([{"spo2": 95, "hr": 70, "unconscious": True}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 100


def test_unconscious_patient_outpatient_resets_and_breaks():
    wards = [make_ward([{"spo2": 95, "hr": 70, "unconscious": True},
                        {"spo2": 95, "hr": 70}], tier="outpatient")]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_low_spo2_adds_60():
    wards = [make_ward([{"spo2": 85, "hr": 70}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_high_heart_rate_adds_60():
    wards = [make_ward([{"spo2": 95, "hr": 130}])]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_icu_standby_adds_25():
    wards = [make_ward([{"spo2": 98, "hr": 72}], icu=True)]
    assert process_triage_wards(wards, 10)["acuity_score"] == 35


def test_ward_alert_when_more_than_four_flags():
    wards = [make_ward([{"spo2": 0, "hr": 70}] * 5)]
    assert process_triage_wards(wards, 10)["status"] == "WARD_ALERT"


def test_default_values_used_when_keys_missing():
    result = process_triage_wards([{"is_accepting": True, "patients": [{}]}], 7)
    assert result["acuity_score"] == 7


# ---------- monitor_oxygen_manifolds ----------
def test_no_data_empty():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_pressure_failure_two_consecutive_drops():
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_pressure_normal_with_streak_reset():
    assert monitor_oxygen_manifolds([[5.0, 3.5, 5.0, 3.5]]) == "PRESSURE_NORMAL"