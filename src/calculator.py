"""Simple calculator module for CI demonstration."""

from __future__ import annotations

import ast
import math
import operator
import os
from collections.abc import Sequence
from typing import Callable, SupportsFloat

BinaryOpMap = dict[type[ast.operator], Callable[[float, float], float]]
UnaryOpMap = dict[type[ast.unaryop], Callable[[float], float]]


def add(a: float, b: float) -> float:
    """Add two numbers."""

    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""

    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""

    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b.

    Raises:
        ValueError: If b is zero.
    """

    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: SupportsFloat, exponent: SupportsFloat) -> float:
    """Raise base to the power of exponent."""

    return math.pow(float(base), float(exponent))


def evaluate_expression(expression: str) -> float:
    """Safely evaluate a basic arithmetic expression using ``ast``."""

    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:  # pragma: no cover - defensive
        raise ValueError("Invalid numeric expression") from exc
    return _evaluate_ast(parsed)


def run_calculation(calc_command: str | Sequence[str]) -> str:
    """Evaluate a calculation string locally without invoking subprocesses."""

    if isinstance(calc_command, str):
        expression = calc_command
    else:
        expression = " ".join(calc_command)
    return str(evaluate_expression(expression.strip()))


# Load secrets from the environment instead of hardcoding them.
API_KEY = os.getenv("APP_API_KEY", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")


_BINARY_OPERATIONS: BinaryOpMap = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

_UNARY_OPERATIONS: UnaryOpMap = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_ast(node: ast.AST) -> float:
    """Recursively evaluate a restricted arithmetic AST tree."""

    if isinstance(node, ast.Expression):
        return _evaluate_ast(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATIONS:
        operand = _evaluate_ast(node.operand)
        return _UNARY_OPERATIONS[type(node.op)](operand)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATIONS:
        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Cannot divide by zero")
        return _BINARY_OPERATIONS[type(node.op)](left, right)
    raise ValueError("Unsupported expression")
