from datetime import datetime

CURRENT_YEAR = datetime.now().year


def calculate_risk(detection):
    if not detection or not detection.get("found"):
        return {"level": "Safe", "score": 0, "reasons": []}

    score = 0
    reasons = []
    records = detection.get("records", [])

    # Check for specific risk factors
    has_password = any(r.get("password_status") == "Leaked" for r in records)
    is_recent = any("2025" in str(r.get("breach_date")) or "2026" in str(r.get("breach_date")) for r in records)
    high_volume = len(records) > 3

    if has_password:
        score += 5
        reasons.append("Password exposed.")
    if is_recent:
        score += 3
        reasons.append("Recent breach.")
    if high_volume:
        score += 2
        reasons.append("Multiple data leaks found.")

    level = "Low"
    if score >= 7: level = "Critical"
    elif score >= 4: level = "Medium"

    return {"level": level, "score": min(score, 10), "reasons": reasons}