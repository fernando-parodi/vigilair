# Runnable public excerpts

## CRC-8 protocol check

`scd4x_crc8.h` isolates the actual CRC-8 routine used by the historical VigilAir SCD41/ENS160 firmware. It is protocol-level code, not a complete device driver.

```bash
g++ -std=c++17 -Wall -Wextra -Werror -pedantic examples/test_scd4x_crc8.cpp -o /tmp/vigilair_crc_test
/tmp/vigilair_crc_test
```

## CSV diagnostics

`analysis/csv_report.py` is an independently runnable **public demo**, not the original proprietary analytics engine. It reports cadence and basic statistics, with no invented concentration conversions.

```bash
python3 examples/analysis/csv_report.py examples/analysis/sample_synthetic.csv
python3 -m unittest discover -s tests -v
```

Required column: `timestamp_utc`, ISO 8601 with an explicit timezone. Optional metric columns: `co2_ppm`, `voc_index`, `nox_index`, `temperature_c`, `rh_pct`. Synthetic test values are not actual measured observations.
