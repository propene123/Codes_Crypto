#include <stdio.h>
#include <openssl/des.h>
#include <stdint.h>

int main() {

    DES_cblock key = "abcdefgh";
    DES_key_schedule sched;
    DES_set_key_unchecked(&key, &sched);
    uint32_t left = sched.ks[0].deslong[0];
    uint32_t right = sched.ks[0].deslong[1];


    return 0;
}
