# Validation and evidence status

All figures below are historical development observations, **not** independent laboratory certification.

## April 2026: SCD41 + ENS160 embedded prototype

- Recovered ESP32-S3 v2/v3 sketches document I²C data acquisition, SCD41 CRC checking, ENS160 T/RH compensation and local Wi-Fi HTTP dashboard.
- Historical VigilAir v3.2 dashboard capture displays 556 ppm measured CO₂, 0 ppb estimated ENS160 TVOC, 25.11 °C and 47.5% RH. It is a snapshot rather than a calibration record.
- Dashboard code supports selectable 1h, 6h, 12h and 1d trends; actual retained samples depend on RAM allocation and runtime.

## May 2026: SCD41 + SGP41 Sensirion Pro evaluation

- Historical evaluation notes report approximately **17,279 rows across ~24 hours**, nominal 5-second logging.
- Earlier exploration identified **19 candidate events** with different relative CO₂ and VOC-index behavior. This does not establish chemical sources.
- A previously reported overall CO₂–VOC correlation near **0.01** applies only to that evaluation.
- The original raw CSV, complete firmware and historical analyzer were **not available for independent reanalysis** for this public release.

## Public example checks

- C++ test validates an extracted historical SCD4x CRC function against known vectors.
- Python standard-library CSV diagnostic and unit tests use **synthetic** fixtures.
- Neither test validates a complete sensor deployment or commercial monitoring performance.

## Next evidence milestones

Record firmware hashes, reference-instrument comparison, calibration/conditioning metadata, environmental offsets, sanitized real measurements with permission, and repeatability trials.
