# Measurement data dictionary

The public audit tool uses **conservative aliases** and does not assume the original CSV headers are known. Its reported `found_measurement_fields` maps recognized original column names to normalized signal classes. A source column can be absent, unknown, or malformed; none is silently replaced by a different sensor.

| Public key | Physical meaning | Unit/scale | Do not confuse with |
| --- | --- | --- | --- |
| `co2_ppm` | SCD41 measured CO₂ | ppm | ENS160 eCO₂, a VOC-based estimate |
| `voc_index` | SGP41 algorithmic relative VOC Index | dimensionless, nominal 1–500 | TVOC ppb or lab concentration |
| `nox_index` | SGP41 relative NOx Index | dimensionless, nominal 1–500 | NO₂ concentration |
| `temperature_c` | Reported temperature, possibly corrected | °C | Independent air temperature unless calibrated |
| `rh_pct` | Reported relative humidity | % | Sensor-independent calibrated RH |
| `sraw_voc` | SGP41 raw VOC-sensitive signal | device raw signal | VOC Index or concentration |
| `sraw_nox` | SGP41 raw NOx-sensitive signal | device raw signal | NOx Index or concentration |

**Excluded from automatic normalization:** any `eco2` column; derived `tvoc_reset_um3` / `tvoc_well_ugm3` engineering indicators; device ID, IP and location; unknown columns. Those require separate explicit semantic review rather than guessing units.

Timestamp recognition: ISO-8601 with timezone (including `Z`), or Unix epoch seconds/milliseconds in recognized timestamp columns. Timezone-naive strings are not used to validate cadence. Only elapsed duration and aggregate cadence are exported, never absolute dates.

The audit deliberately reports **field coverage and basic descriptive statistics**, not clinical, occupational or regulatory air safety judgments.

## Original source field labels (identified in v0.2.1)

The current CSV header includes `ts_utc`, `co2_ppm`, `scd41_temp_c`, `scd41_rh_pct`, `sraw_voc`, `sraw_nox`, `voc_index` and `nox_index`. The audit recognizes these fields without publishing any raw timestamp, device identifier, Wi-Fi metadata or original measurement row.

Its diagnostics distinguish **source row order** from interval estimates derived by sorting unique timestamps. A sorted interval is useful for assessing recording patterns, but cannot prove an uninterrupted sensor-acquisition stream.
