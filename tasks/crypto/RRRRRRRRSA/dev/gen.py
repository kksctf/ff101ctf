#!/usr/bin/env python3

from secret import flag

from gmpy2 import next_prime, invert, mpz
from random import randint


def gen_prime() -> mpz:
    return next_prime(randint(2**31, 2**32))


primes: list[mpz] = list([gen_prime() for _ in range(32)])

phi: mpz = 1
N: mpz = 1

for p in primes:
    phi *= p - 1
    N *= p

e: mpz = 3
while True:
    try:
        d = invert(e, phi)
        break
    except ZeroDivisionError:
        e = next_prime(e)


ct: mpz = pow(flag, e, N)
pt: mpz = pow(ct, d, N)

assert flag == pt

print(f'{e = }\n{N = }\n{ct = }')
