import re
import unittest

from arithmetic_generator import GeneratorConfig, ProblemGenerator


def _extract_numbers(expr: str) -> list[str]:
    return re.findall(r"\d+/\d+|\d+", expr)


class GeneratorTests(unittest.TestCase):
    def test_generate_basics(self) -> None:
        config = GeneratorConfig(count=20, range_limit=10, seed=42, max_operators=3)
        generator = ProblemGenerator(config)
        problems = generator.generate()

        self.assertEqual(len(problems), 20)
        expressions = [p.expression for p in problems]
        self.assertEqual(len(set(expressions)), 20)

        for expr, answer in zip(expressions, [p.answer for p in problems]):
            self.assertLessEqual(len(re.findall(r"\s[+\-*/]\s", expr)), 3)
            for num in _extract_numbers(expr):
                if "/" in num:
                    n, d = map(int, num.split("/"))
                    self.assertGreater(n, 0)
                    self.assertLess(n, d)
                    self.assertLess(d, config.range_limit)
                else:
                    self.assertGreaterEqual(int(num), 0)
                    self.assertLess(int(num), config.range_limit)
            if "/" in answer:
                n, d = map(int, answer.split("/"))
                self.assertGreaterEqual(n, 0)
                self.assertGreater(d, 0)
            else:
                self.assertGreaterEqual(int(answer), 0)

    def test_division_results_proper_fraction(self) -> None:
        config = GeneratorConfig(count=30, range_limit=8, seed=7, max_operators=3)
        generator = ProblemGenerator(config)
        problems = generator.generate()
        for prob in problems:
            if " / " in prob.expression and "/" in prob.answer:
                n, d = map(int, prob.answer.split("/"))
                self.assertLess(n, d)


if __name__ == "__main__":
    unittest.main()
