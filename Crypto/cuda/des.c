#include <stdint.h>
#include <limits.h>
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
    for(int i = 0;i<8;++i){
        res |= ((uint64_t)buff[i]) << (CHAR_BIT * (7-i));
    }
    return res;
}

void gen_sched(unsigned char key[8], uint64_t sched[16]) {

  uint8_t pc1[56] = {57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
                     10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
                     14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4};

  uint8_t pc2[48] = {14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
                     23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
                     41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};
  uint64_t key_int = buff_to_int(key);
  uint64_t key_perm = 0;
  for (int i = 0; i < 56; ++i) {
    key_perm <<= 1;
    if (key_int & (1ul << (64-pc1[i])))
      key_perm |= 1ul;
  }
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
    key_perm = 0;
    for (int j = 0; j < 48; ++j) {
      key_perm <<= 1;
      if (sched[i] & (1ul << (56-pc2[j])))
        key_perm |= 1ul;
    }
    sched[i] = key_perm;
  }
}
