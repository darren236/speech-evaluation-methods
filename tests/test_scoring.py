import json
from pathlib import Path
import tempfile
import unittest

from speech_eval.cli import score
from speech_eval.scoring import score_pair, tokenize


ROOT = Path(__file__).resolve().parents[1]


class ScoringTests(unittest.TestCase):
    def test_edit_operations_and_rate(self):
        result = score_pair("one two three", "one four three five")
        self.assertEqual((result.substitutions, result.deletions, result.insertions), (1, 0, 1))
        self.assertAlmostEqual(result.rate, 2 / 3)

    def test_particles_preserved_and_punctuation_removed(self):
        self.assertEqual(tokenize("Okay [ah], lah!"), ["okay", "ah", "lah"])
        self.assertEqual(score_pair("okay lah", "okay").deletions, 1)
        self.assertEqual(score_pair("Hello, world!", "hello world").rate, 0)
        self.assertGreater(score_pair("Hello, world!", "hello world", policy="strict").rate, 0)

    def test_cjk_character_scoring_and_empty_reference(self):
        self.assertEqual(score_pair("我刚开始", "我开始", unit="character").deletions, 1)
        empty = score_pair("", "extra")
        self.assertIsNone(empty.rate)
        self.assertEqual(empty.insertions, 1)

    def test_manifest_completeness_and_micro_average(self):
        result = score(ROOT / "examples/references.jsonl", ROOT / "examples/hypotheses.jsonl", "basic")
        self.assertEqual(result["utterances"], 3)
        self.assertEqual(result["overall"]["word"]["reference_units"], 14)
        self.assertIn("code-switch", result["groups"])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "hypotheses.jsonl"
            path.write_text(json.dumps({"id": "singlish-1", "hypothesis": "okay"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ID mismatch"):
                score(ROOT / "examples/references.jsonl", path, "basic")


if __name__ == "__main__":
    unittest.main()
