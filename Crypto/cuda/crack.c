#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <tgmath.h>
#include <omp.h>
#include "../cuda/des.h"


void print_as_hex(const unsigned char blk[8]) {
    for(int i=0; i<8; ++i){
        printf("0x%hhx ", blk[i]);
    }
    printf("\n");
}

int main(){
    unsigned char in[8] = {0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8};
    const unsigned char sec[8] = {0x2a, 0x40, 0x72, 0x0b, 0xb5, 0x6d, 0x15, 0xd6};
    const uint64_t runs = pow(2, 25);
    uint64_t key_init = 0;

    
    unsigned char real_key[8] = {0x0, 0x0, 0x0, 0x0, 0x0 ,0x0 ,0x0, 0x0};

    #pragma omp target teams distribute parallel for map(to:in[:8])
    for(uint64_t key = key_init; key < runs; ++key) {
        unsigned char key_bytes[8];
        memcpy(key_bytes, &key, 8);
        uint64_t sched[16];
        gen_sched(key_bytes, sched);
        unsigned char out[8];
        encrypt(in, out, sched);
    }

    print_as_hex(real_key);
    
    return 0;
}
