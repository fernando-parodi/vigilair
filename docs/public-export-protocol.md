# Local-only archive audit and safe publication protocol

The May 2026 source CSV is on the Windows data drive, **not** within this public GitHub repository. Do not upload the source CSV or the device's original firmware.

## 1. Clone the public repository

In Windows PowerShell:

```powershell
git clone https://github.com/fernando-parodi/vigilair.git
cd vigilair
```

If you already have the repository, run `git pull` instead of cloning. Python 3 is required; the script uses only the standard library.

## 2. Compute a local redacted audit

```powershell
$csv = Read-Host "Enter the full path to your original VigilAir CSV"
py -3 .\scripts\public_measurement_audit.py --csv "$csv" --out "$env:USERPROFILE\Desktop\vigilair-v02-review"
```

This creates **only** `vigilair_v02_public_audit.json` in the desktop review folder, not in GitHub. The script produces a local SHA-256 and aggregated statistics. It does not open the network or export raw measurements.

## 3. Verify before publication

Inspect the JSON locally and check:
- `rows_read` versus 17,279 historically reported, plus any extra header or maintenance rows.
- `found_measurement_fields`: is true CO₂ correctly mapped, and eCO₂ **not** mistaken for it?
- `cadence`: if timestamps are absent/ambiguous, no unsupported 5-second claim should be inferred.
- Warnings, sample gaps, missing values and probable sensor-conditioning effects.
- Any metrics that could expose site behavior. Even aggregate extremes may be sensitive.

## 4. Share or publish only approved derived evidence

The output JSON is designed to limit information disclosure, but it still exposes summary statistics and a unique source-file hash; review it before sharing. It is **not automatically committed**, and **no original CSV rows are published**.

Once the summary has been verified and approved, add a redacted copy under `evidence/verified/` in a later patch with a source-data provenance note and the audit program's commit hash.

## 5. Keep analysis claims separate

The historical 19 event labels were assigned by an unpublished exploratory analyzer. The public script does not reproduce or verify those classifications. Do not present its report as chemical identification or regulatory exposure monitoring.

## 2b. Check timestamps when cadence is unavailable

As of v0.2.1, the local audit explicitly reports `timestamp_order_diagnostics`: count of adjacent backward steps, adjacent equal steps, repeated timestamps, chronological span and diagnostic intervals derived from **sorted unique** timestamps. The report also includes `scd41_rh_pct` as relative humidity.

**Important:** chronologically sorting timestamps is a forensic diagnostic, **not** proof that the acquisition stream had no duplicate, missing or out-of-order samples. The audit keeps `cadence: null` when original row order is not strictly increasing. Read `warnings` as well as `timestamp_order_diagnostics`.

To update an existing clone before re-running the same command:

```powershell
git pull
# Repeat the py -3 audit command above with your local CSV path
```

You can inspect only the redacted diagnostic summary without displaying the sensor data:

```powershell
$a = Get-Content "$env:USERPROFILE\Desktop\vigilair-v02-review\vigilair_v02_public_audit.json" -Raw | ConvertFrom-Json
$a.timestamp_order_diagnostics | Format-List
$a.found_measurement_fields | Format-List
$a.warnings
```

If there are backward steps, the original CSV may be unsorted, may contain duplicates, or may have experienced a logger clock correction. Investigate before calling the sampling cadence verified.
