from pwn import *
import random
def get_mes(r,x):
    r.recvuntil('choice: ')
    r.send('1\n')
    r.recvuntil('message: ')
    r.send(x+'\n')
    return r.recvline()[:-1].split(' ')

def get_index(a,b,c,d):
    if len(a) == 16:
        tmp = ord('0')
    elif len(a) == 22:
        tmp = ord('a')
    else:
        tmp = ord('!')
    for i in range(0,len(a),6):
        if((a[i:i+4] == b[i:i+4]) and (b[i:i+4] == c[i:i+4]) and c[i:i+4] == d[i:i+4]):
            tmp1 = int(a[i:i+2],16)
            return (i, tmp^tmp1, len(a))
    exit()

r=remote('15.164.159.194', 8006)
r.recvuntil(': ')
enc_flag=r.recvline()[:-1].split(' ')

number = '1234567890'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet_l = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
tmp = ''
tmpx = ''
for i in enc_flag:
    if len(i) == 16:
        tmp = tmp + '0'
        tmpx = tmpx+ '1'
    elif len(i) == 22:
        tmp = tmp + 'a'
        tmpx = tmpx + 'b'
    else:
        tmp = tmp + '!'
        tmpx = tmpx + '$'
tmp_0 = get_mes(r,tmpx)
tmp_1 = get_mes(r,tmp)
tmp_2 = get_mes(r,tmp)
tmp_3 = get_mes(r,tmp)
tmp_4 = get_mes(r,tmp)
tmp_index = []
tmp_index1 = []
tmp_index2 = []
plaintext = ''
special_chr = '~`!@#$%^&*()_-+=<,>.?|'

for i in range(64):
    j=(get_index(tmp_1[i], tmp_2[i], tmp_3[i], tmp_4[i]))
    tmp_index.append(j[0])
    tmp_index1.append(j[1])
    tmp_index2.append(j[2])
    tmp_chr = chr(int(enc_flag[i][j[0]:j[0]+2],16) ^ j[1])
    if j[2] == 22 and (tmp_chr not in alphabet):
        tmp_chr = chr(int(enc_flag[i][6:8],16) ^ j[1])
        if tmp_chr not in alphabet_l:
            tmp_chr = chr(int(enc_flag[i][18:20],16) ^ j[1])
            if tmp_chr not in alphabet_l:
                print 'haha....'
                exit()
    plaintext = plaintext + tmp_chr
print plaintext

print tmp_index
print tmp_index1

r.recvuntil('choice: ')
r.send('2\n')
r.recvuntil('flag: ')
r.send(plaintext)
print r.recv()