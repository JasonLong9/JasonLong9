# 3123004305 项目说明

## 仓库结构
- `study_planner.py` / `sample_tasks.json`：上一阶段 PSP 学习计划 CLI。
- `plagiarism_checker.py`：论文查重核心实现。
- `main.py`：命令行入口，按课堂要求从参数读取原文/抄袭/输出路径。
- `tests/`：查重模块的 11 个单元测试。
- `run_tests.py`：配合 `trace` 的测试入口。
- `collect_coverage.py`：使用标准库 `trace` 收集覆盖率并生成 `coverage_summary.txt`。
- `quality_gate.py`：轻量代码质量检查脚本（行长、尾随空格）。
- `PSP.md`、`profiling_report.md`：时间记录与性能分析。
- `requirements.txt`：说明仅依赖标准库。

## 论文查重 CLI 使用
```bash
cd 3123004305
python main.py C:\tests\orig.txt C:\tests\orig_add.txt C:\tests\ans.txt
```
- 各命令行参数之间用空格分隔，路径中不要出现空格（与课堂测试机一致）。
- 可追加 `--window 3` 等参数调整 shingle 窗口大小（默认 3）。
- 课堂样例中，`orig.txt` 是原文，`orig_add.txt`、`orig_del.txt`、`orig_mix.txt` 等为抄袭版本，分别传入第二个参数即可。
- 程序会将重复率（百分比、保留两位小数）写入第三个参数指定的答案文件，并在终端回显。

## 单元测试与覆盖率
1. 运行全部 11 个单元测试：
   ```bash
   python -m unittest discover -s tests -p "test_*.py" -v
   ```
2. 无法安装 `pytest` / `coverage` 时，使用 `collect_coverage.py` 调用 `trace`：
   ```bash
   python collect_coverage.py
   ```
   输出写入 `coverage_summary.txt`（当前 `plagiarism_checker.py` 覆盖 82.4% 非空行，`tests/test_plagiarism_checker.py` 覆盖 95.6%）。
3. 若网络允许，可按常规方式安装更完整的测试/覆盖工具。

## 代码质量
- 执行 `python quality_gate.py` 检查 `study_planner.py`、`plagiarism_checker.py`、`main.py` 的行长/尾随空格。
- 若需要更严格的 Code Quality Analysis，可在网络可用时安装 `ruff`、`pylint` 等。

## Git 提交流程（需手动执行）
1. `git add 3123004305/*`
2. `git commit -m "Add plagiarism checker with tests"`
3. `git push origin main`
助教会检查提交历史，请保持“有进展即提交”。

## 其他文件
- `profiling_report.md`：记录使用 `cProfile`（或 Visual Studio Studio Profiling Tools）分析 knapsack 动态规划热区的过程。
- `PSP.md`：编码前后的时间估算与实际耗时。
- `requirements.txt`：说明运行仅需 Python 3 标准库。
