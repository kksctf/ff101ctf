from sage.all import *
from Crypto.Util.number import long_to_bytes
import base64
import json


class McElieceCryptosystem(object):
    def __init__(self, pk, n, k, t):        
        self.n = n
        self.k = k
        self.t = t
        PK = MatrixSpace(GF(2), k, n)
        self.pk = PK(pk)

    def __GetErrorVector(self):
        F = GF(2)
        e = vector([F(0) for _ in range(self.n)])

        erorBitIndex = list(range(self.n))
        shuffle(erorBitIndex)
        for i in erorBitIndex[:self.t]:
            e[i] = F(1)
        return e

    def Encode(self, m):
        e = self.__GetErrorVector()
        return m * self.pk + e


def main():
    with open('pubkey.json', 'r') as fp:
        data = json.load(fp)
    [pk, n, k, t] = data

    rnd_str = getrandbits(k)
    flag = b'ptctf{' + base64.b16encode(long_to_bytes(rnd_str)) + b'}'
    print(flag)

    mc = McElieceCryptosystem(pk, n, k, t)    
    msg = vector([GF(2)(i) for i in bin(rnd_str)[2:].zfill(k)])
    c_1 = mc.Encode(msg)
    c_2 = mc.Encode(msg)

    with open('output.json', 'w') as fp:
        c_1_int = [int(c) for c in c_1]
        c_2_int = [int(c) for c in c_2]
        json.dump([c_1_int, c_2_int], fp)


if __name__ == '__main__':
    main()