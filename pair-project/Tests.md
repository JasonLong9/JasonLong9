# 测试运行记录

本文件列出最近一次在 `pair-project` 目录下执行的测试，覆盖单元测试与手工 CLI 验证共 10 项，帮助说明程序的正确性。

## 1. 自动化单元测试（6 项）

| 编号 | 命令/案例 | 覆盖点 | 结果 |
| --- | --- | --- | --- |
| UT-1 | `python -m unittest tests.test_generator.GeneratorTests.test_generate_basics` | 生成 20 道题目，校验唯一性、符号数量、数值范围 | ✅ 通过 |
| UT-2 | `python -m unittest tests.test_generator.GeneratorTests.test_division_results_proper_fraction` | 随机题目中若含除法，答案需为真分数 | ✅ 通过 |
| UT-3 | `python -m unittest tests.test_evaluator.EvaluatorTests.test_eval_expression` | 复杂括号+分数表达式求值 | ✅ 通过 |
| UT-4 | `python -m unittest tests.test_evaluator.EvaluatorTests.test_format_and_parse_fraction` | 分数格式化/解析互逆 | ✅ 通过 |
| UT-5 | `python -m unittest tests.test_grader.GraderTests.test_grade_outputs` | 判分流程：两对题目正确一题错误，输出统计 | ✅ 通过 |
| UT-6 | `python -m unittest` | 运行全量测试，确保模块间无耦合问题 | ✅ 通过 |

## 2. CLI 功能测试（4 组，每组含多例）

| 编号 | 命令 | 说明 | 结果 |
| --- | --- | --- | --- |
| CL-1 | `python -m arithmetic_generator -r 10 -n 5` | 生成 5 道 10 以内题目；确认 `Exercises/Answers` 文件创建且无重复 | ✅ 通过 |
| CL-2 | `python -m arithmetic_generator -r 50 -n 200` | 压力测试，验证 200 道题（含分数）生成时间与唯一性 | ✅ 通过 |
| CL-3 | `python -m arithmetic_generator -e Exercises.txt -a Answers.txt` | 使用真实生成的文件判分，`Grade.txt` 显示全部正确 | ✅ 通过 |
| CL-4 | `python -m arithmetic_generator -e custom_ex.txt -a custom_ans.txt`（其中 2 题错误） | 验证错误题号出现在 Wrong 列表 | ✅ 通过 |

> 注：CL-3/CL-4 共覆盖 5+200+若干手工题目，确保判分与生成链路闭环。

## 3. 程序正确性的理由

1. **全流程覆盖**：单元测试验证了题目生成、表达式求值、判分三大核心模块；CLI 测试又确保文件输入输出链路正确。
2. **边界条件验证**：UT-1/UT-2 针对符号数量、真分数、数值范围做了严格断言；CL-2 的 200 题压力测试覆盖了随机边界。
3. **结果可复现**：所有自动化测试使用种子或固定输入，`python -m unittest` 可随时重跑；CLI 命令已在 README 中记录，任何人都能复现。
4. **错误检测机制**：在生成过程中若出现负数/非真分数会立即丢弃；评分时若题数不匹配或表达式非法会抛出异常。
5. **人工抽查**：对 `Exercises.txt` 与 `Answers.txt` 手工抽样核算，确认格式和答案匹配。

因此，我们可以有信心认为当前实现满足题目要求；若未来扩展更多功能，可在现有测试基础上继续补充新用例。
