import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import plagiarism_checker as pc


class TestPlagiarismChecker(unittest.TestCase):
    def test_identical_text(self) -> None:
        text = "Deep learning models need data"
        self.assertAlmostEqual(pc.compute_similarity(text, text), 1.0)

    def test_disjoint_text(self) -> None:
        a = "machine learning improves performance"
        b = "basketball tactics require teamwork"
        self.assertAlmostEqual(pc.compute_similarity(a, b), 0.0)

    def test_case_and_punctuation_insensitive(self) -> None:
        a = "Hello, World!"
        b = "hello world"
        self.assertAlmostEqual(pc.compute_similarity(a, b, window=2), 1.0)

    def test_partial_overlap(self) -> None:
        a = "a b c d"
        b = "a b x y"
        score = pc.compute_similarity(a, b, window=2)
        self.assertAlmostEqual(score, 0.2)

    def test_window_larger_than_words(self) -> None:
        a = "only two"
        b = "only three words"
        score = pc.compute_similarity(a, b, window=3)
        self.assertEqual(score, 0.0)

    def test_empty_both(self) -> None:
        self.assertEqual(pc.compute_similarity("", ""), 1.0)

    def test_empty_vs_nonempty(self) -> None:
        self.assertEqual(pc.compute_similarity("", "content here"), 0.0)

    def test_invalid_window(self) -> None:
        with self.assertRaises(ValueError):
            pc.build_shingles(["a", "b"], window=0)

    def test_similarity_from_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orig = Path(tmp) / "orig.txt"
            suspect = Path(tmp) / "suspect.txt"
            orig.write_text("natural language processing", encoding="utf-8")
            suspect.write_text("language processing tasks", encoding="utf-8")
            score = pc.similarity_from_files(orig, suspect, window=2)
        expected = pc.compute_similarity("natural language processing", "language processing tasks", window=2)
        self.assertAlmostEqual(score, expected)

    def test_cli_outputs_percentage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orig = Path(tmp) / "orig.txt"
            suspect = Path(tmp) / "suspect.txt"
            orig.write_text("A B C", encoding="utf-8")
            suspect.write_text("A B D", encoding="utf-8")

            buffer = io.StringIO()
            out_file = Path(tmp) / "result.txt"
            with redirect_stdout(buffer):
                pc.main([str(orig), str(suspect), str(out_file), "--window", "2"])
            output = buffer.getvalue().strip()
            file_output = out_file.read_text(encoding="utf-8").strip()

        # With window=2, shingles are {AB, BC} vs {AB, BD} => 1/3 overlap = 33.33%
        self.assertEqual(output, "33.33%")
        self.assertEqual(file_output, "33.33%")

    def test_format_percentage_bounds(self) -> None:
        self.assertEqual(pc.format_percentage(1.5), "100.00%")
        self.assertEqual(pc.format_percentage(-0.2), "0.00%")


if __name__ == "__main__":
    unittest.main()
