from Crypto.Util.number import *
import math

f = open('output','r')
x=f.readlines()
data=[]
print int(x[0])
for i in range(10):
	data.append(eval(x[1])[0])

