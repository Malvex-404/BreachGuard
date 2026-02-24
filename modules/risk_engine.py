from datetime import datetime

CURRENT_YEAR = datetime.now().year


def calculate_risk(detection_result):
    """
    Safely calculates risk score and level.
    Works even if some fields are missing.
    """

    # No breach found
    if not detection_result or not detection_result.get("found"):
        return {
            "score": 0,
            "level": "LOW",
            "reasons": ["No breach detected."]
        }

    score = 0
    reasons = []

    records = detection_result.get("records", [])

    for record in records:

        # 🔴 Password Exposure Check
        if record.get("password_status") == "Leaked":
            score += 5
            reasons.append("Password exposed.")

        # 📅 Breach Date Check (safe parsing)
        breach_date = record.get("breach_date")

        if breach_date:
            try:
                breach_year = int(str(breach_date)[:4])
                age = CURRENT_YEAR - breach_year

                if age <= 2:
                    score += 4
                    reasons.append("Recent breach.")
                elif age <= 5:
                    score += 2
                else:
                    score += 1
            except:
                pass

        # ⚠️ Attack Type Severity
        attack = record.get("attack_type", "")

        if attack in ["Credential Stuffing", "Database Leak", "Web Vulnerability"]:
            score += 3
            reasons.append("High severity attack.")

    # 📊 Multiple Records (domain exposure)
    if len(records) > 1:
        score += 3
        reasons.append("Multiple exposures.")

    # 🧠 Final Classification
    if score >= 12:
        level = "CRITICAL"
    elif score >= 8:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "reasons": list(set(reasons))
    }