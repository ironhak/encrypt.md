import os
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

# Function to generate a random encryption key
def generate_encryption_key():
    return Fernet.generate_key()

# Convert simple text into a Fernet-compatible encryption key
def derive_fernet_key(passphrase,salt):
    #my_salt = 'fuck-you-this-is-private'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Fernet keys are 32 bytes long
        salt=salt, #.encode('utf-8'),
        iterations=100000  # You can adjust the number of iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

# Function to encrypt text using Fernet encryption
def encrypt_text(text, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_text = cipher_suite.encrypt(text)
    return encrypted_text

# Function to decrypt text using Fernet decryption
def decrypt_text(encrypted_text, decryption_key):
    try:
        cipher_suite = Fernet(decryption_key)
        decrypted_text = cipher_suite.decrypt(encrypted_text)
        return decrypted_text.decode('utf-8')
    except InvalidToken:
        # Handle the case where the key is incorrect
        return None  # or raise an exception, log an error, etc.

# Function to encrypt text below YAML block in .md file and print the key
def encrypt_md_file(file_path,passphrase,salt):
    encryption_key = derive_fernet_key(passphrase,salt)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regular expressions to find the YAML block and text below it
    match = re.search(r'---\s*(.*?)\s*---\s*(.*)', content, re.DOTALL)
    if match:
        yaml_block, text_to_encrypt = match.groups()
        encrypted_text = encrypt_text(text_to_encrypt.encode('utf-8'), encryption_key)

        # Replace the original text with the encrypted text
        updated_content = f'---\n{yaml_block}\n---\n{encrypted_text.decode("utf-8")}'

        # Write the updated content back to the same file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

# Function to decrypt .md file using a provided key
def decrypt_md_file(file_path, passphrase,salt):
    decryption_key = derive_fernet_key(passphrase,salt)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regular expressions to find the YAML block and encrypted text below it
    match = re.search(r'---\s*(.*?)\s*---\s*(.*)', content, re.DOTALL)
    if match:
        yaml_block, encrypted_text = match.groups()
        decrypted_text = decrypt_text(encrypted_text.encode('utf-8'), decryption_key)

        # Replace the original text with the decrypted text
        updated_content = f'---\n{yaml_block}\n---\n{decrypted_text}'

        # Write the updated content back to the same file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)


### BATCH operations
# Encrypt all
def encrypt_all_md(root_folder,passphrase,salt):
    for root, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                encrypt_md_file(file_path,passphrase,salt)
                print(f'🔐 {file_path} successfully encrypted ')

def decrypt_all_md(root_folder,passphrase,salt):
    for root, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                decrypt_md_file(file_path,passphrase,salt)
                print(f'🔓 {file_path} successfully decrypted ')
