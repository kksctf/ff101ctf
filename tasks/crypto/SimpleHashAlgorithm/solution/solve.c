#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include "SimpleHashAlgorithm.h"

#define STRLEN(s) (sizeof(s) / sizeof(s[0]) - 1)
#define FLAG_FORMAT "ptctf{"
#define FLAG_FORMAT_LEN STRLEN(FLAG_FORMAT)
#define ALPHABET "cdefhjkmnprtvwxyCDEFHJKMNPRTVWXY1234567890_{}"
#define ALPHABET_LEN STRLEN(ALPHABET)

const char *HexLookUp = "0123456789abcdef";
void hex_to_bytes(char *hexstring, uint8_t *dst, size_t dstlen)
{
    for (int i = 0; i < dstlen && 2 * i < strlen(hexstring); i++)
    {
        dst[i] = ((strchr(HexLookUp, hexstring[2 * i]) - HexLookUp) << 4) + (strchr(HexLookUp, hexstring[2 * i + 1]) - HexLookUp);
    }
}

void bytes_to_hex(uint8_t *bytes, char *dst, size_t dstlen)
{
    for (int i = 0; 2 * i < dstlen; i++)
    {
        dst[2 * i] = HexLookUp[(bytes[i] >> 4) & 0xF];
        dst[2 * i + 1] = HexLookUp[bytes[i] & 0xF];
    }
}

void generate_one_permutation(char *target, int permutation_n, char *alphabet, int alphabet_len, int permutation_len)
{
    for (int i = 0; i < permutation_len; i++)
    {
        target[i] = alphabet[permutation_n % alphabet_len];
        permutation_n /= alphabet_len;
    }
}

int check_digests(uint8_t *task_digest, uint8_t *guess_digest, int part_number)
{
    return task_digest[2 * part_number] == guess_digest[0] &&
           task_digest[2 * part_number + 1] == guess_digest[1] &&
           task_digest[10 + 2 * part_number] == guess_digest[18] &&
           task_digest[10 + 2 * part_number + 1] == guess_digest[19];
}

char *break_salt(uint8_t *task_digest)
{
    char string_to_hash[12] = {0};
    strncpy(string_to_hash, FLAG_FORMAT, FLAG_FORMAT_LEN);
    uint8_t guess_digest[20];
    for (int salt_len = 1; salt_len <= 6; salt_len++)
    {
        for (size_t i = 0; i < (size_t)pow(ALPHABET_LEN, salt_len); i++)
        {
            generate_one_permutation(string_to_hash + FLAG_FORMAT_LEN, i, ALPHABET, ALPHABET_LEN, salt_len);

            SimpleHashAlgorithm_CTX ctx;
            SimpleHashAlgorithmInit(&ctx);
            SimpleHashAlgorithmUpdate(&ctx, (uint8_t *)string_to_hash, FLAG_FORMAT_LEN + salt_len);
            SimpleHashAlgorithmFinal(guess_digest, &ctx);

            if (check_digests(task_digest, guess_digest, 0))
            {
                char *salt = calloc(salt_len + 1, 1);
                strncpy(salt, string_to_hash + FLAG_FORMAT_LEN, salt_len);
                return salt;
            }
        }
    }
    return NULL;
}

typedef struct
{
    char **possible_strings;
    size_t size;
} retval;

