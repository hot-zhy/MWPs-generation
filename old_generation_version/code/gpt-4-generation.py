import json
import os
import requests
import time
import sys

api_key = ''
api_url = 'https://api.ohmygpt.com/v1/chat/completions'

input_dir = "../data/TAL-SAQ6K-EN.jsonl"
output_dir = "final_result.jsonl"


pro_id_list = []

while True:
    with open(output_dir, 'r', encoding='utf-8-sig') as output_file:
        data = output_file.readlines()
        for line_number, line in enumerate(data, start=1):
            pro_id_list.append(json.loads(line)['queId'])

    with open(input_dir, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            json_data = json.loads(line)
            if json_data['queId'] == '459d851ac5cd4dcd8da1397633b3b589':
                # 如果执行到最后一道题就退出
                print('执行完了！最后一道题！')
                sys.exit(0)
            print(json_data['problem'])
            if json_data['queId'] in pro_id_list:
                continue
            else:
                pro_id_list.append(json_data['queId'])

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": 'gpt-4',
                "messages": [
                    {
                        "role": "user",
                        "content": "I will give you a math word problem and its knowledge points route, and you should think step by step according to the question problem and its knowledge points route. And if the question problem is too deplicated, you may consider solve by equations. Pay attention to what the denominator of a proportional calculation is, and think step-by-step; you can solve these problems by asking yourself some sub-questions .Then you should give me the final answer. Please think step by step and you should be careful about the particulars. What you should give back to me is the the cleaned final answer (extracted from the models’ original generations) which can directly answer the question.Note that you want to make sure that the final numeric answer or the final phrase answer is at the end of your generated text and separated from the preceding parsed section by ||,if the answer is a fraction, just give me the fraction, not the decimal."
                    },
                    {
                        "role": "user",
                        "content": "And the question is:"+json_data['problem']+'.And the knowledge points route is:'+str(json_data['knowledge_point_routes'])
                    }
                ]
            }

            response = requests.post(
                api_url, data=json.dumps(data), headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                print(result)
            else:
                print(f"请求失败，状态码: {response.json()}")
                print("重新执行脚本...")
                time.sleep(10)  # 等待一段时间，避免无限快速重试
                os.execv(__file__, sys.argv)  # 重新执行当前脚本

            output_data = {
                "queId": json_data['queId'],
                "problem": json_data['problem'],
                "answer": result['choices'][0]['message']['content']
            }

            with open(output_dir, 'a', encoding='utf-8') as json_file:
                json_file.write(json.dumps(
                    output_data, ensure_ascii=False)+'\n')
