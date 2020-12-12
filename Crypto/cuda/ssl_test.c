#include <stdio.h>
#include <openssl/des.h>

int main() {

    DES_cblock key = "abcdefgh";
    DES_key_schedule sched;
    DES_set_key_unchecked(&key, &sched);
    for(int i = 0;i<16;++i){
        printf("0x%x%x\n", sched.ks[i].deslong[0], sched.ks[i].deslong[1]);
    }

    return 0;
}
