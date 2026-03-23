import bcrypt
from database.db import get_connection


import bcrypt
from database.db import get_connection


def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {"success": False, "message": "Email already registered"}

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, hashed_password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True, "message": "Registration successful"}


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return {"success": False, "message": "User not found"}

    stored_hash = user["password_hash"]

    # If stored as string, convert to bytes
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return {"success": True, "user": user}

    return {"success": False, "message": "Invalid password"}