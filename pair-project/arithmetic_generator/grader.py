from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import List

from .evaluator import eval_expression, parse_fraction


@dataclass
class GradeResult:
    correct: List[int]
    wrong: List[int]


def _normalize_exercise(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return stripped
    if ". " in stripped:
        prefix, rest = stripped.split(". ", 1)
        if prefix.isdigit():
            stripped = rest.strip()
    if stripped.endswith("="):
        stripped = stripped[:-1].strip()
    return stripped


def _normalize_answer(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return stripped
    if ". " in stripped:
        prefix, rest = stripped.split(". ", 1)
        if prefix.isdigit():
            stripped = rest.strip()
    if "=" in stripped:
        stripped = stripped.split("=")[-1].strip()
    return stripped


def grade(exercises_file: str, answers_file: str, output_file: str = "Grade.txt") -> GradeResult:
    exercises_path = Path(exercises_file)
    answers_path = Path(answers_file)
    exercises = [line for line in exercises_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    answers = [line for line in answers_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(exercises) != len(answers):
        raise ValueError("题目数量与答案数量不一致")

    correct: List[int] = []
    wrong: List[int] = []
    comparison_lines: List[str] = []

    for idx, (expr_line, answer_line) in enumerate(zip(exercises, answers), start=1):
        expression = _normalize_exercise(expr_line)
        if not expression:
            raise ValueError(f"题目第 {idx} 行为空")

        expected = eval_expression(expression)
        answer_text = _normalize_answer(answer_line)
        try:
            actual = parse_fraction(answer_text)
        except Exception:  # noqa: BLE001
            actual = None
        match = actual is not None and expected == actual
        (correct if match else wrong).append(idx)

    grade_lines = [
        _format_grade_line("Correct", correct),
        _format_grade_line("Wrong", wrong),
    ]
    Path(output_file).write_text("\n".join(grade_lines), encoding="utf-8")
    return GradeResult(correct=correct, wrong=wrong)


def _format_grade_line(label: str, indices: List[int]) -> str:
    if indices:
        numbers = ", ".join(str(i) for i in indices)
    else:
        numbers = ""
    return f"{label}: {len(indices)} ({numbers})"
