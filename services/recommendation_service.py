def get_recommendations(record):

    actions = []

    if record["password_status"] == "Leaked":
        actions.append("Change password immediately.")
        actions.append("Enable Multi-Factor Authentication (MFA).")

    if "email" in record["data_exposed"].lower():
        actions.append("Monitor inbox for phishing emails.")

    if "phone" in record["data_exposed"].lower():
        actions.append("Beware of SMS phishing (smishing).")

    if "security question" in record["data_exposed"].lower():
        actions.append("Update security questions.")

    return actions