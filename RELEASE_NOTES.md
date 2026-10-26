# v0.2 — Measurement Transparency (provenance framework)

- Added data provenance classifications: direct source verification versus historical analysis versus illustration versus synthetic fixtures.
- Added the detailed May 2026 **SCD41 + SGP41** historical evaluation summary, including the 17,279-row/5-second/19-candidate-event figures marked **not yet independently reproduced**.
- Added a field dictionary distinguishing measured SCD41 CO₂ from eCO₂, and SGP41 relative VOC/NOx indices from pollutant concentration.
- Added a **fully offline** Python SHA-256 and CSV-summary audit tool. It exports no source path, absolute timestamps, raw measurements, event traces or device IDs.
- Added seven automated tests for the new audit tool (tested on synthetic fixtures locally).
- Added an exact PowerShell command for the archived Windows F: drive CSV, producing a private review report before any upload.
- Full firmware, raw time-series, specific chemical identification and calibration claims **remain excluded**.

**Status:** v0.2 transparency workflow published. Real-source checksum and statistics are pending running the tool on the original file. This is not a verified new data release or an official GitHub tagged release.

---

# Public release v0.1.0 — Engineering showcase

Initial curated public VigilAir portfolio publication (October 2026).

Includes architecture and measurement semantics, historical observations and limitations, a historical SCD4x CRC-8 excerpt with a C++ test, a stand-alone Python CSV diagnostics example with synthetic data and tests, and public roadmap.

**Excluded:** Full commercial firmware, device secrets, private raw measurements, production decision logic and proprietary analytics.

Public version numbers are distinct from historical internal device labels, e.g. VigilAir v3.2.

The earlier dashboard screenshot is preserved outside this initial GitHub commit; a separate image upload can be added after review.
