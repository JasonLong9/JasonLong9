# 模块接口设计与实现说明（论文查重）

## 1. 总体设计
- **入口**：`main.py` 负责解析命令行参数（原文绝对路径、抄袭版绝对路径、输出答案绝对路径、可选 `--window`）。
- **核心模块**：`plagiarism_checker.py` 封装查重逻辑，公开函数：
  - `tokenize(text: str) -> list[str]`：分词，统一小写，保留字母/数字/单引号。
  - `build_shingles(words: Sequence[str], window: int) -> Set[Tuple[str, ...]]`：生成词级 shingle 集合，窗口大小默认 3。
  - `jaccard_similarity(a, b) -> float`：计算两个 shingle 集合的 Jaccard 相似度。
  - `compute_similarity(original: str, suspect: str, window: int) -> float`：从原始字符串计算相似度。
  - `similarity_from_files(original_path: Path, suspect_path: Path, window: int) -> float`：从文件读取并计算相似度（UTF-8/BOM）。
  - `format_percentage(score: float) -> str`：格式化为保留两位小数的百分比。
  - `main(argv: Sequence[str] | None)`：CLI 入口，读文件、算相似度、写答案文件并打印。
- **异常**：定义 `PlagiarismError` 用于文件读写错误（无法读取/写入指定路径），便于测试和提示。

## 2. 数据流与流程
1. `main.py` 调用 `plagiarism_checker.main(argv)`。
2. `parse_args` 解析 `original/suspect/output` 路径和 `--window`（默认 3）。
3. `similarity_from_files` 读取两份论文文本，向下调用 `compute_similarity`。
4. `compute_similarity`：
   - `tokenize` -> 词列表
   - `build_shingles` -> shingle 集合
   - `jaccard_similarity` -> 相似度分数（0~1）
5. `format_percentage` -> 百分比字符串（两位小数），写入输出文件，打印结果。

## 3. 关键设计与独到之处
- **简洁可控的复杂度**：词级 shingle + Jaccard，时间/空间约 O(n)，适合课堂评测的规模与 5 秒/内存限制要求。
- **健壮的 IO 处理**：读取使用 `utf-8-sig` 兼容 BOM；写入包裹异常统一抛 `PlagiarismError`，便于定位文件权限/路径错误。
- **可扩展参数**：`--window` 可调，兼容课堂样例（orig.txt / orig_add.txt 等）。
- **可测试性**：模块化函数、无全局状态，便于 `unittest` 独立测试各阶段（分词、shingle、Jaccard、文件 IO、CLI）。

## 4. 流程图（文字描述）
- Start -> 解析参数 -> 读取原文/抄袭文 -> 分词 -> 生成 shingle -> 计算 Jaccard -> 格式化百分比 -> 写答案文件 -> 打印 -> End。

## 5. 与代码位置的映射
- 入口：`main.py:1-9`
- 参数解析与 CLI：`plagiarism_checker.py:78-108`
- 核心函数：`tokenize`(行 17)、`build_shingles`(23)、`jaccard_similarity`(36)、`compute_similarity`(49)、`similarity_from_files`(60)、`format_percentage`(71)
- 异常定义：`PlagiarismError`(13)

## 6. 提交与验证
- 已通过多个阶段的 Git 提交并推送到 `main`。
- 质量检查：`python quality_gate.py` 无警告。
- 单元测试：`python -m unittest discover -s tests -p "test_*.py" -v` 全部通过；覆盖率见 `collect_coverage.py` 生成的 `coverage_summary.txt`。
