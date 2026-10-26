#pragma once
#include <cstdint>

// Extracted from historical VigilAir v3 SCD41 reader.
// Sensirion CRC-8: initial 0xFF, polynomial 0x31, no final XOR.
inline uint8_t scd4xCRC8(const uint8_t* data, int len) {
  uint8_t crc = 0xFF;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];
    for (int b = 0; b < 8; b++) {
      crc = (crc & 0x80) ? (uint8_t)((crc << 1) ^ 0x31) : (uint8_t)(crc << 1);
    }
  }
  return crc;
}
