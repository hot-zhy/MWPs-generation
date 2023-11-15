import json
import os
import requests
import time
import sys
import re
import sympy as sp

api_key = ''
api_url = 'https://api.ohmygpt.com/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
keywords = ['work out', 'calculate',
            'find the value of', 'compute', 'find the number of']

input_dir = "../dataset/AAAI/TAL-SAQ6K-EN.jsonl"
output_dir = "../generation/final_result.jsonl"


"""
    Sends a POST request to the specified API URL.
"""


def send_request(api_url=api_url, headers=headers, data=""):
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码: {response.json()}")
        time.sleep(10)  # 等待一段时间，避免无限快速重试
        os.execv(__file__, sys.argv)  # 重新执行当前脚本


def read_output_file(output_dir):
    pro_id_list = []

    if os.stat(output_dir).st_size == 0:
        return pro_id_list

    with open(output_dir, 'r', encoding='utf-8-sig') as output_file:
        for line in output_file:
            pro_id_list.append(json.loads(line)['queId'])
    return pro_id_list


def write_output_file(output_dir, output_data):
    with open(output_dir, 'a', encoding='utf-8') as json_file:
        json_file.write(json.dumps(output_data, ensure_ascii=False) + '\n')


def extract_sympy_code(api_response):
    start_tag = "SymPy Code Start"
    end_tag = "SymPy Code End"
    start_index = api_response.find(start_tag) + len(start_tag)
    end_index = api_response.find(end_tag)

    return api_response[start_index:end_index].strip()


def process_calculation_questions(question_problem, question_id):
    instruction_template = (
        "Generate a Python code snippet that uses SymPy to perform a calculation. "
        "Assume that all necessary SymPy functions like 'symbols', 'Eq', and 'solve' "
        "are already imported and available. Do not include any import statements. "
        "Instead of printing results, assign the final result to a variable named 'result'.\n\n"
        "Please write the code so it can be executed directly in a Python environment with SymPy available.\n\n"
        "Please write the code between the tags 'SymPy Code Start' and 'SymPy Code End'.\n\n"
        "For example:"
        "SymPy Code Start\n"
        "# Define the numbers as symbols"
        "x = symbols('x')"
        "# Define the calculation"
        "calculation = x * x"
        "# Substitute x with 66666 and evaluate"
        "result = calculation.subs(x, 66666)"
        "SymPy Code End"
        "After the code, please give me the final answer of this code print, do not let myself to execute the python code"
        "### The calculation problem:\n{problem}\n\n"
        "### Response: Let's use sympy to work out this problem."
    )
    data = {
        "model": 'gpt-4-1106-preview',
        "messages": [
            {
                "role": "user",
                "content": instruction_template.format(
                    problem=question_problem
                )
            }
        ]
    }

    result = send_request(data=data)
    print(result)

    sympy_code = extract_sympy_code(result['choices'][0]['message']['content'])
    # Print the extracted code to check its correctness
    print("Extracted Sympy Code:", sympy_code)

    # ... Modify the sympy_code if necessary ...

    # Define the local variables that the sympy_code will require
    local_vars = {
        "sp": sp,
        "Eq": sp.Eq,
        "solve": sp.solve,
        "symbols": sp.symbols,
        # Provide a placeholder for the result to be stored
        "result": None
    }

    if 'import' in sympy_code:
        raise ValueError("Code should not contain import statements.")

    try:
        # Execute the sympy_code in a safe local environment
        exec(sympy_code, {"__builtins__": None}, local_vars)
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        # Retrieve the result after execution
        # Access the result directly since we know it's been defined
        execution_result = local_vars.get('result', None)
        print(f"The result of the calculation is {result}")

    output_data = {
        "queId": question_id,
        "problem": question_problem,
        "answer": result['choices'][0]['message']['content'],
        # "execution_result": execution_result
    }

    write_output_file(output_dir, output_data)


def main():
    pro_id_list = read_output_file(output_dir)

    with open(input_dir, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            json_data = json.loads(line)
            quesion_problem = json_data['problem']
            question_id = json_data['queId']

            # first judge if it is a calculation problem
            if any(re.search(keyword, quesion_problem, re.IGNORECASE) for keyword in keywords):
                process_calculation_questions(
                    question_problem=quesion_problem, question_id=question_id)

            # if json_data['queId'] == '459d851ac5cd4dcd8da1397633b3b589':
            #     print('执行完了！最后一道题！')
            #     sys.exit(0)

            # if json_data['queId'] in pro_id_list:
            #     continue

            # print(json_data['problem'])
            # pro_id_list.append(json_data['queId'])

            # data = {
            #     "model": 'gpt-4-1106-preview',
            #     "messages": [
            #         {
            #             "role": "user",
            #             "content": "I will give you a math word problem and its knowledge points route, and you should think step by step according to the question problem and its knowledge points route. And if the question problem is too deplicated, you may consider solve by equations. Pay attention to what the denominator of a proportional calculation is, and think step-by-step; you can solve these problems by asking yourself some sub-questions .Then you should give me the final answer. Please think step by step and you should be careful about the particulars. What you should give back to me is the the cleaned final answer (extracted from the models’ original generations) which can directly answer the question.Note that you want to make sure that the final numeric answer or the final phrase answer is at the end of your generated text and separated from the preceding parsed section by ||,if the answer is a fraction, just give me the fraction, not the decimal."
            #         },
            #         {
            #             "role": "user",
            #             "content": "And the question is:"+json_data['problem']+'.And the knowledge points route is:'+str(json_data['knowledge_point_routes'])
            #         }
            #     ]
            # }

            # result = send_request(api_url, headers, data)

            # output_data = {
            #     "queId": json_data['queId'],
            #     "problem": json_data['problem'],
            #     "answer": result['choices'][0]['message']['content']
            # }

            # write_output_file(output_dir, output_data)


if __name__ == "__main__":
    main()
