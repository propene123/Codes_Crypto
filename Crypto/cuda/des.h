#ifndef DES_H
#define DES_H
#include <stdint.h>

void gen_sched(unsigned char key[8], uint64_t sched[16]);
void encrypt(const unsigned char in[8], unsigned char out[8], const uint64_t sched[16]);

#endif 
