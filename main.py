from db import initialize_db
from auth import validate_login
from banking import create_account, check_balance, deposit, withdraw

def main():
    initialize_db()
    print("=== Welcome to CDL Bank ===")

    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Username: ")
            pin = input("PIN: ")
            user = validate_login(username, pin)
            if user:
                print("Login successful!")
                user_session(user["user_id"], user["is_admin"])
            else:
                print(" Invalid credentials.")

        elif choice == '2':
            username = input("Choose a username: ")
            pin = input("Choose a PIN: ")
            create_account(username, pin)

        elif choice == '3':
            print("Goodbye!")
            break

def user_session(user_id, is_admin):
    while True:
        print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout")
        action = input("Choose an action: ")

        if action == '1':
            balance = check_balance(user_id)
            print(f"💰 Your balance: ${balance:.2f}")
        elif action == '2':
            amount = float(input("Enter amount to deposit: "))
            deposit(user_id, amount)
            print("✅ Deposit successful.")
        elif action == '3':
            amount = float(input("Enter amount to withdraw: "))
            withdraw(user_id, amount)
        elif action == '4':
            print(" Logged out.")
            break

if __name__ == "__main__":
    main()
