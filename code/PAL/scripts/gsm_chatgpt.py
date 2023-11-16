import copy
import json
import argparse
import tqdm
import os

from pal import interface
from pal.prompt import math_prompts

parser = argparse.ArgumentParser()
parser.add_argument('--append', action='store_true')
parser.add_argument('--verbose', action='store_true')
parser.add_argument(
    '--dataset', default='../../../dataset/AAAI/TAL-SAQ6K-EN.jsonls', type=str)
parser.add_argument('--model', default='gpt-3.5-turbo', type=str)
parser.add_argument('--temperature', default=0.0, type=float)
parser.add_argument('--top_p', default=1.0, type=float)
parser.add_argument('--max_tokens', default=512, type=int)
args = parser.parse_args()

DATA_PATH = f'../../../dataset/AAAI/TAL-SAQ6K-EN.jsonl'
OUTPUT_PATH = f'../scripts/eval_results/TAL-SAQ6K-EN-output.jsonl'
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

examples = list(map(json.loads, open(DATA_PATH, encoding='utf-8')))

itf = interface.ProgramChatInterface(
    stop=None,
    get_answer_expr='solution()',
    model=args.model,
    verbose=args.verbose,
    system_message=math_prompts.MATH_CHAT_BETA_SYSTEM_MESSAGE,
)

if args.append:
    lines = open(OUTPUT_PATH).readlines()
    num_skip_exps = len(lines)
else:
    num_skip_exps = 0

with open(OUTPUT_PATH, 'a' if args.append else 'w', encoding='utf-8') as f:
    pbar = tqdm.tqdm(examples[num_skip_exps:],
                     initial=num_skip_exps, total=len(examples))
    for x in pbar:
        question = x['problem']
        result = copy.copy(x)

        try:
            ans = itf.run(
                math_prompts.MATH_CHAT_BETA_PROMPT.format(question=question),
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens
            )
            ans = float(ans)
            print(ans)
        except Exception as e:
            print(e)
            ans = ''

        result['answer'] = ans
        result['generation'] = itf.history
        f.write(json.dumps(result, ensure_ascii=False) + '\n')

        itf.clear_history()
        f.flush()
