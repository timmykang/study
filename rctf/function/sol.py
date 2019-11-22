from Crypto.Util.number import *
from fractions import Fraction
f=open("enc",'r')
xx=[]
tmp2=[]
for i in range(0x200):
	x=f.readline()
	y=x.find(')')
	xx.append(int(x[2:y]))
	tmp2.append(int(x[y+4:-1]))

tmp = []
for i in range(512):
	tmp.append(xx[i])

xx.sort()
yy=[]
for i in range(512):
	tmp1 = tmp.index(xx[i])
	yy.append(tmp2[tmp1])

print xx
x=[]
x=[[]]
for i in range(512):
	x[0].append(yy[i])
for i in range(256):
	x.append([0]*512)

for i in range(1,257):
	print i
	for j in range(300-i):
		x[i][j] = (Fraction(x[i-1][j+1])-Fraction(x[i-1][j])/Fraction(xx[j+1]-xx[j]))

print x[256]	
