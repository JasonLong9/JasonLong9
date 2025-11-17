"""Plagiarism detection via word shingling and Jaccard similarity."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence, Set, Tuple

DEFAULT_WINDOW = 3
_WORD_RE = re.compile(r"[\w']+", re.UNICODE)


class PlagiarismError(Exception):
    """Custom exception for plagiarism checker errors."""


def tokenize(text: str) -> list[str]:
    """Lowercase and split text into words, keeping alphanumerics and apostrophes."""

    return [match.group(0).lower() for match in _WORD_RE.finditer(text)]


def build_shingles(words: Sequence[str], window: int = DEFAULT_WINDOW) -> Set[Tuple[str, ...]]:
    """Return a set of n-gram shingles from the words list."""

    if window <= 0:
        raise ValueError("Window size must be positive")
    if not words:
        return set()
    if len(words) < window:
        return {tuple(words)}

    return {tuple(words[i : i + window]) for i in range(len(words) - window + 1)}


def jaccard_similarity(a: Iterable[Tuple[str, ...]], b: Iterable[Tuple[str, ...]]) -> float:
    """Compute Jaccard similarity between two shingle collections."""

    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


def compute_similarity(original: str, suspect: str, window: int = DEFAULT_WINDOW) -> float:
    """Compute similarity score (0~1) between two texts."""

    words_a = tokenize(original)
    words_b = tokenize(suspect)
    shingles_a = build_shingles(words_a, window)
    shingles_b = build_shingles(words_b, window)
    return jaccard_similarity(shingles_a, shingles_b)


def similarity_from_files(original_path: Path, suspect_path: Path, window: int = DEFAULT_WINDOW) -> float:
    """Load two files and compute their similarity."""

    try:
        original_text = original_path.read_text(encoding="utf-8-sig")
        suspect_text = suspect_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise PlagiarismError(f"无法读取文件: {exc}") from exc

    return compute_similarity(original_text, suspect_text, window)


def format_percentage(score: float) -> str:
    """Format similarity as percentage string with two decimals."""

    percentage = min(max(score, 0.0), 1.0) * 100
    return f"{percentage:.2f}%"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="论文查重：基于词语 shingles 的重复率计算")
    parser.add_argument("original", type=Path, help="原文文件的绝对路径")
    parser.add_argument("suspect", type=Path, help="抄袭版论文文件的绝对路径")
    parser.add_argument("output", type=Path, help="输出答案文件的绝对路径")
    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_WINDOW,
        help="shingle 窗口大小（默认 3）",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    similarity = similarity_from_files(args.original, args.suspect, args.window)
    result = format_percentage(similarity)
    try:
        args.output.write_text(result, encoding="utf-8")
    except OSError as exc:
        raise PlagiarismError(f"无法写入输出文件: {exc}") from exc
    print(result)


if __name__ == "__main__":
    main()
