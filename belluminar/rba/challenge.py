#!/usr/bin/env python3

from Crypto.Util.number import *
import pickle
import os, sys
import string, random
from hashlib import sha256

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

def print(s, ln=True):
    if ln:
        s += '\n'
    sys.stdout.write(s)
    sys.stdout.flush()

def gen_params(bits):
    assert bits % 128 == 0

    e = 0x10001
    while True:
        p, q = [ getStrongPrime(bits) for _ in range(2) ]
        if p < q:
            p, q = q, p
        N, phi = p * q, (p - 1) * (q - 1)
        if GCD(phi, e) == 1:
            break

    return (e, N, p, q)

def get_padded_flag(bits):
    bytelen = (2 * bits) // 8
    with open('flag', 'rb') as f:
        flag = f.read()

    padlen = bytelen - len(flag) - 1
    flag = os.urandom(padlen) + flag

    assert len(flag) < bytelen
    return flag

def proof():
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    answer = ''.join(random.choice(alphabet) for i in range(16))
    hsh = sha256(answer.encode()).hexdigest()
    print("Prefix: " + answer[:12])
    print("Hash: " + hsh)
    print("Give me four letters: ", ln=False)
    inp = input()

    if len(inp) == 4 and sha256((answer[:12] + inp).encode()).hexdigest() == hsh:
        print("OK")
        return True
    else:
        print("NO")
        return False

if __name__ == "__main__":

    # Generate parameters
    bits = 640
    e, N, p, q = gen_params(bits)
    print("=" * 50)
    print("Generated parameters")
    print("N = {:x}".format(N))
    print("e = {:x}".format(e))

    # Encrypt the flag
    flag = get_padded_flag(bits)
    flag = bytes_to_long(flag)
    enc = pow(flag, e, N)
    print("=" * 50)
    print("Encrypted the flag")
    print("flag = {:x}".format(enc))

    # Hint time!
    print("=" * 50)
    print("Now, I'll give you a chance! (I'm so kind)")
    print("As this presentation: https://www.kangacrypt.info/files/NH.pdf")
    print("It is possible to recover p from given any random bits of p!")
    print("If you give me the hexstring, I'll hash it,")
    print("and give you some random bits of p from the hash result.")

    print("> ", ln=False)
		#inp = input()
    inp = 'cc1e3e439d770d7c96e0020ddd5233f3ded56bca3e33bc49d95514242f5e53cd707e6c6061e1fae8a80c7b9569140cd059b326287a0f6101e861367775be28dafe9c2cfc9bd2b0816de05f3493377eb885e30e25394610b258e5b229283965532114641b6cfdd3d0d89d190aa3007a2d9afee21e354f41aee412d775d64f42489bc8ceee4670b5d4e40723733add7c294a077bd99cd268001e62175a34f8b5addc8a42672299055f288b03f54291c1bff3be0130900178e1de0d7a08c2e6f5ff2f569fec65a861263e843b7602d82fa3e9a4d8e8bead1768bd4c5f66506ac941332882951e0a1abe5b092d2e012ef399baf587a60981e7d4826bd5974010612678e2a8cc024ad028f4703379a36e1ea67a0cae233f7e59c46e25ae38588fe49c08757f67f8e578534c6ac7b5150d381d6cf57814104f0da24f056c60954e757e5914508e88c7d1120f9d7ec163f5b12f501af3841d6092c031ddd3748cef1559c04cf32a6c86586170334018106a64b85e8a6f7ece656761052226c195a4ca3740d39447304856f45b066b3bb61aa8546c3482169beb1f34de5f626bb88f47dda4332d0a4587102f256a92b3880df2c1b861fb62098ca9c7e477440f0ec2550d71b9f29f1628fb8a35ba1be7ef5c0e4d3469387357211b79babe16a653b01bd5f017090212b5d44ff419aeee746e23f95598bd6daa020b708fde8f2d4a0526a122c6f189d588765ae8150f429b3922c18a2cb025aaee26418b8073d1a4fc81659196141b2209d09315a16c172f0d094e033aa20be4e900ca230582577d997787'
    try:
        inp = bytes.fromhex(inp)
    except:
        print("WRONG INPUT!!!")
        exit(0)
    hasher = pickle.load(open('CrcSetting', 'rb'))
	
    hash = hasher.crc(inp)
    print("Hash value: {:x}".format(hash))

    tbits, gbits = int(bits * 0.8), int(bits * 0.1)
    bitmask = 0
    for i in range(tbits):
        bitmask |= 1 << (hash % tbits + gbits)
        print(str(hash % tbits + gbits)+' ',False)
        hash //= tbits

    print("Partial p: {:x}".format(bitmask & p))
    print("Bye bye!")
