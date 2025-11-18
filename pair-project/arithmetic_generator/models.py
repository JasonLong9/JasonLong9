from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass
class Problem:
    expression: str
    answer: str


@dataclass
class ExpressionNode:
    value: Fraction | None = None
    op: str | None = None
    left: "ExpressionNode | None" = None
    right: "ExpressionNode | None" = None

    def is_leaf(self) -> bool:
        return self.op is None
