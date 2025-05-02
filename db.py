import sqlite3

def get_connection():
    return sqlite3.connect("bank.db")

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            is_admin INTEGER DEFAULT 0
        )
    ''')

    # Insert default admin and customer only if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, pin, balance, is_admin) VALUES (?, ?, ?, ?)",
                       ('admin', 'admin123', 1000.0, 1))  # Admin
        cursor.execute("INSERT INTO users (username, pin, balance, is_admin) VALUES (?, ?, ?, ?)",
                       ('customer1', 'cust123', 500.0, 0))  # Customer

        print("🔑 Admin and customer test accounts created.")

    conn.commit()
    conn.close()
