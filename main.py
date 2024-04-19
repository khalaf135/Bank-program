import pandas as pd
from openpyxl import load_workbook
import os

# Define the file path for the Excel database
file_path = "bank_users.xlsx"


def initialize_file():
    if not os.path.exists(file_path):
        # Create a DataFrame to hold user information if the file does not exist
        df = pd.DataFrame(columns=["Full Name", "Username", "Password", "Balance"])
        df.to_excel(file_path, index=False)


def add_account():
    # Load existing data
    df = pd.read_excel(file_path)

    full_name = input("Enter full name: ")

    # Check if username is already used
    while True:
        username = input("Enter username: ")
        if df[df['Username'] == username].empty:
            break
        else:
            print("Username already used, please try another username.")

    # Check password length
    while True:
        password = input("Enter password (must be at least 8 characters): ")
        if len(password) >= 8:
            break
        else:
            print("Password too short, it must be at least 8 characters long.")

    balance = 0  # Initialize balance to zero

    # Create a new DataFrame for the new user
    new_user_df = pd.DataFrame({
        "Full Name": [full_name],
        "Username": [username],
        "Password": [password],
        "Balance": [balance]
    })

    # Concatenate the new user DataFrame to the existing DataFrame
    df = pd.concat([df, new_user_df], ignore_index=True)

    # Save to Excel
    df.to_excel(file_path, index=False)


def enter_account():
    username = input("Enter your username: ").strip()  # Strip leading/trailing whitespace
    password = input("Enter your password: ").strip()  # Strip leading/trailing whitespace

    # Load user data
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to load user data: {e}")
        return

    # Determine if password is numeric or contains letters
    if password.isdigit():
        # If the password is all digits, convert to int for comparison
        try:
            password = int(password)
            user = df[(df["Username"].str.strip().str.lower() == username.lower()) & (df["Password"] == password)]
        except ValueError:
            print("Password conversion to integer failed.")
            return
    else:
        # Treat password as a string
        user = df[(df["Username"].str.strip().str.lower() == username.lower()) & (df["Password"] == password)]

    # Check if any user matches the criteria
    if not user.empty:
        print("Login successful!")
        account_menu(user.index[0])  # Pass user index to account menu function
    else:
        print("Invalid username or password!")


def account_menu(user_index):
    df = pd.read_excel(file_path)
    user = df.iloc[user_index]

    options = """
    1 - Show Balance
    2 - Deposit Money
    3 - Withdraw Money
    4 - Transfer Money
    5 - Logout
    """
    print(options)

    choice = input("Choose an option: ")
    if choice == '1':
        print(f"Your current balance is: ${user['Balance']}")
    elif choice == '2':
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            df.at[user_index, 'Balance'] += amount
            print(f"Deposit successful! Your new balance is: ${df.at[user_index, 'Balance']:.2f}")
        else:
            print("Invalid amount entered.")
    elif choice == '3':
        amount = float(input("Enter amount to withdraw: "))
        if amount > 0 and amount <= user['Balance']:
            df.at[user_index, 'Balance'] -= amount
            print(f"Withdrawal successful! Your new balance is: ${df.at[user_index, 'Balance']:.2f}")
        else:
            print("Insufficient funds or invalid amount entered!")
    elif choice == '4':
        recipient_username = input("Enter the username of the recipient: ")
        amount = float(input("Enter amount to transfer: "))
        recipient = df[df['Username'] == recipient_username]
        if not recipient.empty and amount > 0 and amount <= user['Balance']:
            recipient_index = recipient.index[0]
            df.at[user_index, 'Balance'] -= amount
            df.at[recipient_index, 'Balance'] += amount
            print(f"Transfer successful! Your new balance is: ${df.at[user_index, 'Balance']:.2f}")
            print(f"${amount:.2f} has been transferred to {recipient_username}.")
        else:
            print("Invalid transaction! Check recipient and amount.")
    elif choice == '5':
        print(f"Logging out. Your final balance was: ${user['Balance']:.2f}")
        return  # Logout

    df.to_excel(file_path, index=False)
    account_menu(user_index)  # Re-display menu until user logs out


def main():
    initialize_file()
    while True:
        action = input("1 - Add Account, 2 - Enter Account, 3 - Quit: ")
        if action == '1':
            add_account()
        elif action == '2':
            enter_account()
        elif action == '3':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
