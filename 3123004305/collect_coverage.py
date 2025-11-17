"""Collect coverage data via trace module and output summary."""
from __future__ import annotations

from pathlib import Path
from trace import Trace

import run_tests

TARGETS = [
    Path(__file__).with_name("plagiarism_checker.py"),
    Path(__file__).with_name("tests") / "test_plagiarism_checker.py",
]


def count_non_empty_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> None:
    tracer = Trace(count=True, trace=False)
    tracer.runfunc(run_tests.main)
    results = tracer.results()

    summary_lines = ["Coverage summary via trace module"]
    counts = results.counts
    for target in TARGETS:
        resolved = str(target.resolve())
        executed = {
            lineno
            for (filename, lineno), hit in counts.items()
            if filename == resolved and hit
        }
        total = count_non_empty_lines(target)
        coverage = 100.0 if total == 0 else len(executed) / total * 100
        summary_lines.append(
            f"{target}: {len(executed)}/{total} 非空行 => {coverage:.1f}% coverage"
        )

    Path("coverage_summary.txt").write_text("\n".join(summary_lines), encoding="utf-8")
    print("Coverage summary written to coverage_summary.txt")


if __name__ == "__main__":
    main()
