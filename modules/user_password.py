import bcrypt
import os

# Function to register a new user and hash their password
def register_user(plaintext_password):
    # Generate a unique random salt
    salt = bcrypt.gensalt()

    # Hash the plaintext password with the salt
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), salt)

    # Store the username, salt, and hashed password in the .status file
    store_user_credentials(salt, hashed_password)

# Function to store user credentials in the .status file
def store_user_credentials(salt, hashed_password):
    with open(".status", "a") as status_file:
        status_file.write("\n")
        status_file.write("-" * 40)
        status_file.write("\nLogin user and password:\n")
        status_file.write(f"\nusername: admin\n")
        status_file.write(f"salt: {salt.decode('utf-8')}\n")
        status_file.write(f"hashed_password: {hashed_password.decode('utf-8')}")

# Function to retrieve user credentials from the .status file
def retrieve_user_credentials():
    if not os.path.isfile(".status"):
        return None, None, None

    with open(".status", "r") as status_file:
        lines = status_file.readlines()

    username = None
    salt = None
    hashed_password = None

    for line in lines:
        parts = line.split(": ")
        if len(parts) != 2:
            continue
        key, value = parts
        if key == "username":
            username = value.strip()
        elif key == "salt":
            salt = value.strip().encode('utf-8')
        elif key == "hashed_password":
            hashed_password = value.strip().encode('utf-8')

    return username, salt, hashed_password

# Function to verify a user's login credentials
def verify_user_login(plaintext_password):
    # Retrieve user credentials from the .status file
    _, salt, hashed_password = retrieve_user_credentials()

    if salt is None or hashed_password is None:
        return False  # No stored credentials

    # Hash the provided plaintext password with the retrieved salt
    entered_password_hash = bcrypt.hashpw(plaintext_password.encode('utf-8'), salt)

    # Compare the entered password hash with the stored hashed password
    return entered_password_hash == hashed_password

# Function to delete user credentials from the .status file
def delete_user_credentials():
    if os.path.isfile(".status"):
        with open(".status", "r") as status_file:
            lines = status_file.readlines()

        with open(".status", "w") as status_file:
            for line in lines:
                if line.strip() in ["username:", "salt:", "hashed_password:"]:
                    # Stop writing after reaching these lines
                    break
                status_file.write(line)
        print("User credentials deleted.")
    else:
        print("No user credentials found to delete.")
