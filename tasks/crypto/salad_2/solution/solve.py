#!/usr/bin/env python

f = open('./data.enc', "rb")
flag = f.read().decode("latin-1")
f.close()

for k in range(256):
    flag_c = ""
    for ch in flag:
        n = (ord(ch) + k) % 256
        flag_c += chr(n)
    if flag_c.startswith('ptctf'):
        print(flag_c)
        break