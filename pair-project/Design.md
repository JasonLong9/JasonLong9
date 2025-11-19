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
| `config.py` | `GeneratorConfig` | 控制题目数量、数值范围、操作符集合等 |
| `models.py` | `Problem` | 封装题目表达式与答案 |
|  | `ExpressionNode` | 生成器构建的表达式树节点 |
| `generator.py` | `ProblemGenerator.generate()` | 生成题目、保证唯一性 |
|  | `_build_tree()` | 随机决定操作符个数并生成表达式树 |
|  | `_evaluate()` | 计算树的值，确保非负或真分数等约束 |
|  | `_canonical()` | 用于去重的 canonical 表示 |
| `evaluator.py` | `eval_expression()` | 评分时对题目进行求值 |
| `grader.py` | `grade()` | 读取题目/答案文件并统计正确率 |
| `cli.py` | `main()` | 解析命令行，协调生成与评分 |

## 2. 模块关系（文字描述）

- **CLI 层（cli.py）**：解析命令行参数，构建 `GeneratorConfig`，根据参数决定调用 `ProblemGenerator` 还是 `grade()`。
- **生成器**：`ProblemGenerator` 使用 `GeneratorConfig` 控制生成策略；内部依赖 `ExpressionNode` 构建随机表达式树，最终产出 `Problem`。
- **评分器**：`grade()` 读取题目/答案文件，借助 `eval_expression()` 计算标准答案并比较。
- **模型**：`Problem`、`ExpressionNode` 由生成器产生，在评分环节仅需 `Problem` 的序列化形式。
- **测试层**：`tests/test_*.py` 导入上述模块，验证约束与边界条件。

## 3. 关键函数流程（文字描述）

### 3.1 `ProblemGenerator.generate()`

1. 初始化结果列表与 `seen` 集合，设置尝试次数上限。
2. 在“题目数量小于 `count` 且尝试次数未达上限”时循环：
   - 随机确定操作符数量 `ops_count`；
   - 调用 `_build_tree()` 构建表达式树；
   - `_evaluate()` 计算树值，若出现负数、除零或非真分数则放弃本次迭代；
   - 生成 canonical 字符串，若已存在于 `seen`，则继续下一次迭代；
   - 将格式化后的表达式与答案存入结果，并把 canonical 加入 `seen`。
3. 若生成数量已满足 `count`，返回结果；若尝试上限耗尽仍不足，则抛出异常提醒用户调整参数。

### 3.2 `grade()`

1. 读取题目/答案文件，去掉空行，对比题目数量，数量不一致直接报错。
2. 对每行题目：
   - 规范化表达式（去序号、去等号），并调用 `eval_expression()` 计算标准答案；
   - 解析输入答案，转换为分数后与标准答案比较；
   - 根据结果将题号写入 `correct` 或 `wrong` 列表。
3. 写入 `Grade.txt`（`Correct: N (...)` 和 `Wrong: M (...)`），同时返回 `GradeResult` 供 CLI 输出统计信息。

## 4. 其他说明

- **测试**：`tests/test_generator.py`、`test_evaluator.py`、`test_grader.py` 分别校验生成、求值、评分逻辑。
- **流程补充**：由于核心流程较为直观，此处使用文字描述；若后续拓展更复杂的 UI/交互，可再补充图形化流程图。
