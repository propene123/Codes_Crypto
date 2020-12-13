#include <limits.h>
#include <stdint.h>
#include <stdio.h>

static uint32_t lrot32(uint32_t in, uint8_t n) {
  uint32_t ret = (in << n) | (in >> (28 - n));
  return (ret & 0x0fffffff);
}

static uint64_t cat32(uint32_t left, uint32_t right) {
  return (((uint64_t)left) << 28) | ((uint64_t)right);
}

static uint64_t buff_to_int(unsigned char buff[8]) {

  uint64_t res = 0;
  for (int i = 0; i < 8; ++i) {
    res |= ((uint64_t)buff[i]) << (CHAR_BIT * (7 - i));
  }
  return res;
}

static uint64_t perm(const uint64_t in, const size_t in_length,
                     const uint8_t *table, const size_t out_length) {
  uint64_t out = 0;
  for (size_t i = 0; i < out_length; ++i) {
    out <<= 1ul;
    if (in & (1ul << (in_length - table[i])))
      out |= 1ul;
  }
  return out;
}

void gen_sched(unsigned char key[8], uint64_t sched[16]) {

  const uint8_t pc1[56] = {57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34,
                           26, 18, 10, 2,  59, 51, 43, 35, 27, 19, 11, 3,
                           60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7,
                           62, 54, 46, 38, 30, 22, 14, 6,  61, 53, 45, 37,
                           29, 21, 13, 5,  28, 20, 12, 4};

  const uint8_t pc2[48] = {14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
                           23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
                           41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                           44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};
  uint64_t key_int = buff_to_int(key);
  uint64_t key_perm = perm(key_int, 64, pc1, 56);
  uint32_t key_left = key_perm >> 28;
  uint32_t key_right = 0x000000000fffffff & key_perm;
  uint32_t c = lrot32(key_left, 1);
  uint32_t d = lrot32(key_right, 1);
  sched[0] = cat32(c, d);
  for (int i = 0; i < 15; ++i) {
    if (i % 7 == 0) {
      c = lrot32(c, 1);
      d = lrot32(d, 1);
      sched[i + 1] = cat32(c, d);
    } else {
      c = lrot32(c, 2);
      d = lrot32(d, 2);
      sched[i + 1] = cat32(c, d);
    }
  }
  for (int i = 0; i < 16; ++i) {
    key_perm = perm(sched[i], 56, pc2, 48);
    sched[i] = key_perm;
  }
}

static const uint8_t ip[64] = {
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7};

void encrypt(unsigned char in[8], unsigned char out[8], uint64_t sched[16]) {
  uint64_t in_int = buff_to_int(in);
  uint64_t in_perm = perm(in_int, 64, ip, 64);
  uint32_t left = in_perm >> 32;
  uint32_t right = in_perm & 0xffffffff;
}
