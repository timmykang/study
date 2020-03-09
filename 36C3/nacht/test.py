import os, ctypes
from pwn import *
r = remote('88.198.156.141', 2833)
msg = []
cipher = []
minusp = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 252]
for i in range(32):
    x=r.recvline()[:-1].split(' ')
    msg.append(x[0])
    cipher.append(x[1])
flag_cipher = r.recvline()[:-1].split(' ')[0]

def add1305(x,y):
    tmp = 0
    x1 = [''] * 16
    for i in range(16):
        tmp += (x[i]+y[i])
        x1[i] = hex(tmp & 255)[2:]
        tmp >>= 8
    return x1

def strtoint(x):
    tmp = 0
    for i in range(0,len(x),2):
        tmp = tmp + pow(16,i)*int(x[i:i+2],16)
    return tmp

def list_to_int(x):
    tmp = ''
    for i in x:
        tmp = i+tmp
    return int(tmp,16)

def int_to_list(x):
    tmp = hex(x)[2:]
    tmp1 = []
    for i in range(0,len(tmp),2):
        tmp1.insert(0,tmp[i:i+2])
    return tmp1
def decipher(x,y):
    h = []
    c = []
    for i in range(16):
        h.append(x[2*i:2*i+2])
        c.append(y[32+2*i:32+2*i+2])
    tmp_h = list_to_int(h)
    tmp_c = list_to_int(c)
    tmp_h = (tmp_h - tmp_c) % (1<<128)
    h = int_to_list(tmp_h)
    print h

decipher(cipher[0], msg[0])

