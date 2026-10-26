import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "analysis"))
from csv_report import parse_timestamp, summarize


class ReportTests(unittest.TestCase):
    def test_fixture(self):
        result = summarize(ROOT / "examples" / "analysis" / "sample_synthetic.csv")
        self.assertEqual(result["records"], 6)
        self.assertEqual(result["median_cadence_seconds"], 5.0)
        self.assertEqual(result["gaps_over_2x_median"], 1)
        self.assertEqual(result["metrics"]["co2_ppm"]["min"], 515.0)
        self.assertEqual(result["metrics"]["voc_index"]["max"], 170.0)

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            parse_timestamp("2026-01-01T00:00:00")

    def test_non_monotonic_time_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("timestamp_utc,co2_ppm\n2026-01-01T00:00:05Z,500\n2026-01-01T00:00:00Z,510\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "strictly increasing"):
                summarize(path)

    def test_index_not_claimed_as_concentration(self):
        report = summarize(ROOT / "examples" / "analysis" / "sample_synthetic.csv")
        self.assertIn("dimensionless", report["note"])
        self.assertNotIn("tvoc_ppb", report["metrics"])


if __name__ == "__main__":
    unittest.main()
