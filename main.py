import os
from modules import yaml_operations as yo
from modules import encryption as ecy
from modules import check_status
from modules import user_password as login

# Use the current working directory and specify a specific folder
current_directory = os.getcwd()
specific_folder = ''  # Change to the folder you want to use

# Set file last modified timestamp equal to YAML modified property
os.system('clear')

## INIT
check_status.create_status_file()

# Attempt to retrieve stored user credentials

_,salt, passphrase = login.retrieve_user_credentials()

if passphrase is None:
    # If no credentials are stored, register a new user
    passphrase = input("Create a new password: ")
    login.register_user(passphrase)
    print("User registered!")

while True:
    os.system('clear')
    passphrase = input("Enter your password: ")
    if login.verify_user_login( passphrase):
        print("Login successful!")
        break

while check_status.check_status() is None:
    print('Please check if your notes are encrypted.\n')
    while True:
        user_input = input('(y)yes - (n)no : ')

        if user_input == 'y':
            user_input = True
            break
        elif user_input == 'n':
            user_input = False
            break
        else:
            print('Not a valid answer.')

    check_status.set_status(user_input)
    os.system('clear')

os.system('clear')

while True:
    print(f'Your notes are {check_status.check_status()}\n' )
    print("-" * 40)  # Print a horizontal line of 40 hyphens

    if check_status.bool_status():
        print('2 - Decrypt all notes\n')
    else:
        print('1 - Encrypt all notes')
        print('\n3 - Change password')

    print('4 - Quit')
    print("-" * 40)

    user_input = input('\nChoose operation: ')

    if user_input == '1':
        if check_status.bool_status() == True:
            os.system('clear')
            print("Notes are already crypted!\n")
        else:
            ecy.encrypt_all_md(folder_path,passphrase,salt)
            yo.update_dates(folder_path,False)
            check_status.set_status(True)
            os.system('clear')
    elif user_input == '2':
        if check_status.bool_status() == True:
            ecy.decrypt_all_md(folder_path,passphrase,salt)
            yo.update_dates(folder_path,False)
            check_status.set_status(False)
            os.system('clear')
        else:
            os.system('clear')
            print("Notes are already decrypted!\n")
    elif user_input == '3' and not check_status.bool_status():
            login.delete_user_credentials()
            passphrase = input("Create a new password: ")
            login.register_user(passphrase)
            os.system('clear')
            print("User registered!\n\n")
    elif user_input == '4':
        os.system('clear')
        break
    else:
        os.system('clear')
