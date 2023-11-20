#!/usr/bin/env python3

import hashlib
import sys
import itertools
import binascii

ALPHABET = "cdefhjkmnprtvwxyCDEFHJKMNPRTVWXY1234567890_{}"
FLAG_FORMAT = b"ptctf{"

task_digest = binascii.unhexlify(sys.argv[1])
true_digest = binascii.unhexlify(sys.argv[2])


def check_digest(task_digest: bytes, guess_digest: bytes, part_number: int) -> bool:
    shift = part_number * 2
    return (
        task_digest[shift : shift + 2] == guess_digest[0:2]
        and task_digest[shift + 10 : shift + 12] == guess_digest[-2:]
    )


def break_salt(task_digest: bytes) -> bytes:
    for salt_len in range(6):
        for x in itertools.product(ALPHABET, repeat=salt_len):
            guess = "".join(x).encode()
            if check_digest(task_digest, hashlib.sha1(FLAG_FORMAT + guess).digest(), 0):
                print(f"salt: {guess.decode()}")
                return guess
    return b""


def break_portion(task_digest: bytes, part_number: int, salt: bytes) -> list[bytes]:
    ret: list[bytes] = []
    for x in itertools.product(ALPHABET, repeat=6):
        guess = "".join(x).encode() + salt
        if check_digest(task_digest, hashlib.sha1(guess).digest(), part_number):
            print(f"recovered possible {part_number} part: {guess[:6].decode()} ({hashlib.sha1(guess).hexdigest()})")
            ret.append(guess[:6])
    return ret


salt = break_salt(task_digest)
variants = [break_portion(task_digest, part_number, salt) for part_number in range(1, 5)]
variants.insert(0, [FLAG_FORMAT])

for i in itertools.product(*variants):
    if hashlib.sha1(b"".join(i)).digest() == true_digest:
        print(b"".join(i).decode())
        exit(0)
