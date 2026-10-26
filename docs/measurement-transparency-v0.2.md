# v0.2 — Measurement Transparency

**Status: provenance framework published; source-file revalidation pending.**

VigilAir distinguishes a live instrument's **measured** signals, its **algorithmic indicators**, and an investigator's **hypotheses**. This milestone makes those distinctions reviewable and gives the owner a reproducible, offline way to audit the original measurement archive.

## Evidence levels

| Tier | Meaning | Present in this repository |
| --- | --- | --- |
| A — Source verified | Original CSV actually read, hashed and analyzed using the public script | **Pending.** The original source is on a Windows F: drive, not accessible to this repository's authoring environment |
| B — Historical analysis summary | Results previously generated during the May 2026 experiment, with no new direct verification | **Available:** see [May 2026 evaluation](historical-sensirion-pro-2026-05.md) |
| C — UI or marketing illustration | Shows the look and design of the product, but does not prove a sensor reading | **Available only as legacy marketing assets outside the repository** |
| D — Synthetic fixture | Made-up numbers for automated code tests, explicitly labeled | **Available** in `examples/analysis/sample_synthetic.csv` |

The 17,279-row historical result is **Tier B** until the original CSV is read through the auditing script and its checksum and measurement schema are recorded.

## What is actually measured?

- Sensirion SCD41: real CO₂ concentration in ppm, plus temperature and relative humidity, subject to calibration and thermal considerations.
- Sensirion SGP41: raw gas-sensitive VOC/NOx signals and *relative*, dimensionless algorithmic VOC/NOx indices. **Indices are not pollutant concentrations.**
- ScioSense ENS160 (earlier prototype only): vendor-estimated TVOC and AQI category; its eCO₂ is **not** a direct CO₂ measurement.
- Engineering-derived TVOC figures in historical analysis are **not certified lab concentration measurements**, even if formatted as µg/m³.

## Reproducible audit

The only purpose of `scripts/public_measurement_audit.py` is to read a locally available CSV and generate a privacy-reduced report. It:
1. SHA-256 hashes the original bytes before parsing.
2. Counts records and recognizes known measurement aliases conservatively.
3. Summarizes numeric fields (number of observations, min/median/p95/max).
4. Validates cadence and timing gaps **only when trustworthy timestamp values are present**.
5. Exports no absolute timestamps, source folder, hardware ID, observation rows or events.

The script does not upload any data, infer pollutant identity, or claim calibration. When an input column is unknown, the tool reports this rather than fabricating a matching sensor field.

[Local use and publication protocol](public-export-protocol.md) · [Measurement dictionary](measurement-data-dictionary.md)

## Not yet claimed

- No freshly verified 24-hour sample count or correlation coefficient.
- No raw time-series release.
- No reference-calibration certificate.
- No independent chemical identification of isopropyl alcohol or other contaminants.
- No proven exposure-limit compliance, regulatory conformity or safety-critical alarming.

**A verified and voluntarily approved aggregate report can be appended in v0.2.1.** This doesn't require publishing private raw data or proprietary firmware.

## Timestamp-order diagnostic refinement (v0.2.1)

The first offline direct check of the original file returned 17,280 rows (versus the historical 17,279), zero unparseable timestamps, and `cadence: null` due to one or more adjacent non-increasing timestamps. That confirms **row count and timestamp parseability**, not time continuity.

The v0.2.1 auditor now reports counts of equal/backward adjacent timestamp steps, duplicate timestamps, sorted-unique interval estimates and total observed timestamp span. **Sorted time statistics never substitute for verified row order.** The public output omits every absolute timestamp and all raw records. It also recognizes the original SCD41 relative humidity header `scd41_rh_pct`.

The first direct source SHA-256 was calculated locally, but is intentionally not recorded in this public document until aggregate publication is reviewed and approved.
