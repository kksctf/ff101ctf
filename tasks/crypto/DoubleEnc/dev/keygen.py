from sage.all import *
import json

k = 128
m = 16
t = 96
n = m*t+k

PK = MatrixSpace(GF(2), k, n)
pk = PK.random_element()

with open('pubkey.json', 'w') as fp:
    pk_list = [[int(g) for g in row] for row in list(pk)]
    json.dump([pk_list, n, k, t], fp)