# Measurement semantics

| Sensor signal | Meaning | Units | Caution |
| --- | --- | --- | --- |
| SCD41 CO₂ | Measured CO₂ using photoacoustic NDIR technology | ppm | Calibration and operating conditions matter |
| SCD41 T/RH | Temperature and relative humidity | °C / %RH | Enclosure/board heating may bias T |
| ENS160 TVOC | Vendor-estimated TVOC proxy | ppb, estimated | Not a laboratory compound-specific concentration |
| ENS160 eCO₂ | VOC-derived CO₂-equivalent estimate | ppm, estimated | Not true measured CO₂ |
| ENS160 AQI | Vendor's indoor air-quality categories | 1–5 | Not a government ambient AQI |
| SGP41 SRAW_VOC / SRAW_NOX | Gas-sensitive raw signals | raw output | Influenced by compensation and sensor state |
| SGP41 VOC/NOx Index | Relative, algorithmically processed gas indices | dimensionless | Never label as ppb VOC or NO₂ |

Sensor fusion means interpreting complementary signals in context, **not** claiming chemical identification from a general broadband sensor.

A simultaneous CO₂/RH rise can be consistent with occupancy, and isolated VOC index rises with independent VOC sources; these are hypotheses requiring controlled evidence.

Archived ventilation guidance is advisory, not a calibrated alarm or regulatory threshold.
