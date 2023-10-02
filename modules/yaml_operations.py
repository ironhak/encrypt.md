import re
from datetime import datetime
import pytz  # For working with time zones
import os

# Function to extract the datetime for a specified property from the file
def extract_datetime(file_path, property):
    datetime_value = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(fr'^\s*{property}:\s*(.*)$', line)
            if match:
                time_str = match.group(1)
                try:
                    # Parse the datetime string and convert to UTC
                    datetime_value = datetime.fromisoformat(time_str)
                    datetime_value = datetime_value.astimezone(pytz.UTC)
                except ValueError:
                    pass
                break
    return datetime_value

def extract_yaml(file_path, property):

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(fr'^\s*{property}:\s*(.*)$', line)
            if match:
                yaml_str = match.group(1)
                try:
                    # Parse the datetime string and convert to UTC
                    print(yaml_str)
                except ValueError:
                    pass
                break
    return yaml_str

# Function to copy content of "created: " YAML and paste it on "modified: " YAML
def reset_modified_yaml_timestamp(file_path):
    modified_line_index = None
    created_timestamp = None

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == '---':
            # Find the start and end of the YAML block
            yaml_block_start = i + 1
            yaml_block_end = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '---':
                    yaml_block_end = j
                    break

            if yaml_block_end is not None:
                for j in range(yaml_block_start, yaml_block_end):
                    yaml_line = lines[j].strip()
                    if yaml_line.startswith("created: "):
                        created_timestamp = yaml_line.split("created: ", 1)[1]
                        break

        if line.strip().startswith("modified: "):
            modified_line_index = i

    if modified_line_index is not None and created_timestamp:
        lines[modified_line_index] = f"modified: {created_timestamp}\n"

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            print("Updated file:", file_path)
    else:
        print("File format not recognized or missing 'modified:' or YAML content.")


# Function to find all .md files, extract the $property datetime value and modify file creation/modified date
# according to the YAML value extracted
def update_dates(root_folder,reset_modified):
    for root, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)

                if reset_modified:
                    reset_modified_yaml_timestamp(file_path)
                    print("\tReset YAML modified date")

                datetime_value = extract_datetime(file_path, 'modified')
                print("Working on: ", file_path)
                if datetime_value:
                    #if property == 'created':
                    #    os.utime(file_path, (datetime.now().timestamp(), datetime.now().timestamp()))
                    #  os.utime(file_path, (datetime_value.timestamp(), datetime_value.timestamp()))
                    #    os.utime(file_path, (datetime_value.timestamp(), datetime_value.timestamp()))
                    #    modified = extract_datetime(file_path, 'modified')
                    #    os.utime(file_path, (datetime_value.timestamp(), modified.timestamp()))

                    os.utime(file_path, (datetime_value.timestamp(), datetime_value.timestamp()))
                    print(f'\tUpdated file modified date')

def yaml_to_timestamp(root_folder,property):
    for root, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                datetime_value = extract_datetime(file_path, property)

                if datetime_value:
                    os.utime(file_path, (datetime_value.timestamp(), datetime_value.timestamp()))

                print(f'\tUpdated file {property} date')
