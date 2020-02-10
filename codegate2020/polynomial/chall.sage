#!/usr/bin/env sage
from sage.misc.banner import version_dict
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import inverse
from Padding import pad
from Crypto.Cipher import AES
from os import urandom

#assert version_dict()["major"] >= 9


class Chall:
    def __init__(self, N, p, q):
        self.N, self.p, self.q = N, p, q
        self.R = PolynomialRing(Integers(q), "x")
        self.x = self.R.gen()
        self.S = self.R.quotient(self.x ^ N - 1, "x")
        self.h, self.f = None, None

    def random(self):
        return self.S([randint(-1, 1) for _ in range(self.N)])

    def keygen(self):
        while True:
            self.F = self.random()
            self.f = self.p * self.F + 1
            try:
                self.z = self.f ^ -1
            except:
                continue
            break
        while True:
            self.g = self.random()
            try:
                self.g ^ -1
            except:
                continue
            break
        self.h = self.p * self.z * self.g
        #print(list(self.h * self.f * self.random()))

    def getPublicKey(self):
        return list(self.h)

    def getPrivateKey(self):
        return list(self.f)

    def encrypt(self, m):
        m_encoded = self.encode(b2l(m))
        e = self.random() * self.h + self.S(m_encoded)
        return list(e)

    def decrypt(self, e, privkey):
        e, privkey = self.S(e), self.S(privkey)
        temp = map(Integer, list(privkey * e))
        temp = [t - self.q if t > self.q // 2 else t for t in temp]
        temp = [t % self.p for t in temp]
        pt_encoded = [t - self.p if t > self.p // 2 else t for t in temp]
        pt = l2b(self.decode(pt_encoded))
        return pt

    def encode(self, value):
        assert 0 <= value < 3 ^ self.N
        out = []
        for _ in range(self.N):
            out.append(value % 3 - 1)
            value -= value % 3
            value /= 3
        return out

    def decode(self, value):
        out = sum([(value[i] + 1) * 3 ^ i for i in range(len(value))])
        return out

    def count(self, row):
        p = sum([e == 1 for e in row])
        n = sum([e == self.q - 1 for e in row])
        return p, len(row) - p - n, n


def wrapper(N, p, q, pt):
    chall = Chall(N, p, q)
    chall.keygen()
    print(chall.getPublicKey())
    print(chall.encrypt(pt))
    #chall.decrypt(x,chall.getPrivateKey())
    print(chall.count(list((chall.F))))
'''
if __name__ == "__main__":
    key = urandom(16)
    cipher = AES.new(key, AES.MODE_ECB)
    flag = pad(open("flag.txt", "rb").read(), 16)
    enc_flag = b2l(cipher.encrypt(flag))
    print(enc_flag)

    key1, key2 = key[:8], key[8:]

    wrapper(55, 3, 4027, key1)
    wrapper(60, 3, 1499, key2)
'''
chall1 = Chall(55,3,4027)
pub1=[3627, 1889, 3460, 2627, 3545, 1478, 2307, 3378, 3350, 1272, 2445, 3881, 3110, 1628, 1798, 1826, 259, 1983, 453, 52, 2650, 834, 3307, 907, 2762, 3452, 1085, 3059, 3544, 1136, 3767, 2346, 1952, 699, 3023, 531, 1208, 1449, 3636, 1742, 2692, 1128, 1683, 1152, 2584, 637, 3053, 2072, 2687, 1811, 2981, 3288, 2324, 3632, 1813]
enc_1 = [426, 3379, 3985, 160, 2502, 3592, 55, 1753, 3599, 2656, 2380, 582, 1038, 1028, 791, 1695, 1783, 3814, 3687, 3742, 1892, 1053, 2728, 3946, 801, 238, 3766, 1355, 1219, 528, 3560, 9, 3737, 1975, 1469, 85, 1373, 3717, 195, 3252, 2020, 1087, 201, 2536, 1655, 3380, 2322, 2438, 803, 2838, 1034, 457, 3050, 4010, 231]

chall2 = Chall(60,3,1499)
pub2 = [314, 1325, 1386, 176, 369, 1029, 877, 1255, 111, 1226, 117, 0, 210, 761, 938, 273, 525, 751, 1085, 372, 1333, 898, 780, 44, 649, 1463, 326, 354, 116, 1080, 1065, 1109, 358, 275, 1209, 964, 101, 950, 415, 1492, 1197, 921, 1000, 1028, 1400, 43, 1003, 914, 447, 360, 1171, 1109, 223, 1134, 1157, 1383, 784, 189, 870, 565]
enc_2 = [378, 753, 466, 825, 320, 658, 630, 288, 16, 576, 134, 914, 549, 489, 197, 1392, 328, 361, 1241, 50, 710, 315, 526, 1250, 977, 453, 225, 433, 1342, 1005, 1432, 143, 1326, 1426, 1251, 1397, 237, 1202, 555, 83, 994, 446, 1406, 356, 1127, 1469, 485, 1034, 1224, 230, 1445, 825, 630, 1158, 815, 807, 837, 747, 423, 184]
tmp = list(((chall1.S(pub1) ^ -1) * 3) ^ -1) #g/f
tmp1 = list(((chall2.S(pub2) ^ -1) * 3) ^ -1) #g/f

def shifting(x):
    tmp = x[len(x)-1]
    for i in range(len(x)-1, 0, -1):
        x[i] = x[i-1]
    x[0] = tmp

M = matrix(110)
M1 = matrix(120)

for i in range(55):
    M[i,i] = 4027
for i in range(55,110):
    M[i,i] = 1
    for j in range(55):
        M[i,j] = tmp[j]
    shifting(tmp)
M = M.LLL()
f_1 = list(M[0][55:])

for i in range(55):
    f_1[i] = -f_1[i]

for i in range(55-f_1.index(-2)):
    shifting(f_1)

for i in range(60):
    M1[i,i] = 1499
for i in range(60,120):
    M1[i,i] = 1
    for j in range(60):
        M1[i,j] = tmp1[j]
    shifting(tmp1)
M1 = M1.LLL()

f_2 = list(M1[0][60:])

for i in range(60-f_2.index(-2)):
    shifting(f_2)

print(f_2)


encflag = l2b(2960408776014513590203667205130185225161547470030516261741102417822093600856513664346223496713014612247754765985505434047965417819771431223015026059243409921418043319365743779292681722097463141)
key1 = chall1.decrypt(enc_1, f_1)
key2 = chall2.decrypt(enc_2, f_2)
key = key1 + key2
cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(encflag))
#CODEGATE2020{86f94100f760b45e9c0f6925f5b474b24387ff6be5732ab88d74b4bfbff35951}

