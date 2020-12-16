#include "tables.h"
#include <limits.h>
#include <stdint.h>
#include <stdio.h>



static uint32_t lrot32(uint32_t in, uint8_t n) {
    uint32_t ret = (in << n) | (in >> (28 - n));
    return (ret & 0x0fffffff);
}

static uint64_t cat28(const uint32_t left, const uint32_t right) {
    return (((uint64_t)left) << 28) | ((uint64_t)right);
}

static uint64_t cat32(const uint32_t left, const uint32_t right) {
    return (((uint64_t)left) << 32) | ((uint64_t)right);
}

uint64_t buff_to_int(const unsigned char buff[8]) {
    uint64_t res = 0;
    for (int i = 0; i < 8; ++i) {
        res |= ((uint64_t)buff[i]) << (CHAR_BIT * (7 - i));
    }
    return res;
}

static void int_to_buff(const uint64_t in, unsigned char out[8]) {
    for (int i = 0; i < 8; ++i) {
        out[i] = (unsigned char)((in >> (CHAR_BIT * (7 - i))) & 0xff);
    }
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

static uint32_t read_s_block(const uint8_t in, const uint8_t s_block[4][16],
                             const int id) {
    const uint8_t row = (in & 1) | ((in & 0x20) >> 4);
    const uint8_t col = (in & 0x1e) >> 1;
    return ((uint32_t)s_block[row][col]) << (4 * (8 - id));
}

static uint8_t get_mini_block(const uint64_t in, const int id) {
    return ((in >> (6 * (8 - id))) & 0x3f);
}

static uint32_t feistel(const uint32_t in, const uint64_t key) {
    uint64_t expanded = perm(in, 32, expand, 48);
    expanded ^= key;
    uint32_t res = read_s_block(get_mini_block(expanded, 1), s1, 1) |
                   read_s_block(get_mini_block(expanded, 2), s2, 2) |
                   read_s_block(get_mini_block(expanded, 3), s3, 3) |
                   read_s_block(get_mini_block(expanded, 4), s4, 4) |
                   read_s_block(get_mini_block(expanded, 5), s5, 5) |
                   read_s_block(get_mini_block(expanded, 6), s6, 6) |
                   read_s_block(get_mini_block(expanded, 7), s7, 7) |
                   read_s_block(get_mini_block(expanded, 8), s8, 8);
    return ((uint32_t)perm(res, 32, fp, 32));
}

void gen_sched(unsigned char key[8], uint64_t sched[16]) {

    uint64_t key_int = buff_to_int(key);
    uint64_t key_perm = perm(key_int, 64, pc1, 56);
    uint32_t key_left = key_perm >> 28;
    uint32_t key_right = 0x000000000fffffff & key_perm;
    uint32_t c = lrot32(key_left, 1);
    uint32_t d = lrot32(key_right, 1);
    sched[0] = cat28(c, d);
    for (int i = 0; i < 15; ++i) {
        if (i % 7 == 0) {
            c = lrot32(c, 1);
            d = lrot32(d, 1);
            sched[i + 1] = cat28(c, d);
        } else {
            c = lrot32(c, 2);
            d = lrot32(d, 2);
            sched[i + 1] = cat28(c, d);
        }
    }
    for (int i = 0; i < 16; ++i) {
        key_perm = perm(sched[i], 56, pc2, 48);
        sched[i] = key_perm;
    }
}

void encrypt(const unsigned char in[8], unsigned char out[8],
             const uint64_t sched[16]) {
    uint64_t in_int = buff_to_int(in);
    uint64_t in_perm = perm(in_int, 64, ip, 64);
    uint32_t left_prev = in_perm >> 32;
    uint32_t right_prev = in_perm & 0xffffffff;
    uint32_t left = 0;
    uint32_t right = 0;
    for (int i = 0; i < 16; ++i) {
        left = right_prev;
        right = left_prev ^ feistel(right_prev, sched[i]);
        left_prev = left;
        right_prev = right;
    }
    uint64_t out_int = cat32(right, left);
    out_int = perm(out_int, 64, ip1, 64);
    int_to_buff(out_int, out);
}

