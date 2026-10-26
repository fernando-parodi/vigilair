#!/usr/bin/env python3
"""VigilAir public CSV diagnostics example; NOT production analytics."""
from __future__ import annotations
import argparse
import csv
import json
import math
import statistics
from datetime import datetime
from pathlib import Path

COLUMNS = ("co2_ppm", "voc_index", "nox_index", "temperature_c", "rh_pct")


def parse_timestamp(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    t = datetime.fromisoformat(value)
    if t.tzinfo is None or t.utcoffset() is None:
        raise ValueError("timestamp_utc must include a UTC offset or Z")
    return t


def summarize(path: Path) -> dict:
    timestamps = []
    data = {key: [] for key in COLUMNS}
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "timestamp_utc" not in reader.fieldnames:
            raise ValueError("CSV requires timestamp_utc column")
        for row_num, row in enumerate(reader, start=2):
            try:
                t = parse_timestamp(row["timestamp_utc"] or "")
                if timestamps and t <= timestamps[-1]:
                    raise ValueError("timestamps must be strictly increasing")
                timestamps.append(t)
                for key in COLUMNS:
                    raw = (row.get(key) or "").strip()
                    if raw:
                        val = float(raw)
                        if not math.isfinite(val):
                            raise ValueError(f"nonfinite {key}")
                        data[key].append(val)
            except (ValueError, TypeError) as e:
                raise ValueError(f"CSV row {row_num}: {e}") from e
    if not timestamps:
        raise ValueError("CSV has no records")
    deltas = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]
    median = statistics.median(deltas) if deltas else None
    return {
        "source": path.name,
        "records": len(timestamps),
        "from": timestamps[0].isoformat(),
        "to": timestamps[-1].isoformat(),
        "duration_seconds": (timestamps[-1] - timestamps[0]).total_seconds(),
        "median_cadence_seconds": median,
        "gaps_over_2x_median": sum(d > 2 * median for d in deltas) if median else 0,
        "metrics": {
            key: {"n": len(vals), "min": min(vals), "max": max(vals), "mean": round(statistics.fmean(vals), 4)}
            for key, vals in data.items() if vals
        },
        "note": "Sensor indices remain dimensionless; no VOC-index-to-ppb conversion is applied."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Report basic statistics from a VigilAir-format CSV")
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.csv), indent=2))


if __name__ == "__main__":
    main()
