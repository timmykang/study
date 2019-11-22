from Crypto.Util.number import *
from pwn import *
import math
import os
from Pohlig_Hellman import *
r=remote('3.115.26.78',31337)
r.recvuntil('! ')
encflag = int(r.recvline()[:-1],16)
prime_file = open("pastctfprimes.txt")
def xvalue(r,n):
	r.recvuntil(': ')
	r.send(n+'\n')
	return int(r.recvline()[:-1],16)

findn=[]
findn1 = []
tmp = '00'
for i in range(16):
	findn.append(xvalue(r,tmp*i))
for i in range(13):
	tmp0 = findn[i]*findn[i+3]-findn[i+1]*findn[i+2]
	findn1.append(abs(tmp0))
n = findn1[0]
for i in range(12):
	n = GCD(n,findn1[i+1])
tmp0 = inverse(findn[0],n)
e256 = (findn[1] * tmp0) % n

#for i in range(15):
#	if(((findn[i]*e256)%n) != findn[i+1]):
#		print 111
#
i=0
tmp1 = 256
# 'X:' = 0x583a
'''
while(1):
	i=i+1
	if(tmp1 == e256):

		print i
		break
	if(i%100000 == 0):
		print i
		#print tmp1
	tmp1 = (tmp1*256)%n
'''

p = 531268630871904928125236420930762796930566248599562838123179520115291463168597060453850582450268863522872788705521479922595212649079603574353380342938159
q = 52991530070696473563320564293242344753975698734819856541454993888990555556689500359127445576561403828332510518908254263289997022658687697289264351266523
r.close()
phin = (p-1) * (q-1)
i=0;
e=375469807216214245
d = inverse(e,phin)
print long_to_bytes(pow(encflag,d,n))
#print PohlingHellman(e256%p,256,p)
#hitcon{@@@_5m00thneSS_CAN_give_y0u_everything_@@@}
