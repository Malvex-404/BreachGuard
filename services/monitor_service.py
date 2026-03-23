from database.db import get_connection
from services.breach_service import detect_query
from services.notification_service import create_notification


def add_monitor_email(user_id, email):

    conn = get_connection()
    cursor = conn.cursor()

    # verify user exists
    cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return

    cursor.execute("""
        INSERT INTO monitored_emails (user_id, email)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE email=email
    """, (user_id, email))

    conn.commit()

    cursor.close()
    conn.close()


def remove_monitor_email(user_id, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM monitored_emails WHERE user_id=%s AND email=%s",
        (user_id, email)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_monitored_emails(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM monitored_emails WHERE user_id = %s",
        (user_id,)
    )

    emails = cursor.fetchall()

    cursor.close()
    conn.close()

    return emails


def check_monitor_status(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    monitored = get_monitored_emails(user_id)
    results = []

    for item in monitored:

        email = item["email"]
        detection = detect_query(email)

        if not detection:
            results.append({
                "email": email,
                "breached": False,
                "records": []
            })
            continue

        records = detection.get("records", [])

        # Remove duplicate breaches
        unique_records = []
        seen = set()

        for r in records:
            key = (r["breach"], r.get("breach_date"))
            if key not in seen:
                seen.add(key)
                unique_records.append(r)

        records = unique_records

        for record in records:

            breach = record["breach"]

            cursor.execute("""
                SELECT resolved
                FROM monitored_breach_status
                WHERE user_id=%s AND email=%s AND breach_name=%s
            """, (user_id, email, breach))

            status = cursor.fetchone()

            # Correct resolution detection
            if status:
                record["resolved"] = bool(status["resolved"])
            else:
                record["resolved"] = False

            # Only create notification if breach not resolved
            if not record["resolved"]:
                create_notification(user_id, email, breach)

        results.append({
            "email": email,
            "breached": len(records) > 0,
            "records": records
        })

    cursor.close()
    conn.close()

    return results


def mark_breach_resolved(user_id, email, breach_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO monitored_breach_status 
        (user_id, email, breach_name, resolved, resolved_at)
        VALUES (%s, %s, %s, TRUE, NOW())
        ON DUPLICATE KEY UPDATE
        resolved=TRUE,
        resolved_at=NOW()
    """, (user_id, email, breach_name))

    conn.commit()
    cursor.close()
    conn.close()