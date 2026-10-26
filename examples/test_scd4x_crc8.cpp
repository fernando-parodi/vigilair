#include "scd4x_crc8.h"
#include <cassert>
#include <cstdint>
#include <iostream>

int main() {
  const uint8_t word[2] = {0xBE, 0xEF};
  assert(scd4xCRC8(word, 2) == 0x92);
  const uint8_t zeros[2] = {0x00, 0x00};
  assert(scd4xCRC8(zeros, 2) == 0x81);
  std::cout << "SCD4x CRC-8 vectors passed.\n";
  return 0;
}
