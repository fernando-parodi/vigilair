# v0.2.1 — Verified acquisition-timing aggregate (GitHub commit milestone)

An authorized, **aggregate-only** report from the original private Sensirion Pro CSV was published after owner-run local auditing. See [evidence report](evidence/verified/sensirion-pro-acquisition-timing-v0.2.1.md).

The 17,280 stored rows (17,279 distinct timestamps) cover 23:59:56. Across 17,279 adjacent intervals: 17,277 were 5 seconds, one was 11 seconds, and one was 0 seconds. No backward timestamp steps or uptime counter decreases were seen. The same-time pair has different readings and +2,317 ms uptime.

The audit verifies **recording/timestamp structure**, not sample completeness, chemical identity, calibrated performance or historical event classifications. Full source CSV, measurement rows, absolute timestamps, device identifiers, source path, SHA-256 digest and proprietary code remain private.

**Publication type:** public repository evidence commit; not a separately created GitHub tagged Release.

---

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
