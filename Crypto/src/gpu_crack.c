#include <stdio.h>
#include <openssl/des.h>
#include <string.h>
#include <stdint.h>
#include <tgmath.h>
#include <omp.h>


void print_as_hex(const DES_cblock blk) {
    for(int i=0; i<8; ++i){
        printf("0x%hhx ", blk[i]);
    }
    printf("\n");
}

int main(){
    DES_cblock in = {0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8};
    const DES_cblock sec = {0x2a, 0x40, 0x72, 0x0b, 0xb5, 0x6d, 0x15, 0xd6};
    const uint64_t runs = pow(2, 55);
    uint64_t key_init = runs - pow(2, 30);

    
    DES_cblock real_key = {0x0, 0x0, 0x0, 0x0, 0x0 ,0x0 ,0x0, 0x0};

    #pragma omp target teams distribute parallel for
    for(uint64_t key = key_init; key < runs; ++key) {
        #pragma omp cancellation point for
        DES_cblock key_bytes;
        memcpy(key_bytes, &key, 8);
        DES_key_schedule sched;
        DES_set_key_unchecked(&key_bytes, &sched);
        DES_cblock out;
        DES_ecb_encrypt(&in, &out, &sched, DES_ENCRYPT);
        if(!memcmp(out, sec, 8)) {
            memcpy(real_key, key_bytes, 8);
            #pragma omp cancel for
        }
    }

    print_as_hex(real_key);
    
    return 0;
}
