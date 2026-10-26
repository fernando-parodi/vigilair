# May 2026 Sensirion Pro — Historical evaluation record

**Evidence classification: Tier B — historical internal analysis, not independently revalidated for this publication.**

The evaluation used **Sensirion SCD41 + SGP41** with a Seeed XIAO ESP32-S3 and Orange Pi 5 Plus ingestion/dashboard workflow. The earlier **SCD41 + ENS160** dashboard is a different configuration and must not be conflated with this test.

## Archived report-level observations

| Historical metric | Previously reported | Current verification |
| --- | ---: | --- |
| Analysis window | Approximately 24 hours | Original CSV not available in this workspace |
| Rows processed | 17,279 | Not yet reproduced |
| Median sampling interval | 5 seconds | Not yet reproduced |
| Candidate events | 19 | Exploratory algorithm, not independently reviewed |
| VOC-dominant events, tentatively IPA-like | 3 | Source not chemically confirmed |
| Combined breathing+VOC candidates | 2 | Hypothesized source |
| Breathing-dominant candidate | 1 | Hypothesized source |
| Other signal disturbances | 13 | Unclassified |

The original archive was saved under the filename `vigilair_sensirion_pro_last_1440_min.csv`. Its *full local Windows directory* is intentionally omitted from the public repository. The direct source file, its column headers, the sensor calibration record and its SHA-256 are not yet in the repository.

## Three previously highlighted events

All numbers are **reported relative changes** from an earlier exploratory analysis. The exact event timestamps, baselines and processing definitions are not independently checked.

| Event index | Δ SCD41 CO₂ | Δ SGP41 VOC Index | Additional reported signal | Interpretation status |
| --- | ---: | ---: | --- | --- |
| 12 | +16 ppm | +440 index points | +2,714 µg/m³ *engineering-derived* TVOC proxy | VOC-dominant; substance **not identified** |
| 14 | +3,253 ppm | +231 index points | +16.9 percentage points RH | Breathing-associated candidate; not controlled attribution |
| 19 | +1 ppm | +430 index points | Not documented in available summary | VOC-dominant; substance **not identified** |

These observations support studying contrasting sensor responses, **not** claiming that the SGP41 measures VOC concentration or identifies chemical species. The reported engineering TVOC proxy is not certified µg/m³ exposure evidence.

## What will make this reproducible?

1. Open the original file locally and compute its SHA-256.
2. Check the true header, timezone semantics, row count, time span and sample cadence.
3. Export the *aggregate-only* audit JSON from the public script.
4. Verify calibration/compensation provenance independently.
5. Review the redacted report before choosing any information to commit publicly.

**Important:** the previous event classifier and its proprietary algorithm are not included. Recomputing or endorsing those event categories is not part of the public audit script.