void *break_one_portion(uint8_t *task_digest, int part_number, char *salt, char char_from_thread)
{
    retval *r = malloc(sizeof(retval));
    r->size = 0;
    r->possible_strings = malloc(sizeof(char **));

    char guess_size = 6 + strlen(salt);
    char guess[12] = {0};
    guess[0] = char_from_thread;
    strncpy(guess + 6, salt, strlen(salt));
    uint8_t guess_digest[20] = {0};

    for (size_t i = 0; i < (size_t)pow(ALPHABET_LEN, 5); i++)
    {
        generate_one_permutation(guess + 1, i, ALPHABET, ALPHABET_LEN, 5);

        SimpleHashAlgorithm_CTX ctx;
        SimpleHashAlgorithmInit(&ctx);
        SimpleHashAlgorithmUpdate(&ctx, (uint8_t *)guess, guess_size);
        SimpleHashAlgorithmFinal(guess_digest, &ctx);

        if (check_digests(task_digest, guess_digest, part_number))
        {
            char pure_guess[7] = {0};
            strncpy(pure_guess, guess, 6);
            char hexdigest[41] = {0};
            bytes_to_hex(guess_digest, hexdigest, 40);
            printf("recovered possible %d part: %s (%s)\n", part_number, pure_guess, hexdigest);

            r->possible_strings[r->size] = malloc(7);
            strncpy(r->possible_strings[r->size], pure_guess, 7);
            r->size++;
            r->possible_strings = realloc(r->possible_strings, sizeof(char **) * (r->size + 1));
        }
    }

    return r;
}

typedef struct
{
    uint8_t *task_digest;
    int part_number;
    char *salt;
    char char_from_thread;
    retval *r;
} threadparams;

void *job(void *params)
{
    threadparams *p = (threadparams *)params;
    p->r = break_one_portion(p->task_digest, p->part_number, p->salt, p->char_from_thread);
    return NULL;
}

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        fprintf(stderr, "Usage: %s <hashstring> <truehash>\n", argv[0]);
        return -1;
    }

    uint8_t task_digest[20];
    hex_to_bytes(argv[1], task_digest, 20);

    uint8_t true_digest[20];
    hex_to_bytes(argv[2], true_digest, 20);

    char *salt = break_salt(task_digest);
    printf("salt: %s\n", salt);

    retval retvals[5] = {0};
    retvals[0].size = 1;
    retvals[0].possible_strings = malloc(1 * sizeof(char *));
    retvals[0].possible_strings[0] = calloc(7, 1);
    strcpy(retvals[0].possible_strings[0], FLAG_FORMAT);

    for (int i = 1; i < 5; i++)
    {
        pthread_t threads[ALPHABET_LEN] = {0};
        threadparams params[ALPHABET_LEN] = {0};
        for (int t = 0; t < ALPHABET_LEN; t++)
        {
            params[t].task_digest = task_digest;
            params[t].part_number = i;
            params[t].salt = salt;
            params[t].char_from_thread = ALPHABET[t];
            pthread_create(threads + t, NULL, job, params + t);
        }
        for (int t = 0; t < ALPHABET_LEN; t++)
        {
            pthread_join(threads[t], NULL);

            for (int rs = 0; rs < params[t].r->size; rs++)
            {
                retvals[i].possible_strings = realloc(retvals[i].possible_strings, sizeof(char *) * (retvals[i].size + 1));
                retvals[i].possible_strings[retvals[i].size] = params[t].r->possible_strings[rs];
                retvals[i].size++;
            }
        }
    }

    char flag[31] = {0};
    uint8_t flag_digest[20] = {0};

    // too lazy to do it fancy
    for (int a = 0; a < retvals[0].size; a++)
    {
        memcpy(flag, retvals[0].possible_strings[a], 6);
        for (int b = 0; b < retvals[1].size; b++)
        {
            memcpy(flag + 6, retvals[1].possible_strings[b], 6);
            for (int c = 0; c < retvals[2].size; c++)
            {
                memcpy(flag + 12, retvals[2].possible_strings[c], 6);
                for (int d = 0; d < retvals[3].size; d++)
                {
                    memcpy(flag + 18, retvals[3].possible_strings[d], 6);
                    for (int e = 0; e < retvals[4].size; e++)
                    {
                        memcpy(flag + 24, retvals[4].possible_strings[e], 6);

                        SimpleHashAlgorithm_CTX ctx;
                        SimpleHashAlgorithmInit(&ctx);
                        SimpleHashAlgorithmUpdate(&ctx, (uint8_t *)flag, 30);
                        SimpleHashAlgorithmFinal(flag_digest, &ctx);

                        if (!memcmp(flag_digest, true_digest, 20))
                        {
                            puts(flag);
                            return 0;
                        }
                    }
                }
            }
        }
    }

    return 0;
}
