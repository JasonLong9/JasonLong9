# 代码说明（关键模块与思路）

本文摘录项目中最核心的代码片段，并结合注释解释设计思路。所有示例均来自 `pair-project/arithmetic_generator` 模块。

---

## 1. 题目生成器：`ProblemGenerator`

```python
class ProblemGenerator:
    def __init__(self, config: GeneratorConfig) -> None:
        self.config = config
        self._rng = random.Random(config.seed)
        self._attempt_limit = max(config.max_attempts, config.count * 20)

    def generate(self) -> List[Problem]:
        problems: List[Problem] = []
        seen: Set[str] = set()
        attempts = 0
        while len(problems) < self.config.count and attempts < self._attempt_limit:
            attempts += 1
            ops_count = self._rng.randint(1, self.config.max_operators)
            node = self._build_tree(ops_count)
            value = self._evaluate(node)
            if value is None:
                continue

            canonical = self._canonical(node)
            if canonical in seen:
                continue

            problems.append(Problem(expression=self._format_expression(node),
                                    answer=format_fraction(value)))
            seen.add(canonical)

        if len(problems) < self.config.count:
            raise RuntimeError("Unable to generate enough unique problems; increase range or decrease count.")
        return problems
```

- `_attempt_limit` 确保在数值范围有限时不会陷入无休止重试。
- `seen` 利用 canonical 字符串去重，避免交换律导致的重复题目。
- `_build_tree`/`_evaluate` 负责生成表达式树并进行合法性校验（无负数、真分数、除数非零）。

---

## 2. 表达式树的构建与计算

```python
def _build_tree(self, ops_remaining: int) -> ExpressionNode:
    if ops_remaining == 0:
        return ExpressionNode(value=self._random_operand())

    op = self._rng.choice(("+", "-", "*", "/"))
    left_ops = self._rng.randint(0, ops_remaining - 1)
    right_ops = ops_remaining - 1 - left_ops
    left = self._build_tree(left_ops)
    right = self._build_tree(right_ops)
    return ExpressionNode(op=op, left=left, right=right)

def _evaluate(self, node: ExpressionNode) -> Fraction | None:
    if node.is_leaf():
        return node.value
    left_val = self._evaluate(node.left)
    right_val = self._evaluate(node.right)
    ...
    if node.op == "-":
        if left_val < right_val:
            return None  # 保证不出现负数
        value = left_val - right_val
    elif node.op == "/":
        if right_val == 0 or left_val <= 0 or right_val <= left_val:
            return None
        value = left_val / right_val
        if value >= 1:
            return None  # 确保真分数
```

- 构造树时随机决定每一个分支的操作符个数，从而保证最多 `max_operators`（≤3）个运算符。
- `_evaluate` 在递归求值的同时执行约束检查；返回 `None` 表示本次树不合法，上一层会触发重试。

---

## 3. canonical 表示与格式化

```python
def _canonical(self, node: ExpressionNode) -> str:
    if node.is_leaf():
        return f"{node.value.numerator}/{node.value.denominator}"
    left = self._canonical(node.left)
    right = self._canonical(node.right)
    if node.op in {"+", "*"} and left > right:
        left, right = right, left  # 交换律去重
    return f"{node.op}[{left}][{right}]"

def _format_expression(self, node: ExpressionNode) -> str:
    if node.is_leaf():
        return format_fraction(node.value)
    return f"({self._format_expression(node.left)} {node.op} {self._format_expression(node.right)})"
```

- canonical 字符串是去重的关键：对于加法/乘法，左右子树排序后再拼接，保证 `3+5` 与 `5+3` 的 canonical 相同。
- `_format_expression` 用括号确保操作顺序；终端 CLI 会直接输出该格式生成 `Exercises.txt`。

---

## 4. 评分模块：`grade`

```python
def grade(exercises_file: str, answers_file: str, output_file: str = "Grade.txt") -> GradeResult:
    exercises = [...]
    answers = [...]
    if len(exercises) != len(answers):
        raise ValueError("题目数量与答案数量不一致")

    correct: List[int] = []
    wrong: List[int] = []

    for idx, (expr_line, answer_line) in enumerate(zip(exercises, answers), start=1):
        expression = _normalize_exercise(expr_line)
        expected = eval_expression(expression)
        answer_text = _normalize_answer(answer_line)
        actual = parse_fraction(answer_text) if answer_text else None
        match = actual is not None and expected == actual
        (correct if match else wrong).append(idx)

    Path(output_file).write_text("\n".join([
        _format_grade_line("Correct", correct),
        _format_grade_line("Wrong", wrong),
    ]), encoding="utf-8")
    return GradeResult(correct=correct, wrong=wrong)
```

- `_normalize_exercise/_normalize_answer` 会去掉序号、等号等多余字符，使得输入格式灵活。
- `eval_expression` 通过中缀转后缀 + `Fraction` 计算准确结果，避免浮点误差。
- 输出 `Grade.txt` 使用“数量 + 题号列表”的格式，满足题目需求。

---

## 5. 命令行入口：`cli.py`

```python
def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.exercises or args.answers:
        if not args.exercises or not args.answers:
            parser.error("grading mode requires both -e and -a")
        result = grade(args.exercises, args.answers)
        print(
            f"Grading finished: correct {len(result.correct)}, wrong {len(result.wrong)}, output -> Grade.txt"
        )
    else:
        if args.range_limit is None:
            parser.error("missing -r/--range. Use --help for details.")
        config = GeneratorConfig(count=args.count or 20, range_limit=args.range_limit)
        problems = ProblemGenerator(config).generate()
        _write_lines(Path("Exercises.txt"), [f"{p.expression} =" for p in problems])
        _write_lines(Path("Answers.txt"), [p.answer for p in problems])
        print(f"Generated {len(problems)} exercises -> Exercises.txt / Answers.txt")
```

- CLI 支持生成和判分两种模式，并对缺失参数进行提醒。
- 自动写入 `Exercises.txt` / `Answers.txt`，终端提示方便快速验证。

---

## 6. 单元测试概览

- `tests/test_generator.py`：验证题量、唯一性、符号数量上限、真分数约束等，确保生成逻辑稳定。
- `tests/test_evaluator.py`：验证分数解析与表达式求值正确性。
- `tests/test_grader.py`：构造小型题库和答案，核对 `Grade.txt` 的输出格式。

通过上述模块与测试，整体程序既能满足功能需求，也能方便地做回归验证。
