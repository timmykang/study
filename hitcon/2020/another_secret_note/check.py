from pwn import *
from Crypto.Util.number import *
import string

def check_ascii(x):
    str_list = (string.ascii_letters+string.digits+'!@#$%^&*()_-][}{ ;:/?.,><').encode()
    for i in x:
        if i not in str_list:
            return False
    return True
    
with open('data', 'r') as f:
    cipher = f.readline()


result = cipher[-64:-32]

tmp = bytes.fromhex(cipher[-96:-64])
print(result)
print(bytes_to_long(tmp) ^ bytes_to_long(b'{z2_[cEeb?$3xjgR'))