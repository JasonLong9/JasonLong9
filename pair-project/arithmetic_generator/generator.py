from __future__ import annotations

from fractions import Fraction
import random
from typing import List, Set

from .config import GeneratorConfig
from .evaluator import format_fraction
from .models import ExpressionNode, Problem

COMMUTATIVE = {"+", "*"}


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

            problems.append(
                Problem(expression=self._format_expression(node), answer=format_fraction(value))
            )
            seen.add(canonical)

        if len(problems) < self.config.count:
            raise RuntimeError(
                "Unable to generate enough unique problems; increase range or decrease count."
            )
        return problems

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
            assert node.value is not None
            return node.value

        assert node.left and node.right and node.op
        left_val = self._evaluate(node.left)
        right_val = self._evaluate(node.right)
        if left_val is None or right_val is None:
            return None

        if node.op == "+":
            value = left_val + right_val
        elif node.op == "-":
            if left_val < right_val:
                return None
            value = left_val - right_val
        elif node.op == "*":
            value = left_val * right_val
        else:
            if right_val == 0:
                return None
            if left_val <= 0 or right_val <= left_val:
                return None
            value = left_val / right_val
            if value >= 1:
                return None

        node.value = value
        return value

    def _format_expression(self, node: ExpressionNode) -> str:
        if node.is_leaf():
            assert node.value is not None
            return format_fraction(node.value)
        assert node.left and node.right and node.op
        return f"({self._format_expression(node.left)} {node.op} {self._format_expression(node.right)})"

    def _canonical(self, node: ExpressionNode) -> str:
        if node.is_leaf():
            assert node.value is not None
            return f"{node.value.numerator}/{node.value.denominator}"
        assert node.left and node.right and node.op
        left = self._canonical(node.left)
        right = self._canonical(node.right)
        if node.op in COMMUTATIVE and left > right:
            left, right = right, left
        return f"{node.op}[{left}][{right}]"

    def _random_operand(self) -> Fraction:
        should_use_fraction = (
            self.config.allow_fraction_operands
            and self.config.range_limit > 2
            and self._rng.random() < 0.35
        )
        if should_use_fraction:
            upper = max(2, self.config.range_limit - 1)
            denominator = self._rng.randint(2, upper)
            numerator = self._rng.randint(1, denominator - 1)
            return Fraction(numerator, denominator)
        upper = max(0, self.config.range_limit - 1)
        return Fraction(self._rng.randint(0, upper))
