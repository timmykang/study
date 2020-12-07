from pwn import *
from string import ascii_lowercase
from itertools import product
from random import SystemRandom
from math import ceil, log

r = remote('queensarah2.chal.perfect.blue', 1)
#r = process('./challenge.py')
r.recvline()
enc_flag = r.recvline()[:-1].decode()[2:-2]

cnt = 0

def get_enc(x, r):
    global cnt
    r.recvuntil('> ')
    r.sendline(x)
    r.recvline()
    cnt += 1
    print(cnt)
    return r.recvline()[:-1].decode()

def find_list(x, y_list):
    for i in range(len(y_list)):
        if x in y_list[i]:
            return i
    return False

def concat_list(a_list, b_list, a_previous, b_next):
    a_index = a_list.index(a_previous)
    b_index = b_list.index(b_next)
    list_len = len(a_list)
    res_list = []
    for i in range(list_len):
        res_list.append(a_list[(a_index + i) % list_len])
        res_list.append(b_list[(b_index + i) % list_len])
    return res_list

def remake_list(a_list):
    list_len = len(a_list)
    assert list_len % 2 == 1
    res_list = []
    tmp = (list_len + 1) // 2
    for i in range(list_len):
        res_list.append(a_list[(i * tmp) % list_len])
    return res_list

def make_mes(s_list, x):
    tmp_list = s_list[find_list(x, s_list)]
    tmp_mes = tmp_list[(tmp_list.index(x)-1) % len(tmp_list)]
    return tmp_mes

def find_inverse(s_list, x):
    assert len(x) == 4
    for i in range(3):
        tmp0 = x[0] + x[2]
        tmp1 = x[1] + x[3]
        if not find_list(tmp0, s_list) or not find_list(tmp1, s_list):
            return False
        else:
            x = make_mes(s_list, tmp0) + make_mes(s_list, tmp1)
    return x

def decrypt(message, s_list):
    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2)))
    for round in range(rounds):
        if round > 0:
            tmp = []
            for i in range(len(message)//2):
                tmp += [message[i], message[i + len(message) // 2]]
            message = tmp
        for i in range(0, len(message), 2):
            message[i:i+2] = make_mes(s_list, ''.join(message[i:i+2]))
    return ''.join(message)               

ALPHABET = ascii_lowercase + "_"
bigrams = [''.join(bigram) for bigram in product(ALPHABET, repeat=2)]
tmp_list = []
tmp1_list = []
while(len(bigrams) != 0):
    tmp0 = bigrams[0]
    tmp1 = tmp0
    tmp = []
    while(True):
        bigrams.remove(tmp1)
        tmp.append(tmp1)
        tmp1 = get_enc(tmp1, r)
        if tmp1 == tmp0:
            print(len(tmp))
            break
    tmp_list.append(tmp)
    tmp1_list.append(len(tmp))

tmp_s_list = []
s_list = []

for i in range(len(tmp_list)):
    if tmp1_list.count(len(tmp_list[i])) == 1:
        tmp_s_list.append(tmp_list[i])

for i in tmp_s_list:
    s_list.append(remake_list(i))
    tmp_list.remove(i)

cnt1 = 0
while(len(tmp_list) != 0):
    cnt1 += 1
    print(cnt1)
    for i in tmp_list:
        flag = 0
        for j in i:
            bigrams = [''.join(bigram) for bigram in product(ALPHABET, repeat=2)]
            for k in bigrams:
                tmp = j+k
                tmp1 = find_inverse(s_list, tmp)
                if tmp1:
                    tmp_enc = get_enc(tmp1, r)
                    tmp_a = tmp_list[find_list(j, tmp_list)]
                    tmp_b = tmp_list[find_list(tmp_enc[:2], tmp_list)]
                    s_list.append(concat_list(tmp_a, tmp_b, j, tmp_enc[:2]))
                    tmp_list.remove(tmp_a)
                    if tmp_a != tmp_b:
                        tmp_list.remove(tmp_b)
                    flag = 1
                if flag == 1:
                    break
            if flag == 1:
                break
        if flag == 1:
            break
    if cnt1 > 15:
        print(tmp_list)

print(decrypt(enc_flag, s_list))
r.interactive()
#pbctf{slide_attack_still_relevant_for_home_rolled_crypto_systems}