# VigilAir architecture

## Historical embedded Wi-Fi prototype

```text
SCD41 (I²C 0x62) ---> ESP32-S3 <--- ENS160 (I²C 0x53)
 true CO₂, T, RH       |             TVOC, AQI, eCO₂ estimate
              sensor polling, SCD4x CRC
                        |
           temperature/RH compensation
                        |
            volatile RAM/PSRAM history
                        |
            device Wi-Fi access point
                        |
           local HTTP JSON + dashboard
                1h / 6h / 12h / 1d
```

Recovered firmware records I²C SDA on GPIO8 and SCL on GPIO9. The archived April 2026 v3 sketch uses a 17,280-sample target (~24h at 5s) and a 4,320-sample fallback (~6h) if allocation fails. These are **memory capacity targets**, not proof of measured retention. The history is volatile. Its captive portal and default open AP were prototype configurations and need security review before deployment.

## Sensirion Pro evaluation

```text
SCD41 measured CO₂, T, RH ----+
                              +-- acquisition/compensation --> logged time series
SGP41 VOC/NOx raw signals ----+                       |
                                                  trend/event analysis
```

SCD41 periodic CO₂ and SGP41 raw measurement have different sensor cadences. Signal alignment, conditioning and sensor warm-up matter. A historical ~24-hour trace was evaluated, but complete firmware and raw log are **not published** here.

## Core engineering principles

- Direct SCD41 measured CO₂ is different from ENS160 estimated eCO₂.
- SGP41 indices are dimensionless indicators, not absolute concentration measurements.
- Compensate gas sensor measurements appropriately and record relevant sensor state.
- Avoid labeling preliminary event hypotheses as verified chemical identification.

No claim is made here that cloud SaaS, certified alarms, LTE, or secure fleet infrastructure has been implemented.
