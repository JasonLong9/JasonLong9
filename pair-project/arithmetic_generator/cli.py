from __future__ import annotations

import argparse
from typing import Sequence


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
    parser.parse_args(argv)
    parser.print_help()
    return 0

