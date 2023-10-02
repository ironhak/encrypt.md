import os

# Function to check if a .status file exists and create it if not
def create_status_file():
    file_path = os.path.join(os.getcwd(),'.status')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("-" * 40)
            file.write("\nCheck encryption\nstatus: \n")  # You can set an initial status value

# Function to check the status from the .status file
def check_status():
    file_path = os.path.join(os.getcwd(), '.status')
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("status: "):
                status_content = line.split("status: ", 1)[1].strip()
                if status_content:
                    return status_content
    return None

def bool_status():
    status = check_status()
    if status == '🔐 Encrypted':
        return True
    elif status == '🔓 Non-encrypted':
        return False

def set_status(status):
    file_path = os.path.join(os.getcwd(),'.status')
    lines = []
    found_status = False

    status = '🔐 Encrypted' if status else '🔓 Non-encrypted'

    # Read the existing lines and update the status line if it exists
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("status: "):
                lines.append(f"status: {status}\n")
                found_status = True
            else:
                lines.append(line)

    # If "status:" is not found, add it to the end of the file
    if not found_status:
        lines.append(f"status: {status}\n")

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
