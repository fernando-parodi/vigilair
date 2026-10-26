# Public version roadmap

| Version | Goal | Status |
| --- | --- | --- |
| v0.1.0 | Architecture, semantics, protocol excerpt and synthetic CSV examples | Published on main (no formal GitHub Release tag created) |
| v0.2 | Measurement provenance, conservative data dictionary, offline SHA-256 audit and historical evidence classifications | Completed foundation |
| **v0.2.1** | Timestamp integrity diagnostics and authorized aggregate-only evidence from locally audited real archive | **Published on main: owner-verified 17,280 rows, 17,279 unique timestamps, 5 s dominant cadence; one 11 s interval and one collision** |
| v0.3 | Reproducible diagnostics and signal-conditioning evaluation | Planned |
| v0.4 | IP-safe edge historian interface demonstration | Planned |

**Versioning:** Public GitHub milestones do not map to historical proprietary firmware version names such as VigilAir v3.2. New releases must state the evidence level and limits.

**Evidence boundary:** the private archive has been opened locally and an authorized acquisition-time aggregate is public. The old **19 candidate events** and chemical-source hypotheses are still historical, not reproducibly verified. Neither raw data nor the source checksum is public.

Full firmware, deployment configuration, private measurements and the original event-classification algorithm remain proprietary.
