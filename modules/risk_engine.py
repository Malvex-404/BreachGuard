def calculate_risk(records):
    if not records:
        return "LOW"

    score = 0

    for r in records:
        if r["password_exposed"] == "Yes":
            score += 3
        if int(r["year"]) >= 2022:
            score += 2
        else:
            score += 1

    if score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"