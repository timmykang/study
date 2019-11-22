from output import *
from Crypto.Util.number import *
#print p.count('FC') 4
a=[]
i=0
while(i!=-1):
	i=p.find('FC',i+1)
	a.append(i)
a.remove(-1)

def test(a,b):
	tmp = a[:b]+'9F'+a[b+2:]
	return tmp

p = test(p,a[1])
p = test(p,a[3])
p=int(p[2:],16)
q=n/p
phin = (p-1)*(q-1)
d=inverse(65537,phin)
flag=pow(flag,d,n)
print hex(flag)[2:-1].decode('hex')
#INSA{I_w1ll_us3_OTp_n3xT_T1M3}


