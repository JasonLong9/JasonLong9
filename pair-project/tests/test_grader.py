import os
import tempfile
import unittest

from arithmetic_generator.grader import GradeResult, grade


class GraderTests(unittest.TestCase):
    def test_grade_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            exercises_path = os.path.join(tmpdir, "ex.txt")
            answers_path = os.path.join(tmpdir, "ans.txt")
            with open(exercises_path, "w", encoding="utf-8") as f:
                f.write("(1 + 1) =\n")
                f.write("1/2 + 1/4 =\n")
                f.write("(3 - 1) * 2 =\n")
            with open(answers_path, "w", encoding="utf-8") as f:
                f.write("2\n")          # correct
                f.write("1/2\n")       # wrong
                f.write("4\n")         # correct

            result: GradeResult = grade(exercises_path, answers_path, output_file=os.path.join(tmpdir, "Grade.txt"))
            self.assertEqual(result.correct, [1, 3])
            self.assertEqual(result.wrong, [2])

            with open(os.path.join(tmpdir, "Grade.txt"), "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Correct: 2 (1, 3)", content)
            self.assertIn("Wrong: 1 (2)", content)


if __name__ == "__main__":
    unittest.main()

