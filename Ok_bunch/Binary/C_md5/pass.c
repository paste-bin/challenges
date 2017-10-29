#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#if defined(__APPLE__)
#  define COMMON_DIGEST_FOR_OPENSSL
#  include <CommonCrypto/CommonDigest.h>
#  define SHA1 CC_SHA1
#else
#  include <openssl/md5.h>
#endif



char *str2md5(const char *str, int length) {
    int n;
    MD5_CTX c;
    unsigned char digest[16];
    char *out = (char*)malloc(33);

    MD5_Init(&c);

    while (length > 0) {
        if (length > 512) {
            MD5_Update(&c, str, 512);
        } else {
            MD5_Update(&c, str, length);
        }
        length -= 512;
        str += 512;
    }

    MD5_Final(digest, &c);

    for (n = 0; n < 16; ++n) {
        snprintf(&(out[n*2]), 16*2, "%02x", (unsigned int)digest[n]);
    }

    return out;
}
int main(int argc, char **argv) {
    char input[100];
    printf("Enter the password:");
    scanf("%99s",input);
    char *input_hash = str2md5(input,strlen(input));
    char *real_hash = "ac87b4cce0403805138751f3d14d6f33";
    if (strncmp(input_hash, real_hash, strlen(real_hash)) == 0){
        printf("Congradulations! The flag is COMP3441{%s}\n", input);
    } else {
        printf("Nope\n");
    }
    free(input_hash);
    return 0;
}
