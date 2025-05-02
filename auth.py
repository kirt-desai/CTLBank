from db import get_connection

def validate_login(username, pin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, is_admin FROM users WHERE username = ? AND pin = ?", (username, pin))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"user_id": result[0], "is_admin": bool(result[1])}
    return None
