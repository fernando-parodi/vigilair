# VigilAir Sensirion Pro — acquisition timing audit (v0.2.1)

**Status:** Public, owner-approved **aggregate-only** findings from a locally executed audit of the original archived CSV.  
**Evidence level:** Direct owner-run source-file audit of **timestamp/recording structure**; original source remains private. The source file was read on the owner's computer, **not independently reprocessed by the public repository or a third party**.  
**Experiment:** Historical SCD41 + SGP41 Sensirion Pro measurement archive (May 2026).  
**Audit reporting date:** 2026-10-26.  
**Tools:** VigilAir `scripts/public_measurement_audit.py` (v0.2.1 timestamp-order diagnostics) plus a separate local read-only Python comparison of consecutive timestamp, sensor-field and `uptime_ms` values.

## Source-backed acquisition findings

| Item | Audited result |
| --- | ---: |
| Stored CSV measurement rows | **17,280** |
| Parseable timestamps | **17,280** |
| Distinct UTC timestamps | **17,279** |
| Elapsed span from earliest to latest timestamp | **86,396 s (23:59:56)** |
| Consecutive row-to-row timestamp intervals | **17,279** |
| Intervals of exactly 5 s | **17,277** |
| Intervals of exactly 11 s | **1** |
| Intervals of exactly 0 s | **1** |
| Timestamp reversals (negative adjacent deltas) | **0** |
| Equal consecutive timestamps | **1** |
| Unique-timestamp median spacing | **5 s** |
| Identical sensor values at the repeated timestamp | **0 adjacent pairs** |
| Different sensor values at the repeated timestamp | **1 adjacent pair** |
| Device uptime delta across the equal-time pair | **+2,317 ms** |
| Decreases in consecutive device uptime values | **0** |

The recorded 5-second intervals account for **17,277/17,279 adjacent timestamp intervals (approximately 99.988%)**. This is a statement about **timestamp spacing**, not an independently validated sensor sampling accuracy or packet-delivery rate.

## Interpretation

- **The two records sharing a UTC timestamp contain different sensor-field values.** They are not byte-for-byte duplicates of the compared sensor readings. An uptime advance of 2,317 ms occurred across that pair. The reason both were assigned the same UTC timestamp is **undetermined**.
- **One 11-second interval** is longer than the predominant 5-second pattern. It may reflect a logging delay, missing acquisition, or other system behavior; these explanations are hypotheses, not verified diagnoses.
- **No timestamp went backwards**, and no decreases in the device uptime counter were found in the adjacent records examined. This argues against a simple backward-time step or uptime-counter reset *within the inspected record sequence*, but **does not prove there were no device interruptions**.
- The earlier historical result of **17,279** now matches the number of **unique timestamps**, while the CSV contains **17,280 stored rows**. It is plausible the historical count used unique timestamps, but the original earlier counting method has not been recovered.

## Evidence scope and limitations

These figures come from local aggregate audit and follow-up diagnostic outputs supplied by the project owner, not from a raw CSV committed here. The source was checked with a SHA-256 digest on the owner's computer. **The digest is intentionally withheld from this public evidence.**

**Not established:** complete acquisition continuity, actual missed-sample count, timestamp-assignment root cause, sensor calibration/accuracy, concentration compliance, chemical attribution, original 19 candidate-event reproducibility, or independent reference-instrument agreement.

The full CSV, raw measurements, sensor identifiers, IP/network information, exact capture timestamps, local source paths, firmware and proprietary event detection logic remain **unpublished**.

**Reproducibility:** The open-source [local audit script](../../scripts/public_measurement_audit.py) and [public export protocol](../../docs/public-export-protocol.md) describe how an authorized holder of the private source archive can repeat the aggregate analysis; the second read-only duplicate/uptime comparison was run locally and is documented by its summary values above.

**Sensor semantics:** SCD41 directly measures CO₂; SGP41 VOC and NOx indices are relative, dimensionless indicators, not certified chemical concentrations.
