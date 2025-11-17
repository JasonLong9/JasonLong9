"""Light-weight code quality checker for key Python modules."""
from __future__ import annotations

from pathlib import Path

MAX_LINE_LENGTH = 110
TARGET_FILES = [
    Path(__file__).with_name("study_planner.py"),
    Path(__file__).with_name("plagiarism_checker.py"),
    Path(__file__).with_name("main.py"),
]


def find_issues(path: Path) -> list[str]:
    issues: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines, start=1):
        if len(line) > MAX_LINE_LENGTH:
            issues.append(f"{path.name}:{lineno} 超过 {MAX_LINE_LENGTH} 字符")
        if line.rstrip() != line:
            issues.append(f"{path.name}:{lineno} 存在尾随空格")
    return issues


def main() -> None:
    all_issues: list[str] = []
    for target in TARGET_FILES:
        if not target.exists():
            raise SystemExit(f"文件 {target} 不存在，无法执行质量检查")
        all_issues.extend(find_issues(target))

    if all_issues:
        raise SystemExit("\n".join(["发现以下质量问题:", *all_issues]))

    print("quality check passed: no style violations detected")


if __name__ == "__main__":
    main()
