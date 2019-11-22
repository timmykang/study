from Crypto.Util.number import *
import pickle
import os, sys
import string, random
from hashlib import sha256
import pickletools
class CrcCalc:
    def __init__(self, size, mod):
        self.size = size
        self.flip = (1 << size) - 1
        self.mod = mod

    def crc(self, inp):
        l = len(inp)
        v = self.flip
        for i in range(l):
            v ^= inp[i]
            for j in range(8):
                t = v & 1
                v >>= 1
                if t: v ^= self.mod
        return v ^ self.flip

inp = input()
inp = bytes.fromhex(inp)
hasher = pickle.load(open('CrcSetting', 'rb'))
print(hasher.size)
