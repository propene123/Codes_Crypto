#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <openssl/des.h>
#include <tgmath.h>
#include <omp.h>


void print_as_hex(const DES_cblock blk) {
    for(int i=0; i<8; ++i){
        printf("0x%hhx ", blk[i]);
    }
    printf("\n");
}

int main(){
    DES_cblock in = "abcdefgh";
    const DES_cblock sec = {0xf3, 0x95, 0xb1, 0x25, 0xb6, 0xaf, 0xc6, 0x56};
    const uint64_t runs = pow(2,55) + pow(2, 30);
    uint64_t key_init = pow(2,55);
    unsigned char real_key[8] = {0x0, 0x0, 0x0, 0x0, 0x0 ,0x0 ,0x0, 0x0};

    #pragma omp parallel for
    for(uint64_t key = key_init; key < runs; ++key) {
        #pragma omp cancellation point for
        unsigned char key_bytes[8];
        memcpy(key_bytes, &key, 8);
        DES_key_schedule sched;
        DES_set_key_unchecked(&key_bytes, &sched);
        DES_cblock out;
        DES_ecb_encrypt(&in, &out, &sched, DES_ENCRYPT);
        if(!memcmp(out, sec, 8)){
            memcpy(real_key, key_bytes, 8);
            #pragma omp cancel for
        }
    }

    print_as_hex(real_key);
    
    return 0;
}
