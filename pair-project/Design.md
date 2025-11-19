# 设计与实现过程说明

## 1. 架构概览

```
arithmetic_generator/
├── cli.py              # 命令行入口
├── config.py           # 生成配置（GeneratorConfig）
├── models.py           # Problem / ExpressionNode
├── generator.py        # ProblemGenerator
├── evaluator.py        # 表达式求值工具
└── grader.py           # 评分逻辑

tests/
└── test_*.py           # unittest 覆盖
```

核心类/函数：

| 模块 | 类/函数 | 说明 |
| --- | --- | --- |
| `config.py` | `GeneratorConfig` | 控制题目数量、范围、操作符等 |
| `models.py` | `Problem` | 封装题目表达式与答案 |
|  | `ExpressionNode` | 构建随机表达式树 |
| `generator.py` | `ProblemGenerator.generate()` | 生成题目，确保唯一性 |
|  | `_build_tree()` | 随机构造操作符数量为 `max_operators` 的树 |
|  | `_evaluate()` | 计算树值，确保减法非负、除法结果真分数 |
|  | `_canonical()` | 输出用于去重的 canonical 字符串 |
| `evaluator.py` | `eval_expression()` | 用于 grader 的表达式求值，支持分数 |
| `grader.py` | `grade()` | 判分，输出 `Grade.txt` |
| `cli.py` | `main()` | 解析参数，选择生成或判分模式 |

## 2. 模块关系

````mermaid
graph TD
    subgraph CLI
        CLI[cli.py main]
    end
    subgraph Core
        CFG[GeneratorConfig]
        GEN[ProblemGenerator]
        EVAL[eval_expression]
        GRADER[grade]
    end
    subgraph Models
        PROB[Problem]
        NODE[ExpressionNode]
    end

    CLI --> CFG
    CLI --> GEN
    CLI --> GRADER
    GEN --> PROB
    GEN --> NODE
    GEN --> CFG
    GRADER --> EVAL
````

## 3. 关键函数流程

### 3.1 `ProblemGenerator.generate()`

````mermaid
flowchart TD
    A[初始化 seen/结果集合] --> B{题目数 < count 且 attempts < limit?}
    B -- 否 --> Z[返回题目列表/若不足抛异常]
    B -- 是 --> C[随机确定 ops_count]
    C --> D[构建表达式树 `_build_tree`]
    D --> E{_evaluate 能得到合法值?}
    E -- 否 --> B
    E -- 是 --> F[计算 canonical 字符串]
    F --> G{已在 seen?}
    G -- 是 --> B
    G -- 否 --> H[格式化表达式/答案，append Problem]
    H --> I[seen.add(canonical)]
    I --> B
````

### 3.2 `grade()`

````mermaid
flowchart TD
    A[读取 Exercises/Answers] --> B{数量相等?}
    B -- 否 --> Z[抛异常]
    B -- 是 --> C[for idx, line in pairs]
    C --> D[normalize 表达式/答案]
    D --> E[expected = eval_expression(expr)]
    E --> F[actual = parse_fraction(answer)]
    F --> G{expected == actual?}
    G -- 是 --> H[记录 idx 到 correct]
    G -- 否 --> I[记录 idx 到 wrong]
    H --> J[继续循环]
    I --> J
    J --> K[写入 Grade.txt，返回结果]
````

## 4. 其他说明

- **单元测试**：`tests/test_generator.py` 验证题目约束、`test_evaluator.py` 验证表达式求值、`test_grader.py` 验证评分输出。
- **流程图可选**：上述流程图展示了核心函数的步骤，若未来加入更复杂的界面/交互流程，可再补充更细的流程图。
