import time
import hashlib

# Data storage
usernames = []
passwords = []
failed_attempts = []

# Hash Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Password Checker without using any()
def check_password(password):
    errors = []

    has_digit = False
    has_upper = False
    has_special = False

    # Check each character
    for char in password:
        if char.isdigit():
            has_digit = True
        if char.isupper():
            has_upper = True
        if char in "!@#$%^&*":
            has_special = True

    if len(password) < 8:
        errors.append("8+ characters")
    if not has_digit:
        errors.append("a number")
    if not has_upper:
        errors.append("an uppercase letter")
    if not has_special:
        errors.append("a special character (!@#$%^&*)")

    return "Strong" if not errors else "Weak: add " + ", ".join(errors)

# Register User
def registration():
    username = input("Enter username: ")
    password = input("Enter password (min 8 chars, include number, uppercase, special characters): ")

    if username in usernames:
        print("Username already exists.")
        return

    strength = check_password(password)
    if strength != "Strong":
        print(strength)
        return

    usernames.append(username)
    passwords.append(hash_password(password))
    failed_attempts.append(0)
    print("Registration successful.")

# Login
def login():
    username = input("Enter username: ")

    if username not in usernames:
        print("Username or password is incorrect.")
        return

    index = usernames.index(username)
    attempts_left = 3 - failed_attempts[index]

    while attempts_left > 0:
        password = input("Enter password: ")

        if hash_password(password) == passwords[index]:
            print("Login successful.")
            failed_attempts[index] = 0
            return
        else:
            failed_attempts[index] += 1
            attempts_left -= 1
            print("Username or password is incorrect.")
            print("Attempts left:", attempts_left)

        # Lock account after 3 failed attempts
        if failed_attempts[index] >= 3:
            print("Account locked due to too many failed attempts.")
            print("Please wait 1 minute before trying again.")

            for x in range(60, 0, -1):
                seconds = x % 60
                minutes = int(x / 60) % 60
                hours = int(x / 3600)
                print(f"{hours:02}:{minutes:02}:{seconds:02}")
                time.sleep(1)

            failed_attempts[index] = 0  # Reset after cooldown
            print("\nYou can try logging in again now.")
            return

# Menu
while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose option (1,2,3): ")

    if choice == "1":
        registration()
    elif choice == "2":
        if not usernames:
            print("No account found. Please register first.")
        else:
            login()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")