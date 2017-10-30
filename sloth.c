/*
project: trx
author: benjamin wesolowski
*/
#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/bio.h>

#include "gmp.h"

/* #include "sloth.h" */

void next_prime(mpz_t p, const mpz_t n) {
    if (mpz_even_p(n)) mpz_add_ui(p,n,1);
    else mpz_add_ui(p,n,2);
    while (!mpz_probab_prime_p(p, 25)) mpz_add_ui(p,p,2);
}

void prev_prime(mpz_t p, const mpz_t n) {
    if (mpz_even_p(n)) mpz_sub_ui(p,n,1);
    else mpz_sub_ui(p,n,2);
    while (!mpz_probab_prime_p(p, 25)) mpz_sub_ui(p,p,2);
}

// the sqrt permutation as specified in the paper (returns a sqrt of either input or -input)
void sqrt_permutation(mpz_t result, const mpz_t input, const mpz_t p, const mpz_t e) {
	mpz_t tmp;
	mpz_init(tmp);
	if (mpz_jacobi(input, p) == 1) {
		mpz_powm(tmp, input, e, p);
		if (mpz_even_p(tmp)) mpz_set(result, tmp);
		else mpz_sub(result, p, tmp);
	}
	else {
		mpz_sub(tmp, p, input);
        mpz_powm(tmp, tmp, e, p);
		if (mpz_odd_p(tmp)) mpz_set(result, tmp);
		else mpz_sub(result, p, tmp);
	}

	mpz_clear(tmp);
}

// inverse of sqrt_permutation, so basicaly computes squares
void invert_sqrt(mpz_t result, const mpz_t input, const mpz_t p) {
	mpz_t tmp;
	mpz_init(tmp);
	if (mpz_even_p(input)) {
		mpz_mul(tmp, input, input);
		mpz_mod(result, tmp, p);
	}
	else {
		mpz_mul(tmp, input, input);
		mpz_mod(tmp, tmp, p);
		mpz_sub(result, p, tmp);
	}

	mpz_clear(tmp);
}

// computes input1 ^ flip ^ flip ^ ... ^ flip for the minimal number of "^ flip" (at least 1, at most 2) such
// that the result is smaller than mod
void xor_mod(mpz_t result, const mpz_t input1, const mpz_t flip, const mpz_t mod) {
    mpz_xor(result,input1,flip);
    while (mpz_cmp(result, mod) >= 0 || mpz_cmp_ui(result, 0) == 0) {
        mpz_xor(result,result,flip);
    }
}

// SHA512
int sloth_digest(char outputBuffer[], const char *string)
{

    EVP_MD_CTX *mdctx;
    const EVP_MD *md;
    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int md_len;

    OpenSSL_add_all_digests();

    md = EVP_get_digestbyname("SHA512");
    if(!md) {
        printf("Unknown message digest SHA512");
        return 1;
    }

    mdctx = EVP_MD_CTX_create();

    EVP_DigestInit_ex(mdctx, md, NULL);
    EVP_DigestUpdate(mdctx, string, strlen(string));
    EVP_DigestFinal_ex(mdctx, hash, &md_len);
    EVP_MD_CTX_destroy(mdctx);

    int i;
    for (i = 0; i < md_len; i++) {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }

    outputBuffer[i * 2] = '\0';

    return 0;
}

// generates the prime (of bit length "bits"), and the initial value in the field from the data "string"
// bits must be a multiple of 512
void sloth_preprocessing(mpz_t p, mpz_t seed, const char string[], int bits) {
    char str[strlen(string) + 8];

    // find the prime
    int nbr_blocks = bits / 512;
    char hexa[bits/4 + 1]; // number of hexadecimal charater + 1

    for (int i = 0; i < nbr_blocks; ++i) {
        sprintf(str, "%s%s%c", string, "prime", (char)('0' + i));
        sloth_digest(hexa + (128 * i), str);
    }

    mpz_t tmp;
    mpz_init(tmp);

    mpz_set_str(p, hexa, 16);

    if (!mpz_tstbit(p,bits - 1)) mpz_combit(p, bits - 1);

    do next_prime(p,p);
    while (mpz_mod_ui(tmp, p, 4) != 3);

    // find the seed
    for (int i = 0; i < nbr_blocks; ++i) {
        sprintf(str, "%s%s%c", string, "seed", (char)('0' + i));
        sloth_digest(hexa + (128 * i), str);
    }

    mpz_set_str(seed, hexa, 16);
    mpz_mod(seed, seed, p);

    mpz_clear(tmp);
}

// computes witness = the sloth witness, for the given seed, number of iterations and prime p
void sloth_core(mpz_t witness, const mpz_t seed, int iterations, const mpz_t p) {
    mpz_t a, ones, e;
    mpz_init_set(a, seed);

    mpz_init_set_ui(ones, 1);
    mpz_mul_2exp(ones, ones, mpz_sizeinbase(p,2) >> 1); // flip half the bits (least significant)
    mpz_sub_ui(ones, ones, 1);

    // compute the exponent for sqrt extraction

    mpz_init_set(e, p);
    mpz_add_ui(e, e, 1);
    mpz_tdiv_q_ui(e, e, 4);

    for (int i = 0; i < iterations; ++i) {
        //permutation(a, a);
        xor_mod(a,a,ones,p);
        sqrt_permutation(a, a, p, e);
    }

    mpz_set(witness, a);

    mpz_clear(a);
    mpz_clear(ones);
}

// computes witness = the sloth witness, for the given seed, number of iterations and prime p
void sloth(char witness[], char outputBuffer[], char string[], int bits, int iterations) {
    mpz_t p, seed_mpz, witness_mpz;
    mpz_init(p);
    mpz_init(seed_mpz);
    mpz_init(witness_mpz);
    sloth_preprocessing(p,seed_mpz,string,bits);

    sloth_core(witness_mpz, seed_mpz, iterations, p);
    mpz_get_str(witness, 16, witness_mpz);

    sloth_digest(outputBuffer, witness);

    mpz_clear(p);
    mpz_clear(seed_mpz);
    mpz_clear(witness_mpz);
}

// checks if the given witness indeed corresponds to the given seed, number of iterations and prime number
int sloth_verification_core(const char witness[], const mpz_t seed, int iterations, const mpz_t p) {
    mpz_t a, ones;
    mpz_init(a);
    mpz_set_str(a, witness, 16);

    mpz_init_set_ui(ones, 1);
    mpz_mul_2exp(ones, ones, mpz_sizeinbase(p,2) >> 1);
    mpz_sub_ui(ones, ones, 1);

    for (int i = 0; i < iterations; ++i) {
        invert_sqrt(a, a, p);
        //invert_permutation(a, a);
        xor_mod(a,a,ones,p);
    }

    int verif = (mpz_cmp(seed, a) == 0); // true if seed == a
    mpz_clear(a);
    mpz_clear(ones);

    return verif;
}

// computes witness = the sloth witness, for the given seed, number of iterations and prime p
int sloth_verification(const char witness[], const char final_hash[], const char input_string[], int bits, int iterations) {
    mpz_t p, seed_mpz;
    mpz_init(p);
    mpz_init(seed_mpz);

    sloth_preprocessing(p,seed_mpz,input_string,bits);

    return sloth_verification_core(witness, seed_mpz, iterations, p);
}
