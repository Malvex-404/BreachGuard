def mask_password(password_hint, exposed_flag):
    """
    Returns safe display version of password info.
    """

    if exposed_flag != "Yes":
        return {
            "status": "Safe",
            "display": None
        }

    if password_hint == "Not Available":
        return {
            "status": "Leaked",
            "display": "Unknown"
        }

    # Show only last 3 characters
    visible = password_hint[-3:]

    masked = "********" + visible

    return {
        "status": "Leaked",
        "display": masked
    }