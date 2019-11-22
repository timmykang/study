import pickle
import numpy as np
from math import pi, sqrt, asin
#from pyquil import Program, get_qc
#from pyquil.gates import *

#Program 1
def Prog1(Q):
	if Q[4] == 0:
		Q[1] = Q[3]^Q[1]
	else:
		Q[0],Q[2] = Q[2],Q[0]
	
	if Q[5] == 0:
		Q[0],Q[3] = Q[3],Q[0]
		Q[0] ^= 1
	else:
		Q[2] = Q[0]^Q[2]
	Q[6] ^= 1
	if Q[6] == 0:
		Q[1],Q[2] = Q[2],Q[1]
	else:
		Q[3] = Q[2]^Q[3]
	Q[7] ^= 1
	if Q[7] == 0:
		Q[0],Q[1] = Q[1],Q[0]
		Q[0] ^= 1
	else:
		Q[3] = Q[1]^Q[3]
	#return Q[0]*8+Q[1]*4+Q[2]*2+Q[3]
	return Q[:4]
#Program 2
def Prog2(Q):
	Q[0] ^= 1
	if Q[0] == 0:
		Q[4] ^= Q[7]
	else:
		Q[5],Q[6] = Q[6],Q[5]
	
	if Q[1] == 0:
		Q[5] ^= Q[4]
	else:
		Q[4],Q[6] = Q[6],Q[4]
		Q[6] ^= 1
		
	Q[2] ^= 1
	if Q[2] == 0:
		Q[6],Q[7] = Q[7],Q[6]
		Q[6] ^= 1
	else:
		Q[6] ^= Q[7]

	if Q[3] == 0:
		Q[5] ^= Q[7]
	else:
		Q[5],Q[4] = Q[4],Q[5]
		Q[5] ^= 1
	#return Q[4]*8+Q[5]*4+Q[6]*2+Q[7]
	return Q[4:]
a=[]
for i in range(256):
	x=bin(i)[2:].zfill(8)
	tmp=[]
	for j in range(8):
		tmp.append(int(x[j]))
	a.append(tmp)

b=[]
c=[]
for i in range(256):
	#x = Prog1(a[i])*16
	#x += Prog1(a[i])
	x= Prog1(a[i])+Prog2(a[i])
	b.append(x)

with open('result','rb') as f:
    y=pickle.load(f)
xxx=[]
tmp0 = list(y[0])
print type(tmp0)
for i in range(3200000):
	tmp0 = list(y[i])
	xxx.append(tmp0)

for i in range(8):
	count1 = 0
	tmp = ((1<<8)-1)^(1<<i)
	for j in range(256):
		tmp1 = j &tmp
		count1 += xxx.count(b[tmp1])
	print count1


	
