# 使用LLMs API自动求解数学文本题目

## 目录结构

1. /code存放现有代码，可以分成PAL和COT两个目录
2. /dataset存放数据集
3. /generation存放代码生成的结果，可以分成PAL和COT两个目录
4. /old_generation_version是之前的生成一遍全部答案的代码和结果，主体生成答案的文件是gpt-4-generation.py，别的是提取答案的文件
5. /old_generation_version/submission存放之前生成的一遍的答案，其中final_result.jsonl是直接生成的,TAL_SAQ6K_EN_prediction.json是提取完交到网站的
6. /submission存放我们要提交到网站的答案

## 可以改进的地方

- 先前的调用GPT的代码/old_generation_version/code/gpt-4-generation.py，代码质量太差了，prompt写的不好，导致生成答案太繁琐，费钱；我们需要考虑精简，有时候加入一句"Please response briefly"就可以省去很多费用（token）
- 考虑如何设计prompt来让生成的答案方便提取最终答案