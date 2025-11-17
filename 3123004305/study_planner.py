"""Study planner CLI that optimizes a day based on PSP-style planning."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

FOCUS_MULTIPLIER = {"low": 0.8, "medium": 1.0, "high": 1.25}


@dataclass(frozen=True)
class Task:
    """Represents a single unit of work a student may perform."""

    name: str
    category: str
    minutes: int
    value: float
    focus: str = "medium"

    def __post_init__(self) -> None:
        if self.minutes <= 0:
            raise ValueError("Task duration must be positive minutes")
        if self.focus not in FOCUS_MULTIPLIER:
            raise ValueError(f"Focus level {self.focus} is not supported")

    def score(self) -> float:
        """Return weighted contribution for optimization."""

        return self.value * FOCUS_MULTIPLIER[self.focus]


class StudyPlanner:
    """Computes an optimal mix of tasks for the available minutes."""

    def __init__(self, tasks: Sequence[Task]):
        if not tasks:
            raise ValueError("At least one task is required")
        self._tasks = tuple(tasks)

    def optimize(self, available_minutes: int) -> list[Task]:
        if available_minutes <= 0:
            raise ValueError("Minutes must be greater than zero")

        @lru_cache(maxsize=None)
        def best(start: int, remaining: int) -> tuple[float, tuple[int, ...]]:
            if start == len(self._tasks) or remaining <= 0:
                return 0.0, ()

            skip_score, skip_plan = best(start + 1, remaining)
            best_score = skip_score
            best_plan = skip_plan

            task = self._tasks[start]
            if task.minutes <= remaining:
                taken_score, taken_plan = best(start + 1, remaining - task.minutes)
                taken_score += task.score()
                if taken_score > best_score:
                    best_score = taken_score
                    best_plan = (start,) + taken_plan

            return best_score, best_plan

        _, indices = best(0, available_minutes)
        return [self._tasks[i] for i in indices]


def load_tasks(path: Path) -> list[Task]:
    """Load task definitions from a JSON file."""

    raw_text = path.read_text(encoding="utf-8-sig")
    data = json.loads(raw_text)
    return [
        Task(
            name=entry["name"],
            category=entry["category"],
            minutes=int(entry["minutes"]),
            value=float(entry["value"]),
            focus=entry.get("focus", "medium"),
        )
        for entry in data
    ]


def describe_plan(plan: list[Task], available_minutes: int) -> str:
    """Return a friendly textual description of the plan."""

    if not plan:
        return "没有任何任务可以适配给定的时间。"

    total_minutes = sum(task.minutes for task in plan)
    slack = max(available_minutes - total_minutes, 0)
    category_counts = Counter(task.category for task in plan)

    lines = [
        f"计划用时: {total_minutes} 分钟 (剩余 {slack} 分钟)",
        "类别覆盖:",
    ]
    for category, count in category_counts.items():
        category_minutes = sum(task.minutes for task in plan if task.category == category)
        lines.append(f"  - {category}: {count} 项 / {category_minutes} 分钟")

    lines.append("任务清单:")
    for task in plan:
        lines.append(
            f"  · {task.name} ({task.category}) - {task.minutes} 分钟, 价值 {task.value}, 专注 {task.focus}"
        )

    lines.extend([
        "番茄钟建议:",
        *build_focus_blocks(plan),
    ])
    return "\n".join(lines)


def build_focus_blocks(plan: Iterable[Task], block_minutes: int = 25) -> list[str]:
    """Split tasks into focus-friendly blocks."""

    blocks: list[str] = []
    current_block = 1
    for task in plan:
        remaining = task.minutes
        while remaining > 0:
            chunk = min(block_minutes, remaining)
            blocks.append(
                f"    第 {current_block:02d} 块: {task.name} - {chunk} 分钟 ({task.category})"
            )
            remaining -= chunk
            current_block += 1
    return blocks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="为一天的自学/科研安排生成最优任务组合"
    )
    parser.add_argument(
        "--tasks",
        type=Path,
        default=Path(__file__).with_name("sample_tasks.json"),
        help="任务定义 JSON 文件",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=240,
        help="可用于深度工作的分钟数",
    )
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    tasks = load_tasks(args.tasks)
    planner = StudyPlanner(tasks)
    plan = planner.optimize(args.minutes)
    print(describe_plan(plan, args.minutes))


if __name__ == "__main__":
    main()
