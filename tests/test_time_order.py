"""Synthetic-only checks for the v0.2.1 timestamp-order diagnostics."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from public_measurement_audit import audit, diagnose_time_order


class TimestampOrderTests(unittest.TestCase):
    def test_perfect_5_second_cadence(self):
        d = diagnose_time_order([0, 5, 10, 15])
        self.assertTrue(d["source_order_verified"])
        self.assertEqual(d["unique_timestamps"], 4)
        self.assertEqual(d["sorted_unique_median_interval_seconds"], 5)
        self.assertEqual(d["chronological_span_seconds"], 15)
        self.assertEqual(d["adjacent_backward_steps"], 0)

    def test_one_backward_step_not_claimed_as_verified(self):
        d = diagnose_time_order([0, 10, 5, 15])
        self.assertFalse(d["source_order_verified"])
        self.assertEqual(d["adjacent_backward_steps"], 1)
        self.assertEqual(d["largest_backward_jump_seconds"], 5)
        self.assertEqual(d["sorted_unique_median_interval_seconds"], 5)

    def test_duplicate_timestamps(self):
        d = diagnose_time_order([0, 5, 5, 10])
        self.assertFalse(d["source_order_verified"])
        self.assertEqual(d["adjacent_equal_steps"], 1)
        self.assertEqual(d["repeated_timestamp_rows"], 1)
        self.assertEqual(d["unique_timestamps"], 3)

    def test_gap_in_sorted_unique_is_not_verified_capture(self):
        d = diagnose_time_order([0, 5, 20, 25, 10])
        self.assertEqual(d["sorted_unique_gaps_over_2x_median"], 1)
        self.assertFalse(d["source_order_verified"])

    def test_actual_aliases_from_historical_sensor_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "test.csv"
            src.write_text(
                "ts_utc,co2_ppm,scd41_temp_c,scd41_rh_pct,sraw_voc,sraw_nox,voc_index,nox_index\n"
                "2026-01-01T00:00:00Z,500,24.0,48,111,222,100,100\n"
                "2026-01-01T00:00:10Z,515,24.2,49,112,221,101,101\n"
                "2026-01-01T00:00:05Z,510,24.1,48.5,113,220,102,101\n",
                encoding="utf-8",
            )
            result = audit(src)
            self.assertEqual(result["rows_read"], 3)
            self.assertIsNone(result["cadence"])
            self.assertEqual(result["found_measurement_fields"]["rh_pct"], "scd41_rh_pct")
            self.assertEqual(result["statistics"]["rh_pct"]["n_numeric"], 3)
            self.assertEqual(result["timestamp_order_diagnostics"]["adjacent_backward_steps"], 1)
            self.assertEqual(result["timestamp_order_diagnostics"]["chronological_span_seconds"], 10)
            self.assertNotIn("2026-01-01", str(result))
            self.assertNotIn(str(src.parent), str(result))


if __name__ == "__main__":
    unittest.main()
