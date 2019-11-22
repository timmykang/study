from Crypto.Util import number
import math
import dis
NSIZE = 1280

def create_key():
	Nsize = NSIZE
	pqsize = Nsize /2
	N = 0
	while(N.bit_length() != Nsize):
		while(True):
			p=number.getStrongPrime(pqsize)
			q=number.getStrongPrime(pqsize)
			if (abs(p-q)).bit_length() > (Nsize * 0.496):
				break
		N=p*q
	phi = (p-1)*(q-1)
	limit1 = 0.261
	limit2 = 0.293
	while(True):
		d=number.getRandomRange(pow(2,int(Nsize*limit1)), pow(2,int(Nsize*limit1)+1))
		while(d.bit_length() < (Nsize * limit2)):
			ppp = 0
			while not(number.isPrime(ppp)):
				ppp=number.getRandomRange(pow(2,45),pow(2,45)+pow(2,12))
			d*=ppp
		if not(number.GCD(d,phi) != 1):
			e=number.inverse(d,phi)
			if not(number.GCD(e,phi) != 1):
				break
	zzz=3
	return (N,e,d,ppp,phi,p,q)

#print dis.dis(create_key)
(N,e,d,ppp,phi,p,q) = create_key()
#print N-p*q
#print (N,e,d,ppp,p,q)
#print (e*d-1)/((p-1)*(q-1))
#print d/ppp
#print (N,e*ppp)
#print d%ppp
#print d/ppp
#print number.inverse(e*ppp, phi)
#print e*ppp
e1 = (e*ppp)%phi+phi*10
print e
print e*ppp
print (e*ppp)%phi+phi
print N
print N.bit_length()
print d/ppp
print math.log(d/ppp,N)
print N,',',e1
