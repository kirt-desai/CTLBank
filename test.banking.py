import unittest
import sqlite3
from db import initialize_db, get_connection
from banking import create_account, deposit, withdraw, check_balance
from auth import validate_login

class TestBankingApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize a fresh database
        initialize_db()

    def setUp(self):
        # Clear and reset the database before each test
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        # Insert a test user
        cursor.execute("INSERT INTO users (username, pin, balance, is_admin) VALUES (?, ?, ?, ?)",
                       ('testuser', '1234', 500.0, 0))
        conn.commit()
        conn.close()

    def test_create_account(self):
        create_account("newuser", "9999")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username='newuser'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        conn.close()

    def test_validate_login_success(self):
        result = validate_login("testuser", "1234")
        self.assertIsNotNone(result)
        self.assertEqual(result['user_id'], 1)

    def test_validate_login_failure(self):
        result = validate_login("wronguser", "0000")
        self.assertIsNone(result)

    def test_check_balance(self):
        balance = check_balance(1)
        self.assertEqual(balance, 500.0)

    def test_deposit(self):
        deposit(1, 200.0)
        new_balance = check_balance(1)
        self.assertEqual(new_balance, 700.0)

    def test_withdraw_success(self):
        withdraw(1, 300.0)
        new_balance = check_balance(1)
        self.assertEqual(new_balance, 200.0)

    def test_withdraw_insufficient_funds(self):
        withdraw(1, 1000.0)
        # Balance should remain unchanged
        new_balance = check_balance(1)
        self.assertEqual(new_balance, 500.0)

if __name__ == '__main__':
    unittest.main()
