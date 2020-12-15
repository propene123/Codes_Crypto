#include <stdio.h>
#include <openssl/des.h>
#include <stdint.h>

int main() {

    DES_cblock key = {0x13, 0x34, 0x57, 0x79, 0x9B, 0xBC, 0xDF, 0xF1};
    DES_key_schedule sched;
    DES_set_key_unchecked(&key, &sched);
    DES_cblock out;
    DES_cblock in = "abcdefgh";
    DES_ecb_encrypt(&in, &out, &sched, DES_ENCRYPT);

    printf("0x");
    for(int i = 0;i<8;++i){
        printf("%x", out[i]);
    }
    printf("\n");


    return 0;
}
