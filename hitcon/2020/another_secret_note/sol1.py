from pwn import *
from Crypto.Util.number import *
import string
import hashlib
import itertools
import base64
import json

def check_ascii(x):
    str_list = (string.ascii_letters+string.digits+'!@#$%^&*()_-][}{ ;:/?.,><').encode()
    for i in x:
        if i not in str_list:
            return False
    return True
for j in range(0,12):
    print(j)
    with open('data'+str(j), 'r') as f:
        iv0 = f.readline()
        token = f.readline()
        cipher = f.readline()

    print(len(cipher) % 32)
    cnt = (len(cipher) - 160) // 32
    print(cnt)
    iv = bytes.fromhex('3ba9631f48a4fd67f7e3cae3e8ac29ef')
    enc = bytes.fromhex('caa75b43bb137f370909919d09323aa91dd2b46cc92f759a60b3b93fe29c24badb0061c88528bc75679faeed604df525bd627cd688465d65a3aac84cc8db0029')
    plain = b'{"cmd":"get_secret","who":"admin","alpha":"aaa","name":"admin","a":"a"}' +b'\x09' * 9
    plain1 = plain[:16]
    plain2 = plain[16:32]
    plain3 = plain[32:48]
    plain4 = plain[48:64]
    plain5 = plain[64:80]
    iv1 = bytes_to_long(plain1) ^ bytes_to_long(b'{"secret": "hitc') ^ bytes_to_long(iv)

    real_enc = enc[:16] + bytes.fromhex('ddca908e6f57eaf87302398e3c7dbd99')+bytes.fromhex('dc6116f323d7a22c862207df113ba918')
    real_enc = real_enc + bytes.fromhex('ff95b8e2e1b1b5ae6faf4a9166c7a74a')+bytes.fromhex('1417d49cc4390130384965eb58051a9c')
    data_plain = bytes_to_long(b'a' * 16)
    print(real_enc.hex())
    print(hex(iv1))
    for i in range(cnt):
        target_plain = bytes_to_long(real_enc[48:64]) ^ bytes_to_long(plain5)
        tmp0 = int(cipher[96+32*i:128+32*i],16)
        guess_plain = long_to_bytes(target_plain ^ tmp0)
        if check_ascii(guess_plain):
            print('find!!!')
            print(iv0)
            print(token)
            print(target_plain)
            print(i, guess_plain)
            break
        
