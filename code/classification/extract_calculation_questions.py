import openpyxl
import jsonlines
import re

import openpyxl
import jsonlines
import re


def extract_data_to_jsonl(file_path, keywords, output_file):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    extracted_data = []

    # 获取列的索引
    column_indices = {
        'dataset_version': None,
        'queid': None,
        'difficulty': None,
        'qtype': None,
        'problem': None,
        'knowledge_point_routes': None
    }
    for cell in sheet[1]:
        column_name = str(cell.value).lower()
        if column_name in column_indices:
            column_indices[column_name] = cell.column

    for row in sheet.iter_rows(values_only=True):
        problem_value = str(row[column_indices['problem'] - 1])
        if any(re.search(keyword, problem_value, re.IGNORECASE) for keyword in keywords):
            item = {
                'dataset_version': str(row[column_indices['dataset_version'] - 1]),
                'queId': str(row[column_indices['queid'] - 1]),
                'difficulty': str(row[column_indices['difficulty'] - 1]),
                'qtype': str(row[column_indices['qtype'] - 1]),
                'problem': problem_value,
                'knowledge_point_routes': str(row[column_indices['knowledge_point_routes'] - 1])
            }
            extracted_data.append(item)

    with jsonlines.open(output_file, mode='w') as writer:
        for item in extracted_data:
            writer.write(item)


# 示例用法
file_path = '../TAL-SAQ6K-EN.xlsx'
keywords = ['work out', 'calculate',
            'find the value of', 'compute', 'find the number of']
output_file = 'extract.jsonl'

extract_data_to_jsonl(file_path, keywords, output_file)
