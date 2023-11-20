#!/usr/bin/env python3

import socket

addr = ('127.0.0.1', 7000)
s = socket.socket()
s.connect(addr)
data = ''
while True:
    problem = s.recv(8*1024*1024).decode().strip()
    print(problem, flush=True)
    answer = (str(eval(problem)) + "\n").encode()
    s.send(answer)
    result = s.recv(8*1024*1024)
    print(result, flush=True)
    if b"ptctf" in result:
        break

s.close()
