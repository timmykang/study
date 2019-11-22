from Crypto.Util.number import *
x=1<<45
y=[]
for i in range(1<<12):
	tmp = x+i
	if isPrime(tmp):
		y.append(tmp)

