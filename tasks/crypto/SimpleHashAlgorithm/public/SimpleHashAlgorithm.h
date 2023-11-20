typedef struct
{
    u_int32_t state[5];
    u_int32_t count[2];
    unsigned char buffer[64];
} SimpleHashAlgorithm_CTX;

void SimpleHashAlgorithmTransform(u_int32_t state[5], const unsigned char buffer[64]);
void SimpleHashAlgorithmInit(SimpleHashAlgorithm_CTX *context);
void SimpleHashAlgorithmUpdate(SimpleHashAlgorithm_CTX *context, const unsigned char *data, u_int32_t len);
void SimpleHashAlgorithmFinal(unsigned char digest[20], SimpleHashAlgorithm_CTX *context);
