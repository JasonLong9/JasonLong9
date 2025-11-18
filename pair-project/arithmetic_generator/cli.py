from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .config import GeneratorConfig
from .generator import ProblemGenerator


def _write_lines(path: Path, lines: Sequence[str]) -> None:
    path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m arithmetic_generator",
        description="Generate primary-school arithmetic problems or grade answers.",
    )
    parser.add_argument("-n", "--count", type=int, help="Number of exercises to generate.")
    parser.add_argument(
        "-r",
        "--range",
        dest="range_limit",
        type=int,
        help="Upper bound (exclusive) for numbers and denominators.",
    )
    parser.add_argument("-e", "--exercises", help="Exercises file for grading.")
    parser.add_argument("-a", "--answers", help="Answers file for grading.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.range_limit is None:
        parser.error("缺少 -r/--range 参数。使用 --help 查看说明。")
    if args.exercises or args.answers:
        parser.error("判分功能将在下一次提交提供，请仅使用生成模式。")

    count = args.count or 20
    config = GeneratorConfig(count=count, range_limit=args.range_limit)
    generator = ProblemGenerator(config)
    problems = generator.generate()

    exercises_path = Path("Exercises.txt")
    answers_path = Path("Answers.txt")
    _write_lines(exercises_path, [f"{p.expression} =" for p in problems])
    _write_lines(answers_path, [p.answer for p in problems])
    print(f"已生成 {len(problems)} 道题目：{exercises_path} / {answers_path}")

    return 0
