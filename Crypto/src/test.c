#include <stdio.h>
#include <stdint.h>
#include "../cuda/des.h"

int main(){

    unsigned char key[8] = {0x11, 0xf, 0x45, 0xf2, 0, 0, 0, 0};
    unsigned char in[8] = "abcdefgh";
    unsigned char out[8];
    uint64_t sched[16];
    gen_sched(key, sched);

    encrypt(in, out, sched);

    printf("0x");
    for(int i = 0;i < 8; ++i) {
        printf("%x", out[i]);
    }
    printf("\n");



    return 0;
}
