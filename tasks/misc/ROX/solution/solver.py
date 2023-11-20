import re
import ast
import time
from pwn import remote, xor

first_re = re.compile(r"BOB_1: (.+)\n\n")
second_re = re.compile(r"BOB_2: (.+)\n\n")

r = remote('127.0.0.1', 2802)
r.recv()
for i in range(100):
    data = (r.recvuntil(b'>>>')).decode("utf-8")

    xx = first_re.findall(data)
    yy = second_re.findall(data)

    print(i)
    if xx and yy:
        normalized_bytes_x = ast.literal_eval(xx[0])
        normalized_bytes_y = ast.literal_eval(yy[0])

        xored = xor(normalized_bytes_x, normalized_bytes_y)
        r.send(xored + b"\n")

#  gettin' flaaag
time.sleep(5)
data = (r.recvall()).decode("utf-8")
print(data)
