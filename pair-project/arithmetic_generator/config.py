from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GeneratorConfig:
    """Configuration for generating arithmetic problems."""

    count: int = 20
    range_limit: int = 10
    max_operators: int = 3
    max_attempts: int = 100_000
    allow_fraction_operands: bool = True
    seed: int | None = None

    def __post_init__(self) -> None:
        if self.count <= 0 or self.count > 10_000:
            raise ValueError("count must be between 1 and 10000")
        if self.range_limit <= 0:
            raise ValueError("range_limit must be positive")
        if self.max_operators <= 0 or self.max_operators > 3:
            raise ValueError("max_operators must be within 1~3")
        if self.max_attempts < self.count:
            raise ValueError("max_attempts must not be smaller than count")
