import math


def _to_finite_float(text):
    """Convert text to a float; return None if invalid, NaN or infinite."""
    try:
        value = float(text.strip())
    except (ValueError, TypeError, AttributeError, OverflowError):
        return None
    if not math.isfinite(value):
        return None
    return value


def parse_vitals_summary(vitals_csv):
    # Input validation: must be a string
    if not isinstance(vitals_csv, str):
        return "Invalid input: vitals must be a string 'HR,SpO2,Temp'"

    parts = vitals_csv.split(',')
    if len(parts) != 3:
        return "Invalid input: expected exactly 3 values 'HR,SpO2,Temp'"

    hr = _to_finite_float(parts[0])
    spo2 = _to_finite_float(parts[1])
    temp = _to_finite_float(parts[2])
    if hr is None or spo2 is None or temp is None:
        return "Invalid input: HR, SpO2 and Temp must be finite numbers"

    # Range checks (physiologically plausible values)
    if hr <= 0 or not (0 <= spo2 <= 100) or not (25 <= temp <= 45):
        return "Invalid input: value out of realistic range"

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        return "Invalid input: expected a string 'weight/height'"

    parts = bmi_string.split('/')
    if len(parts) != 2:
        return "Invalid input: expected format 'weight/height'"

    weight = _to_finite_float(parts[0])
    height = _to_finite_float(parts[1])
    if weight is None or height is None:
        return "Invalid input: weight and height must be finite numbers"
    if weight <= 0 or height <= 0:
        return "Invalid input: weight and height must be positive"

    try:
        bmi = weight / (height ** 2)
        if not math.isfinite(bmi):
            return "Invalid input: BMI could not be computed"
        return round(bmi, 2)
    except (ZeroDivisionError, OverflowError):
        return "Invalid input: BMI could not be computed"


def assign_ward_bed(allocation_code):
    if not isinstance(allocation_code, str):
        return "Invalid input: expected a string like 'ICU-05'"

    parts = allocation_code.strip().split('-')
    if len(parts) != 2:
        return "Invalid input: expected format 'WARD-BED'"

    ward, bed_str = parts[0].strip(), parts[1].strip()
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    ward_key = ward.upper()
    if ward_key not in ward_names:
        return f"Invalid input: unknown ward '{ward}'"

    # isascii() + isdigit() rejects unicode digits, '+', '_' and empty strings
    if not (bed_str.isascii() and bed_str.isdigit()):
        return "Invalid input: bed number must be a non-negative integer"
    if len(bed_str) > 6:
        return "Invalid input: bed number too large"

    bed_num = int(bed_str)
    if bed_num < 1:
        return "Invalid input: bed number must be at least 1"

    return f"{ward_names[ward_key]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()