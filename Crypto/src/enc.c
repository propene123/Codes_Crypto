#include <stdio.h>
#include <openssl/des.h>

void print_as_hex(const DES_cblock blk) {
    for(int i=0; i<8; ++i){
        printf("0x%hhx ", blk[i]);
    }
    printf("\n");
}

int main() {
    DES_cblock in = "abcdefgh";
    DES_cblock out;
    DES_cblock key = {0x45, 0x21, 0x55, 0x0 ,0x0 ,0x0 ,0x0, 0x0};
    DES_key_schedule sched;
    DES_set_key_unchecked(&key, &sched);
    DES_ecb_encrypt(&in, &out, &sched, DES_ENCRYPT);

    print_as_hex(out);

    return 0;
}
