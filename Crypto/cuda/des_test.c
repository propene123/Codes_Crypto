#include <stdio.h>
#include <stdint.h>
#include "des.h"


int main() {

    unsigned char buff[8] = {0x13, 0x34, 0x57, 0x79, 0x9B, 0xBC, 0xDF, 0xF1};
    uint64_t sched[16];
    gen_sched(buff, sched);
    unsigned char in[8] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF};
    unsigned char out[8];
    encrypt(in, out, sched);
    printf("0x");
    for(int i = 0;i<8;++i){
        printf("%x", out[i]);
    }
    printf("\n");

    return 0;
}
