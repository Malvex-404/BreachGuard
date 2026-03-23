from database.db import get_connection


def create_notification(user_id, email, breach_name):

    conn = get_connection()
    cursor = conn.cursor()

    message = f"Breach detected for {email} in {breach_name}"

    cursor.execute("""
        INSERT INTO breach_notifications (user_id, email, breach_name, message)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id
    """, (user_id, email, breach_name, message))

    conn.commit()
    cursor.close()
    conn.close()


def get_notifications(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM breach_notifications
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (user_id,))

    alerts = cursor.fetchall()

    cursor.close()
    conn.close()

    return alerts


def mark_notification_read(notification_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE breach_notifications
        SET is_read = TRUE
        WHERE id=%s
    """, (notification_id,))

    conn.commit()
    cursor.close()
    conn.close()


def unread_notification_count(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM breach_notifications
        WHERE user_id=%s AND is_read=FALSE
    """, (user_id,))

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count