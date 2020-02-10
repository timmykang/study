from pwn import *
from Crypto.Util.number import *

def get_T(r):
    r.recvuntil('> ')
    r.sendline('1')
    r.recvuntil('= ')
    #r.sendline('0000000000000000000000000000000000000000000000000000000000000000')
    #r.sendline('1000000000000000000000000000000000000000000000000000000000000000')
    r.recvuntil('ciphertext = ')
    T0 = r.recvline()[:-1]
    return T0

r = remote('110.10.147.44', 7777)
#print get_T(r)
#T0 = 'ec8e2e8ec0319fbaa0e7d4d819006e28'
E_0 = 'e6048fd38996e7cb945879d068a612bd'
E_1 = '144e4f2d41105cde0993ce4b02f5e2db'
plain = ';cat flag;000000'
plain_long = bytes_to_long(plain)
ciphertext = hex(int(E_0,16) ^ plain_long)[2:] # dd67eea7a9f08baaf36349e05896228d
feed_data = hex(plain_long)[2:18] + ciphertext[16:] # 3b63617420666c61f36349e05896228d
tag = int(E_0,16) ^ int(feed_data,16)
fake_feed = hex(int(E_1, 16) ^ tag)[2:]
fake_plain = fake_feed[:16] + hex(int(fake_feed[16:],16) ^ int(E_1[16:],16))[2:]

print fake_plain #c929a18ae8e0d774673b303030303030
#10000000000000000000000000000000c929a18ae8e0d774673b303030303030

r.recvuntil('> ')
r.sendline('1')
r.recvuntil('= ')
r.sendline('10000000000000000000000000000000c929a18ae8e0d774673b303030303030')
r.recvuntil('tag = ') 
tag = r.recvline()[:-1] #04e46eb38401a4727f15967a29784f17
r.close() 
r = remote('110.10.147.44', 7777)
r.recvuntil('> ')
r.sendline('3')
r.recvuntil('= ')
r.sendline('00000000000000000000000000000000')
r.recvuntil('= ')
r.sendline('ec8e2e8ec0319fbaa0e7d4d819006e28dd67eea7a9f08baaf36349e05896228d')
r.recvuntil('= ')
r.sendline(tag)
print r.recv()
#CODEGATE2020{F33D1NG_0N1Y_H4LF_BL0CK_W1TH_BL0CK_C1PH3R}
r.close()