# 模块接口设计与实现说明（论文查重）

## 1. 代码组织概览
- **入口模块 `main.py`**：
  - 负责解析命令行参数（原文、抄袭版、输出答案路径，以及可选 `--window`）。
  - 将参数传递给 `plagiarism_checker.main(argv)`，保持入口极简，便于课堂测试统一运行方式。
- **核心模块 `plagiarism_checker.py`**：
  - 包含一个自定义异常 `PlagiarismError`，用于描述文件读写异常情况。
  - 函数划分：
    1. `tokenize(text: str)`：分词与规范化。
    2. `build_shingles(words, window)`：构建词级 n-gram 集合。
    3. `jaccard_similarity(a, b)`：计算 shingle 集合的 Jaccard 相似度。
    4. `compute_similarity(original, suspect, window)`：整合上述函数，得到相似度分数。
    5. `similarity_from_files(original_path, suspect_path, window)`：从文件读取并计算分数。
    6. `format_percentage(score)`：将分数格式化为两位小数的百分比字符串。
    7. `main(argv)`：命令行接口，解析参数、调用 `similarity_from_files`、输出答案。
  - 函数之间通过清晰的接口传递（字符串、词列表、shingle 集合、浮点分数），没有隐藏状态，便于单元测试。
- **测试与工具模块**：
  - `tests/test_plagiarism_checker.py`：11 个单元测试，覆盖各核心函数及 CLI 边界情况。
  - `run_tests.py` / `collect_coverage.py`：分别用于快速运行测试与生成 coverage 摘要。
  - `quality_gate.py`：统一检查关键 Python 文件的行长与尾随空格，保证代码风格。

## 2. 函数关系与流程（文字流程图）
```
main.py → plagiarism_checker.main(argv)
            ├─ parse_args → 获取 original/suspect/output/--window
            ├─ similarity_from_files
            │    ├─ Path.read_text() ×2 → 原文 / 抄袭文串
            │    ├─ compute_similarity
            │    │    ├─ tokenize(original)
            │    │    ├─ tokenize(suspect)
            │    │    ├─ build_shingles(words_a, window)
            │    │    ├─ build_shingles(words_b, window)
            │    │    └─ jaccard_similarity(shingles_a, shingles_b)
            │    └─ 返回分数（0~1）
            ├─ format_percentage(score)
            ├─ 写入 output 文件（UTF-8，两位小数）
            └─ print(result)
```

## 3. 关键算法与独到之处
- **词级 shingle + Jaccard**：
  - 将文本转为小写词序列，再用窗口大小生成 n-gram（shingle）集合。
  - 通过 shingle 集合的 Jaccard 相似度衡量“语句结构 + 单词排列”的相似度，兼容增删改的抄袭情形。
  - 时间复杂度 O(n)、空间复杂度 O(n)（n 为词数），适合课堂评测的 5 秒/内存限制。
- **可调窗口**：
  - `--window` 参数允许根据测试需求调整关注粒度（窗口越大越强调长语句一致性）。
  - 默认为 3，兼顾精度与性能；如果测试文本特别长，可调高窗口减小集合规模。
- **健壮的 IO 处理**：
  - 使用 `utf-8-sig` 读取，兼容带 BOM 的文件。
  - 写入失败（路径不存在、权限不足）会抛 `PlagiarismError`，易于测试与排查。
- **模块化结构**：
  - 各函数职责单一，且无隐式状态，方便单元测试覆盖到每个环节（分词、shingle、相似度、文件 IO、CLI）。
  - CLI 入口与核心逻辑解耦，便于其他脚本或库直接调用 `compute_similarity` 等函数。
- **扩展性**：
  - 可以在 `tokenize` 中扩展自定义分词（如中文分词库），或在 `build_shingles` 中加入停用词过滤。
  - 也能替换 `jaccard_similarity` 为 MinHash/SimHash 等更大规模场景的算法。

## 4. 实现细节
- `tokenize`：使用正则 `[\w']+` 萃取英文/数字/中文字符；所有单词 lower()，减少大小写影响。
- `build_shingles`：当词数小于窗口时，返回一个包含完整词序列的 tuple，避免空集导致相似度为 0。
- `jaccard_similarity`：处理空集（两边均空返回 1.0，避免 0/0）以及集合交并运算。
- `format_percentage`：对分数进行 `min/max` 裁剪，保证输出在 0~100% 内，再格式化为两位小数字符串。
- `main(argv)`：命令行参数顺序固定 `[原文] [抄袭] [答案] (--window N)`，与课堂测试脚本保持一致。

## 5. 非功能支持
- `quality_gate.py` 保证核心文件遵循行长 ≤110、无尾随空格的规范。
- `collect_coverage.py` 利用 `trace` 模块生成 coverage 概要，定位未覆盖分支。
- `profiling_report.md` 记录使用 Visual Studio Studio Profiling Tools / `cProfile` 定位 `build_shingles` 和 `best` 函数的性能瓶颈，并给出优化建议（如增加缓存、转迭代 DP 等）。

## 6. 提交与验证
- Git 按功能阶段提交：
  - `feat: add core plagiarism checker implementation`
  - `test: add unit tests and tooling`
  - `chore: remove generated artifacts`
  - `chore: remove placeholder file`
  - `docs: refine PSP table`
  - `docs: add module design overview`
- 质量与测试：
  - `python quality_gate.py` → 无警告
  - `python -m unittest discover -s tests -p "test_*.py" -v` → 11/11 通过
  - `python collect_coverage.py` → `coverage_summary.txt`（核心模块 82.4% 非空行覆盖）

以上内容可直接用于博客中“计算模块接口设计与实现”部分。
