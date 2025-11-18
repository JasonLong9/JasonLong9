# 小学四则运算题目生成器

实现命令行程序，既能批量生成符合小学要求的四则运算题，也能给定题目/答案文件输出对错统计结果。

## 功能概览

- `-n` 题目数量（默认 20，最多 10000），`-r` 数值范围上限（必填，取 [0, r)）。
- 支持自然数与真分数，自动添加括号，保证中间结果不为负、除法结果真分数且题目唯一。
- 自动写入 `Exercises.txt` 与 `Answers.txt`，并可通过 `-e/-a` 判题生成 `Grade.txt`。
- 单元测试覆盖表达式求值、题目生成约束及判题流程。

## 使用方法

```bash
cd pair-project
# 生成 30 道 20 以内的题目
python -m arithmetic_generator -r 20 -n 30
# 判题
python -m arithmetic_generator -e Exercises.txt -a Answers.txt
```

输出示例：

```
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```

## 目录结构

```
pair-project/
├── arithmetic_generator/
│   ├── cli.py           # 参数解析、生成/判题入口
│   ├── config.py        # 生成配置
│   ├── evaluator.py     # 表达式解析与求值
│   ├── generator.py     # 题目生成、去重与约束控制
│   └── grader.py        # 判分逻辑
├── tests/               # unittest 覆盖关键逻辑
└── README.md
```

## 测试

在 `pair-project` 目录执行：

```bash
python -m unittest
```

测试会跳转至临时目录校验题目生成、表达式求值与判题结果，无需额外依赖。

