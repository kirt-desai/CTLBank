import sqlite3
from db import get_connection

def create_account(username, pin, is_admin=0):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, pin, is_admin) VALUES (?, ?, ?)", (username, pin, is_admin))
        conn.commit()
        print("✅ Account created successfully!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    conn.close()

def check_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def deposit(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def withdraw(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    if amount > balance:
        print("❌ Insufficient funds.")
    else:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
        conn.commit()
        print("✅ Withdrawal successful.")
    conn.close()
