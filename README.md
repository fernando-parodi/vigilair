# VigilAir

**Indoor air quality sensing · embedded monitoring · environmental data analysis**

VigilAir is an independently developed, evolving sensor-fusion project exploring how reliable CO₂ measurements and complementary gas-sensor signals can support meaningful indoor-air decisions. The work spans sensor integration, embedded firmware, environmental compensation, web dashboards and analysis of measurement histories.

![VigilAir — air quality engineering overview](assets/vigilair-architecture.svg)

> The architecture illustration is schematic. The historical dashboard capture (VigilAir v3.2, SCD41 + ENS160) is available in the accompanying [public starter package](https://github.com/fernando-parodi/vigilair) for later binary upload. The image is **not** evidence of a released Sensirion SGP41 product.

## Current milestone: v0.2.1 — Verified acquisition timing aggregate

An **owner-approved, aggregate-only audit** of the historical Sensirion Pro recording has now been [published as v0.2.1 evidence](evidence/verified/sensirion-pro-acquisition-timing-v0.2.1.md). The locally audited archive contains **17,280 stored rows**, **17,279 unique timestamps**, a **23:59:56** observed span, and **17,277 five-second intervals** plus one **11-second** interval and one equal-time pair. No backward timestamp steps or uptime-counter decreases were observed. The equal-time pair contains different sensor-field readings and is separated by **2,317 ms** of uptime.

These are verified **recording-structure** results from owner-run local tools; raw measurements, original timestamps, device identifiers, full source path and source SHA-256 have not been published. They do **not** establish chemical identity, sensor calibration, missing-sample count, uninterrupted capture, or independently reproduce the historical 19 event classifications.

## Previous milestone: v0.2 — Measurement Transparency

The **v0.2 public evidence framework** is available, with [measurement provenance and evidence tiers](docs/measurement-transparency-v0.2.md), a [May 2026 historical analysis record](docs/historical-sensirion-pro-2026-05.md), a [measurement dictionary](docs/measurement-data-dictionary.md), and an [offline SHA-256/CSV audit tool](scripts/public_measurement_audit.py).

**Evidence status:** the original private CSV was read and analyzed locally by its owner; the resulting approved timing aggregates have been published. The historical **19 candidate-event interpretations remain unverified**, and no source CSV rows or sensitive capture metadata have been uploaded.

To generate a local, privacy-reduced report, follow the [Windows export procedure](docs/public-export-protocol.md). The export does not upload or publish any data automatically.

## Two developed configurations

| Track | Sensors | Measurement meaning | Available development evidence |
| --- | --- | --- | --- |
| Embedded Wi-Fi prototype | Sensirion **SCD41** + ScioSense **ENS160** | Measured CO₂ (ppm), SCD41 temperature/RH, ENS160 estimated TVOC (ppb) and vendor AQI category | Recovered ESP32-S3 v2/v3 firmware, AP dashboard with local trend plots, CRC-checked SCD41 packets |
| **Sensirion Pro** evaluation | Sensirion **SCD41** + **SGP41** | Measured CO₂ (ppm); temperature/RH; SGP41 raw VOC/NOx signals and relative VOC/NOx indices | Owner-audited 17,280-row, 23:59:56 acquisition record with 17,279 distinct timestamps; historical exploratory events remain unverified |

**SGP41 VOC/NOx Index is not gas concentration in ppb; ENS160 eCO₂ is not a direct CO₂ measurement.** See [measurement semantics](docs/measurement-semantics.md).

## Contents of this public portfolio edition

- An overview of the sensor architecture, separated by proven development tracks.
- A real historical **SCD4x CRC-8 routine**, extracted from the older ESP32 dashboard firmware and isolated with a host-compiled regression test.
- A dependency-free **public CSV diagnostics example** and **explicitly synthetic** test data. This is not the private production analytics system.
- Historical validation notes, with evidence limitations stated clearly.
- A milestone-based roadmap.

Full embedded firmware, production device configuration, proprietary alarm or decision logic, private measurement archives, infrastructure, and other commercial implementation details are **not included**.

## Explore the engineering

| Document | Focus |
| --- | --- |
| [Architecture](docs/architecture.md) | Dual-sensor embedded device, local dashboard, Sensirion Pro historian concept |
| [Measurement semantics](docs/measurement-semantics.md) | Distinguishing measured CO₂, eCO₂, estimated TVOC and VOC/NOx index |
| [Verified timing audit](evidence/verified/sensirion-pro-acquisition-timing-v0.2.1.md) | Owner-approved recording counts and timestamp anomalies, with provenance |\n| [Validation notes](docs/validation.md) | Historical observations, datasets and evidence limits |
| [Public roadmap](docs/roadmap.md) | Version-by-version development |
| [Runnable code examples](examples/README.md) | CRC test and CSV diagnostics |

## Run the public examples

C++ CRC-8 regression test (standard compiler):

```bash
g++ -std=c++17 -Wall -Wextra -Werror -pedantic examples/test_scd4x_crc8.cpp -o /tmp/vigilair_crc_test
/tmp/vigilair_crc_test
```

CSV diagnostics (Python 3.9+ standard library):

```bash
python3 examples/analysis/csv_report.py examples/analysis/sample_synthetic.csv
python3 -m unittest discover -s tests -v
```

The bundled CSV is **synthetic**; it is not a recorded observation from VigilAir hardware.

## Boundaries and safety

This is a research-and-engineering portfolio, **not** a certified indoor-air-quality instrument, life-safety alarm, occupational exposure measurement system, or substitute for calibrated reference equipment. Do not rely on these examples for emergency detection or safety-critical control.

## Author and rights

**Fernando Parodi** · [GitHub](https://github.com/fernando-parodi)

Published as a technical portfolio and educational reference. No open-source license is granted unless explicitly stated; **all rights reserved**. No rights to the unpublished device firmware or commercial implementation are granted. Contact the author for permission to reuse or collaborate.

Public repository release numbers (starting with **v0.1.0**) are distinct from historical internal firmware names such as **VigilAir v3.2**.
