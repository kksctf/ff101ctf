#!/usr/bin/env python

flag = r"ptctf{d0_y0u_pr3f3r_ch1ck3n_0r_shr1mps}"
shift = 23
flag_enc = ''
filename = "./data.enc"
f = open(filename, "wb")

for ch in flag:
    n = (ord(ch) + shift) % 256
    flag_enc += chr(n)

for ch in flag_enc:
    print(ch, end='')
print()

for ch in flag_enc:
    print(hex(ord(ch))[2:], end=' ')
print()

f.write(flag_enc.encode("latin-1"))
print(f"{filename} created")
f.close()