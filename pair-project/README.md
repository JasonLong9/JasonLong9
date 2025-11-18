# 小学四则运算题目生成器

本项目实现一个用于自动生成小学四则运算练习以及批改答案的命令行程序。核心需求：

- 支持自然数与真分数，运算符 `+ - * /` 以及括号。
- `-r` 控制数值范围（必填），`-n` 控制题目数量，`-e/-a` 用于判分。
- 输出 `Exercises.txt`、`Answers.txt` 和 `Grade.txt`，保证题目唯一性且一次可生成 1 万道题。

> 当前已支持题目生成，判分（-e/-a）功能将在后续提交补齐。

## 目录结构

```
pair-project/
├── arithmetic_generator/   # Python 包（业务逻辑与 CLI）
├── tests/                  # 单元测试
└── README.md               # 使用说明
```

## 环境要求

- Python 3.11+
- 仅依赖标准库，无需额外安装

## 生成题目

```bash
cd pair-project
python -m arithmetic_generator -r 10 -n 20
# 将在当前目录生成 Exercises.txt 与 Answers.txt
```

## 判分模式

```bash
python -m arithmetic_generator -e Exercises.txt -a Answers.txt
# 在当前目录输出 Grade.txt
```

当前输入文件假设符合题目格式，程序会统计对错题号：

```
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```

## 开发规范

1. 功能以小步提交方式推进，提交信息包含功能点与范围。
2. 关键逻辑将配套单元测试，确保题目生成/判分可回归。
3. README 将持续更新以反映运行命令、参数示例等。

请等待下一次提交以获得完整功能实现。
