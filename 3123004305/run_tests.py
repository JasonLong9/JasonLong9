"""Helper script to run unittest discovery (used for trace coverage)."""
from __future__ import annotations

import unittest


def main() -> None:
    loader = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(loader)
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
