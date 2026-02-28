import re

def analyze_password(password):

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Include numbers.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    levels = ["Weak", "Moderate", "Strong", "Very Strong"]

    return {
        "strength_score": score,
        "strength_level": levels[score-1] if score else "Weak",
        "feedback": feedback
    }