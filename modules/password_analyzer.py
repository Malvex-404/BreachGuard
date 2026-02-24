import re


def analyze_password(password, detection_records=None):
    """
    Analyze password strength and possible exposure patterns.
    Password is NEVER stored.
    """

    if not password:
        return {"error": "Password cannot be empty."}

    strength = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Use at least 8 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        feedback.append("Add uppercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        feedback.append("Include numbers.")

    # Special Characters
    if re.search(r"[!@#$%^&*]", password):
        strength += 1
    else:
        feedback.append("Add special characters.")

    # Exposure Hint Match (if breach data exists)
    exposed_match = False

    if detection_records:
        last_chars = password[-3:]

        for record in detection_records:
            hint = record.get("password_display")
            if hint and last_chars in hint:
                exposed_match = True
                break

    level = ["Weak", "Moderate", "Strong", "Very Strong"][strength - 1] if strength else "Weak"

    return {
        "strength_score": strength,
        "strength_level": level,
        "feedback": feedback,
        "exposed_pattern": exposed_match
    }