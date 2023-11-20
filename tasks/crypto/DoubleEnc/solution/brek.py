from sage.all import *
from itertools import compress
from Crypto.Util.number import long_to_bytes
import base64
import json


def gen_rand_index(N, w):
    index = set()
    while len(index) < w:
        index.add(randint(0, N-1))
    return index


def gen_submatrix(M, ind):
    cols = [M.column(i) for i in ind]
    return Matrix(cols).transpose()


def Two_msg_ISD(pk, n, k, t, c_1, c_2):    
    # отсеиваем те столбцы, соттветсвующие биты для которых разичны
    mask = [(i+j)%2 == 0 for i, j in zip(c_1,c_2)]
    n_ = sum(mask)
    
    print(f"n  = {n}")
    print(f"n_ = {n_}")
    print(f"t_ = {2*t-n+n_}")
    
    PK = MatrixSpace(GF(2), k, n_)
    G = PK(matrix(list(compress(matrix(pk).columns(),mask))).transpose())
    Vn_ = VectorSpace(GF(2), n_)
    c_ = Vn_(list(compress(c_1,mask)))

    # непосредственно ISD на новом коде, с проверкой результата на старом коде
    i = 0
    while True:
        i += 1
        ind = gen_rand_index(n_,k) 
        S = gen_submatrix(G, ind)
        sub_c = vector([c_[i] for i in ind])
        if S.is_invertible():
            m_ = S.solve_left(sub_c)
            summ = sum((int(i)+j)%2 for i, j in zip(m_*matrix(pk),c_1))
            if summ == t:
                return m_
            else:
                print(f"[{i}]: summ = {summ}")
        else: 
            print(f"[{i}]: not invertible")

def main():
    with open('output.json', 'r') as fp:
        data = json.load(fp)
        [c_1, c_2] = data
    with open('pubkey.json', 'r') as fp:
        data = json.load(fp)
        [pk, n, k, t] = data

    msg = Two_msg_ISD(pk, n, k, t, c_1, c_2)

    rnd_str = int("".join(str(m) for m in msg),2)
    flag = b'ptctf{' + base64.b16encode(long_to_bytes(rnd_str)) + b'}'
    print(flag)
            

if __name__ == '__main__':
    main()