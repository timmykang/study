import hashlib
import signal
import sys
import struct
import random
import os
from fastecdsa import keys, curve

n =  int('ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551',16)
secret = os.urandom(4)
print int((secret).encode('hex'),16)
tmp= struct.unpack(">I",secret)[0]
print hex(tmp)
#n=0
#for i in range(8):
#	n = (n << 32) + (tmp * random.getrandbits(1))
print hex(n)
i=1
x=[]
while(1):
	x.append(keys.get_public_key(i,curve.P256))
	i=i+1
	if(i%100000==0):
		print i
print(keys.get_public_key(n,curve.P256))
