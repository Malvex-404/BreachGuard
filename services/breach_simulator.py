from data.tester import generate_dataset
from database.db import get_connection
from services.notification_service import create_notification

def simulate_breaches(user_id, monitored_emails):

    df = generate_dataset()

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        # Only trigger for monitored emails
        if row["email"] in monitored_emails:

            cursor.execute("""
                SELECT id FROM breach_notifications
                WHERE user_id=%s AND email=%s AND breach_name=%s
            """, (user_id, row["email"], row["breach"]))
            
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(""" INSERT ... """)

    conn.commit()
    cursor.close()
    conn.close()