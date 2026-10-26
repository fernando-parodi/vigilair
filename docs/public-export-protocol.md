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
py -3 .\scripts\public_measurement_audit.py --csv "F:\SGP41 and SCD41 new device\data_analysis\vigilair_sensirion_pro_last_1440_min.csv" --out "$env:USERPROFILE\Desktop\vigilair-v02-review"
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
