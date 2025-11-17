from __future__ import annotations

import sys

from plagiarism_checker import main as run_checker


if __name__ == "__main__":
    run_checker(sys.argv[1:])
