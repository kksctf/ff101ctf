#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "SimpleHashAlgorithm.h"

#define ALLOWED_CHARS "cdefhjkmnprtvwxyCDEFHJKMNPRTVWXY1234567890_{}"
#define FLAG_FORMAT "ptctf{"

void hash_print(uint8_t *data, size_t len)
{
    for (size_t i = 0; i < len; i++)
    {
        if (i % 16 == 0)
            printf("%08lX  ", i);
        printf("%02x ", data[i]);
        if (i % 8 == 7)
            printf(" ");
        if (i % 16 == 15)
            printf("\n");
    }
    puts("");
}

int min(int x, int y)
{
    return (x < y) ? x : y;
}

int check_allowed(char *s)
{
    int check = 0;
    for (int i = 0; i < strlen(s); i++)
    {
        if (i != check)
            return 0;
        for (int a = 0; a < strlen(ALLOWED_CHARS); a++)
            if (s[i] == ALLOWED_CHARS[a])
            {
                check++;
                break;
            }
    }
    return check == strlen(s);
}

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        fprintf(stderr, "Usage: %s <salt> <flag>\n", argv[0]);
        return 1;
    }

    char *salt = argv[1];
    char flag[31] = {0};
    strncpy(flag, argv[2], 30);

    if (strlen(argv[2]) != 30)
        return 2;

    if (!check_allowed(flag))
        return 3;

    if (!check_allowed(salt))
        return 4;

    if (strncmp(flag, FLAG_FORMAT, strlen(FLAG_FORMAT)) != 0)
        return 5;

    uint8_t final_digest[20] = {0};
    for (int i = 0; i < 5; i++)
    {
        SimpleHashAlgorithm_CTX ctx;
        SimpleHashAlgorithmInit(&ctx);
        char portion[20] = {0};
        strncpy(portion, flag + i * 6, min(6, strlen(flag + i * 6)));
        strncpy(portion + min(6, strlen(flag + i * 6)), salt, min(strlen(salt), 20 - 6));
        SimpleHashAlgorithmUpdate(&ctx, (uint8_t *)portion, strlen(portion));
        uint8_t digest[20];
        SimpleHashAlgorithmFinal(digest, &ctx);
        final_digest[2 * i] = digest[0];
        final_digest[2 * i + 1] = digest[1];
        final_digest[10 + 2 * i] = digest[18];
        final_digest[10 + 2 * i + 1] = digest[19];
    }
    hash_print(final_digest, 20);

    uint8_t true_digest[20] = {0};
    SimpleHashAlgorithm_CTX ctx;
    SimpleHashAlgorithmInit(&ctx);
    SimpleHashAlgorithmUpdate(&ctx, (uint8_t *)flag, strlen(flag));
    SimpleHashAlgorithmFinal(true_digest, &ctx);

    hash_print(true_digest, 20);
}
