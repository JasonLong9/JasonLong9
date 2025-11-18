from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GeneratorConfig:
    """Placeholder for generator configuration."""

    count: int = 20
    range_limit: int = 10

