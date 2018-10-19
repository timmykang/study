from pwn import *
from Crypto import *
from math import factorial
r=remote('arcade.fluxfingers.net',1820)
r.recvuntil('Challenge: ')
challenge = r.recvuntil('\n')
challenge = challenge[:-1]

n=385
offset = 2432902008176639000
key1=[0]*385
key2=[1]*385
def generatekey(i):
	x=str(i)
	r.recvuntil('> ')
	r.send(x+'\n')
	return r.recvuntil('\n')

def list_to_num(l):
	num = 0L
	for i in l:
		num <<= 1
		num += i
	return num

for x in range(384):
	print x
	i1 = factorial(n)-offset
	i2 = (factorial(n-x-1)-offset)%factorial(n)
	i2 = i2 + factorial(n)*(factorial(n)-factorial(n-x-1))
	if generatekey(i1) == generatekey(i2):
		key1[x+1] = key1[x] ^ 0
		key2[x+1] = key2[x] ^ 0
		print 1
	else:
		key1[x+1] = key1[x]^1
		key2[x+1] = key2[x]^1

flag1 = list_to_num(key1) ^ int(challenge,0)
flag2 = list_to_num(key2) ^ int(challenge,0)
print flag1
print flag2
flag11 = hex(flag1)
flag22 = hex(flag2)
r.close()
