import unittest
from fractions import Fraction

from arithmetic_generator.evaluator import eval_expression, format_fraction, parse_fraction


class EvaluatorTests(unittest.TestCase):
    def test_eval_expression(self) -> None:
        expr = "(1/2 + 1/3) * (2 + 1)"
        result = eval_expression(expr)
        self.assertEqual(result, Fraction(5, 6) * 3)

    def test_format_and_parse_fraction(self) -> None:
        value = Fraction(6, 4)
        self.assertEqual(format_fraction(value), "3/2")
        self.assertEqual(parse_fraction("3/2"), Fraction(3, 2))
        self.assertEqual(parse_fraction("5"), Fraction(5, 1))


if __name__ == "__main__":
    unittest.main()

