from hypothesis import given, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed


@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    try:
        result = parse_vitals_summary(s)
    except Exception as e:
        assert False, f"parse_vitals_summary crashed with: {e!r} on input {s!r}"
    # Property: function must always return a string
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    try:
        result = compute_patient_bmi(s)
    except Exception as e:
        assert False, f"compute_patient_bmi crashed with: {e!r} on input {s!r}"
    # Property: result is either a valid BMI number or an error message string
    assert isinstance(result, (float, str))


@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    try:
        result = assign_ward_bed(s)
    except Exception as e:
        assert False, f"assign_ward_bed crashed with: {e!r} on input {s!r}"
    # Property: function must always return a string
    assert isinstance(result, str)