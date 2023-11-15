import json

file_path = '../code/final_result.jsonl'

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for line_number, line in enumerate(lines, start=1):
    try:
        json.loads(line)
    except json.JSONDecodeError as e:
        print(f"Error in line {line_number}: {e}:{line}")
        # You can choose to remove the problematic line or fix it

# You can also use this script to automatically clean the file by removing problematic lines
