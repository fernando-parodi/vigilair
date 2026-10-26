#!/usr/bin/env python3
"""VigilAir public reproducibility tool. Produces a privacy-reduced LOCAL audit.

Does not upload, transmit, or publish the original file. No external packages.
Output is a digest and aggregate, NOT a substitute for certified calibration.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

FIELDS = {
    "co2_ppm": {"co2ppm", "scd41co2ppm", "co2scd41ppm", "co2", "trueco2ppm"},
    "voc_index": {"vocindex", "sgp41vocindex"},
    "nox_index": {"noxindex", "sgp41noxindex"},
    "temperature_c": {"temperaturec", "tempc", "scd41temperaturec", "scd41tempc", "temp"},
    "rh_pct": {"rhpct", "relativehumidity", "relativehumiditypct", "humiditypct", "rh", "scd41rhpct", "scd41rh", "scd41relativehumiditypct"},
    "sraw_voc": {"srawvoc", "rawvoc", "sgp41rawvoc"},
    "sraw_nox": {"srawnox", "rawnox", "sgp41rawnox"},
}
TIME_ALIASES = {"timestamputc", "timestamp", "timeutc", "datetimeutc", "datetime", "tsutc", "ts", "time", "recordedat", "recordedatutc"}


def normalized(s: str) -> str:
    return "".join(c.lower() for c in (s or "") if c.isalnum())


def timestamp_seconds(s: str) -> float:
    s = s.strip()
    if not s:
        raise ValueError("empty timestamp")
    if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
        n = int(s)
        if len(s.lstrip("-")) >= 13:
            n /= 1000.0
        return float(n)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    t = datetime.fromisoformat(s)
    if t.tzinfo is None or t.utcoffset() is None:
        raise ValueError("timestamp has no explicit timezone")
    return t.astimezone(timezone.utc).timestamp()


def quantile(sorted_values: list[float], q: float) -> float:
    idx = q * (len(sorted_values) - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    return sorted_values[lo] * (hi - idx) + sorted_values[hi] * (idx - lo) if lo != hi else sorted_values[lo]


def diagnose_time_order(times: list[float]) -> dict:
    """Aggregate timestamp integrity without revealing a single absolute timestamp.

    Chronologically sorting timestamps can *characterize* a dataset but does not
    establish that the logger actually captured rows in that order. Keep it
    separate from validated acquisition-order cadence.
    """
    if not times:
        return {"parsed_timestamps": 0, "source_order_verified": False}

    row_deltas = [b - a for a, b in zip(times, times[1:])]
    backwards = [d for d in row_deltas if d < 0]
    equals = sum(d == 0 for d in row_deltas)
    unique_times = sorted(set(times))
    sorted_deltas = [b - a for a, b in zip(unique_times, unique_times[1:])]
    median_sorted = statistics.median(sorted_deltas) if sorted_deltas else None

    return {
        "parsed_timestamps": len(times),
        "unique_timestamps": len(unique_times),
        "repeated_timestamp_rows": len(times) - len(unique_times),
        "source_order_verified": not backwards and not equals,
        "adjacent_backward_steps": len(backwards),
        "adjacent_equal_steps": equals,
        "largest_backward_jump_seconds": round(-min(backwards), 3) if backwards else 0,
        "chronological_span_seconds": round(unique_times[-1] - unique_times[0], 3),
        "sorted_unique_median_interval_seconds": round(median_sorted, 3) if median_sorted else None,
        "sorted_unique_gaps_over_2x_median": (
            sum(d > 2 * median_sorted for d in sorted_deltas)
            if median_sorted else None
        ),
        "largest_sorted_unique_gap_seconds": round(max(sorted_deltas), 3) if sorted_deltas else None,
        "sorted_interval_warning": (
            "Sorted timestamps are only a diagnostic: they do NOT prove acquisition order, "
            "sample completeness, or a continuous 24-hour logger run."
        ),
    }


def audit(path: Path) -> dict:
    checksum = hashlib.sha256()
    with path.open("rb") as raw:
        for chunk in iter(lambda: raw.read(1024 * 1024), b""):
            checksum.update(chunk)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if not headers:
            raise ValueError("No header row found in source CSV")
        canon = {normalized(h): h for h in headers}
        mapping = {kind: next((canon[a] for a in sorted(aliases) if a in canon), None) for kind, aliases in FIELDS.items()}
        time_col = next((canon[a] for a in sorted(TIME_ALIASES) if a in canon), None)
        values = {name: [] for name in FIELDS}
        missing = Counter()
        invalid = Counter()
        times = []
        timestamps_rejected = 0
        n = 0
        for row in reader:
            n += 1
            for kind, col in mapping.items():
                if col is None:
                    continue
                val = (row.get(col) or "").strip()
                if not val:
                    missing[kind] += 1
                    continue
                try:
                    x = float(val)
                    if not math.isfinite(x):
                        raise ValueError("non-finite")
                    values[kind].append(x)
                except ValueError:
                    invalid[kind] += 1
            if time_col:
                try:
                    times.append(timestamp_seconds(row.get(time_col) or ""))
                except (ValueError, TypeError, OverflowError):
                    timestamps_rejected += 1
        if n == 0:
            raise ValueError("CSV has no data rows")
    metrics = {}
    for kind, v in values.items():
        if not v:
            continue
        s = sorted(v)
        metrics[kind] = {
            "n_numeric": len(v), "missing": missing[kind], "non_numeric": invalid[kind],
            "min": round(s[0], 3), "median": round(quantile(s, 0.5), 3),
            "p95": round(quantile(s, 0.95), 3), "max": round(s[-1], 3),
        }
    cadence = None
    if time_col and not timestamps_rejected and len(times) >= 2:
        diffs = [b - a for a, b in zip(times, times[1:])]
        if all(d > 0 for d in diffs):
            med = statistics.median(diffs)
            cadence = {"duration_seconds": round(times[-1] - times[0], 3),
                       "median_cadence_seconds": round(med, 3),
                       "gaps_over_2x_median": sum(d > 2 * med for d in diffs)}
    warnings = []
    if not metrics:
        warnings.append("No recognized numeric measurement columns; inspect source headers locally.")
    if not time_col:
        warnings.append("No recognizable timestamp column; cannot validate cadence or coverage.")
    elif timestamps_rejected:
        warnings.append(f"{timestamps_rejected} timestamps could not be parsed; cadence not independently verified.")
    elif not cadence:
        warnings.append("Timestamps are not strictly increasing; cadence not independently verified.")
    for kind, m in metrics.items():
        if kind == "rh_pct" and (m["min"] < 0 or m["max"] > 100):
            warnings.append("Relative humidity values outside 0–100%; investigate sensor or parsing.")
        if kind == "co2_ppm" and m["min"] < 0:
            warnings.append("Negative CO2 values; investigate parser or source quality.")
        if kind in ("voc_index", "nox_index") and (m["min"] < 0 or m["max"] > 500):
            warnings.append(f"{kind} values outside usual index range; check source semantics.")
    return {
        "audit_schema": "vigilair-public-audit/0.2.1",
        "source_file_basename": path.name,
        "source_sha256": checksum.hexdigest(),
        "source_bytes": path.stat().st_size,
        "rows_read": n,
        "found_measurement_fields": {key: col for key, col in mapping.items() if col is not None},
        "timestamp_column_present": time_col is not None,
        "timestamp_values_rejected": timestamps_rejected if time_col else None,
        "cadence": cadence,
        "timestamp_order_diagnostics": diagnose_time_order(times) if time_col and not timestamps_rejected else None,
        "statistics": metrics,
        "warnings": warnings,
        "privacy": "Local aggregate only: no absolute timestamps, source directory, device IDs, raw observations, or events exported.",
        "interpretation": "Observed signals only. VOC/NOx indices are unitless; no pollutant identity, exposure limit, or calibration claims are established.",
        "calibration_verified": False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Audit a local VigilAir CSV without publishing the source data")
    p.add_argument("--csv", type=Path, required=True, help="Path to original CSV (never uploaded)")
    p.add_argument("--out", type=Path, required=True, help="Local output folder for redacted report")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result = audit(args.csv)
    target = args.out / "vigilair_v02_public_audit.json"
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("AUDIT_SAVED:", target)
    print("ROWS:", result["rows_read"])
    print("SHA256:", result["source_sha256"])
    print("CADENCE:", result["cadence"])
    print("TIMESTAMP_ORDER:", json.dumps(result["timestamp_order_diagnostics"], ensure_ascii=False))
    print("WARNINGS:", len(result["warnings"]))
    print("NO NETWORK ACCESS OR FILE UPLOAD PERFORMED")


if __name__ == "__main__":
    main()
