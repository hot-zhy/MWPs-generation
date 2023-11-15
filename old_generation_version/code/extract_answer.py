import json

jsonl_input_file = './final_result.jsonl'
json_data = {}

with open(jsonl_input_file, 'r', encoding='utf-8') as jsonl_file:
    for line in jsonl_file:
        json_object = json.loads(line)
        que_id = json_object['queId']
        answer = json_object['answer']
        json_data[que_id] = answer

json_file_path = '../code/first-answer.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4)
