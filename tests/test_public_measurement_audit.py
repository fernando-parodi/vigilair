import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from public_measurement_audit import audit, normalized, timestamp_seconds


class AuditTests(unittest.TestCase):
    def _write(self, content):
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / "log.csv"
        path.write_text(content, encoding="utf8")
        return directory, path

    def test_synthetic_sample(self):
        d, p = self._write("timestamp_utc,co2_ppm,voc_index,nox_index,rh_pct\n"
                           "2026-01-01T00:00:00Z,510,100,101,45\n"
                           "2026-01-01T00:00:05Z,520,110,102,46\n"
                           "2026-01-01T00:00:10Z,530,160,103,47\n")
        with d:
            a = audit(p)
            self.assertEqual(a["rows_read"], 3)
            self.assertEqual(a["cadence"]["median_cadence_seconds"], 5.0)
            self.assertEqual(a["statistics"]["co2_ppm"]["median"], 520)
            self.assertNotIn("2026-01", str(a))
            self.assertNotIn(str(p.parent), str(a))
            self.assertFalse(a["calibration_verified"])

    def test_rejects_no_rows(self):
        d, p = self._write("timestamp_utc,co2_ppm\n")
        with d, self.assertRaisesRegex(ValueError, "no data rows"):
            audit(p)

    def test_timestamp_without_timezone_rejected(self):
        with self.assertRaises(ValueError):
            timestamp_seconds("2026-01-01T00:00:00")

    def test_missing_cadence_not_inferred(self):
        d, p = self._write("co2_ppm,raw_voc\n600,2000\n610,2010\n")
        with d:
            a = audit(p)
            self.assertIsNone(a["cadence"])
            self.assertIn("sraw_voc", a["statistics"])

    def test_no_eco2_misidentified(self):
        d, p = self._write("timestamp_utc,eco2_ppm,voc_index\n2026-01-01T00:00:00Z,1000,100\n")
        with d:
            a = audit(p)
            self.assertNotIn("co2_ppm", a["statistics"])

    def test_bad_numeric_and_gaps(self):
        d, p = self._write("timestamp,co2_ppm,rh_pct\n"
                           "2026-01-01T00:00:00Z,590,45\n"
                           "2026-01-01T00:00:05Z,bad,46\n"
                           "2026-01-01T00:00:10Z,620,47\n"
                           "2026-01-01T00:00:35Z,640,48\n")
        with d:
            a = audit(p)
            self.assertEqual(a["statistics"]["co2_ppm"]["non_numeric"], 1)
            self.assertEqual(a["cadence"]["gaps_over_2x_median"], 1)

    def test_digits_timestamp(self):
        self.assertEqual(timestamp_seconds("1767225600000"), 1767225600.0)
        self.assertEqual(normalized("CO2_ppm"), "co2ppm")


if __name__ == "__main__":
    unittest.main()
