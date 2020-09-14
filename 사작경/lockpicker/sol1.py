#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from os import urandom

n = 0x914e0f4b603ac9ab6eb0796271fff8f6033aa612e04d95547109d025748e1c68672fe40459e71937e6a3f9156fd4713ad95a3198b318378565f53e46c6059e0f6ec973c09a4f588e8f9078e03af8a7ea6211169638efd7c5d5db179c37cdf4732aa5462bca7deab6c3c9c6b02a0491d8363495b1c834e7733eeccfa0aaa6d021
enc_master_key = 0x80e611da674e6654d7aece63cbb659effec7c31739c9e5996ccb6b45d4cb3581b432ac033e6eee900eb30a41ab1964ff52dce8a2c909c1b82a3e102ecc16742cd48d559fdff2372c55d8094913934fcafccdf28bdfd2b081b81dbef2f475e5223e299c623d9f70030a1e288a64978f5c47c022593b70f42dfe2eba90bdb58415
p = 9948474479436238487097843039220267347435759423720839486093373703533485799457499214993533467207104249020402684570802127036607141522224433552019075009195229
q = n // p
print(p*q-n)
phin = (p-1) * (q-1)
d = inverse(65537, phin)
key = RSA.construct((n,65537,d))
cipher = PKCS1_OAEP.new(key)
enc_master_key = long_to_bytes(enc_master_key)
master_key = cipher.decrypt(enc_master_key)
with open('safe.lock', 'rb') as f:
    ciphertext = f.read()
master_cipher = AES.new(master_key, AES.MODE_ECB)
print(master_cipher.decrypt(ciphertext))
