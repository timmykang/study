#!/usr/bin/python3 -u
from secrets import flag
from fastecdsa import keys, curve
import hashlib
import signal
import sys
import struct
import random
import os

def handler(signum, frame):
    print("\nGame over!")
    sys.exit(0)

signal.signal(signal.SIGALRM, handler)

secret = os.urandom(1000)
pub_keys = []
for i in range(0, len(secret), 4):
    p = struct.unpack(">I", secret[i:i+4])[0]
    n = 0
    while n == 0:
        for i in range(8):
            n = (n << 32) + (p * random.getrandbits(1))
    pk = keys.get_public_key(n, curve.P256)
    pub_keys.append((hex(pk.x), hex(pk.y)))

print(pub_keys)

signal.alarm(100)
h = input("Tell me the hash: ")
if h == hashlib.sha256(secret).hexdigest():
    print(flag)
