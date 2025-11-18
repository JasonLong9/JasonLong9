from __future__ import annotations

import re
from fractions import Fraction
from typing import List, Sequence

OPERATORS = {"+", "-", "*", "/"}
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def _tokenize(expr: str) -> List[str]:
    spaced = expr.replace("(", " ( ").replace(")", " ) ")
    return [tok for tok in spaced.split() if tok]


def _to_postfix(tokens: Sequence[str]) -> List[str]:
    output: List[str] = []
    op_stack: List[str] = []
    for token in tokens:
        if token in OPERATORS:
            while op_stack and op_stack[-1] in OPERATORS and PRECEDENCE[op_stack[-1]] >= PRECEDENCE[token]:
                output.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Mismatched parentheses")
            op_stack.pop()
        else:
            output.append(token)
    while op_stack:
        top = op_stack.pop()
        if top in ("(", ")"):
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output


def _apply_operator(op: str, a: Fraction, b: Fraction) -> Fraction:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def parse_fraction(text: str) -> Fraction:
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(text), 1)


def eval_expression(expr: str) -> Fraction:
    tokens = _tokenize(expr)
    postfix = _to_postfix(tokens)
    stack: List[Fraction] = []
    for token in postfix:
        if token in OPERATORS:
            b = stack.pop()
            a = stack.pop()
            stack.append(_apply_operator(token, a, b))
        else:
            stack.append(parse_fraction(token))
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"

