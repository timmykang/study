import struct 
from Crypto.Util.number import *

f1 = open("test_key", "rb")
f2 = open("key", "rb")
key = f2.read()

f3 = open("../secret", "rb")
data = f3.read()
sbox = data[12576:22944]

qbox = []
for i in range(256):
    qbox.append(struct.unpack('<Q', data[22816+8*i:22816+8*(i+1)])[0])

def enc(key, idx):
    v5 = [0 for i in range(0x80)]
    cnt = 0
    for i in range(128):
        if sbox[128*idx+i] > 0x4F:
            v5[i] = sbox[128*idx+i]
        else:
            v5[i] = key[sbox[128*idx+i]]
            v5[i] = (i, sbox[128*idx+i])
    a = 0
    print(v5)
    for i in range(128):
        b = v5[i] ^ a
        a = (b >> 8) ^ qbox[b % 2**8]
    return a

'''
for i in range(80):
    a = f1.read(8)
    if enc(key, i) != struct.unpack('<Q', a)[0]:
        print("error")
        break
'''
enc(key, 0)
a=f1.read(8)
print(hex(struct.unpack('<Q', a)[0]))