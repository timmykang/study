import os
import copy
from pwn import *
r = 18
def get_number(x, num):
    num_list = []
    for i in range(num):
        num_list.append(int(x[i*2:i*2+2],16))
    return num_list
    
def get_flag(r1):
    r1.recvuntil('> ')
    r1.sendline('read')
    r1.recvuntil('> ')
    r1.sendline('encrypt {}'.format(r))
    return r1.recvline()[-(r*2+1):-1]

r1 = remote('rcrypted.zajebistyc.tf', 13401)

flag = []
flag_cnt = []
text = []

for i in range(r):
    tmp = [1] * 256
    flag.append(tmp)

for i in range(r):
    flag_cnt.append(256)

for i in range(r):
    text.append(0)

cnt = 0

while(True):
    result_cnt = 0
    tmp = get_flag(r1)
    cnt += 1
    num_list = get_number(tmp, r)
    for i in range(r):
        flag[i][num_list[i]] = 0

    for i in range(r):
        flag_cnt[i] = flag[i].count(1)
        if flag_cnt[i] == 1:
            text[i] = flag[i].index(1)
            result_cnt += 1
    if result_cnt > 9:
        print(text)
    if cnt % 10 == 0:
        print(flag_cnt)

#p4{sh0ut-out-to-4-5UP3R-old-un1nt3nded-5ln}
#p4{45-w34k-45-rc4}