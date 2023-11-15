import json
import re

input_file = '../code/first-answer.json'
output_file = '../code/TAL_SAQ6K_EN_prediction.json'

new_data = {}

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for key, value in data.items():
    # 截取||后面的部分
    parts = value.split("||")

    if len(parts) > 1:
        result = parts[1]
        # 去除前后空格
        result = result.strip()
        # 去除最后一个小数点
        if result.endswith("."):
            result = result[:-1]
        # 去除美元符号
        result = result.replace("$", "").replace("£", "")

        match = re.findall(r'[-+]?\d*\.\d+|\d+|\d*\.?\d+', result[::-1])
        if match:
            result = match[0][:-1]

    else:
        result = "There is no answer."

    new_data[key] = result

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)
