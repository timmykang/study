from flag import *
#X, N, E, C
def nextbit(p,q,x,n,k):
	p1 = int(('1'+p),2)
	p0 = int(p,2)
	q1 = int(('1'+q),2)
	q0 = int(q,2)
	n00 = "{0:b}".format(p0*q0)[::-1].zfill(k+1)
	n01 = "{0:b}".format(p0*q1)[::-1].zfill(k+1)
	n11 = "{0:b}".format(p1*q1)[::-1].zfill(k+1)
	n10 = "{0:b}".format(p1*q0)[::-1].zfill(k+1)
	xrev = x[::-1]
	nrev = n[::-1]
	print p
	print q
	print xrev[k]
	print nrev[k]
	print n00[k]
	print n01[k]
	print n11[k]
	print n10[k]
	if(xrev[k]=='0'):
		if(n00[k] == nrev[k]):
			return '0'+p,'0'+q,x,n,k+1
		if(n11[k] == nrev[k]):
			print 'fuck'
			return '1'+p,'1'+q,x,n,k+1
	else:
		if(n01[k] == nrev[k]):
			return '0'+p,'1'+q,x,n,k+1
		if(n10[k] == nrev[k]):
			return '1'+p,'0'+q,x,n,k+1

xbit = len("{0:b}".format(X))
k=1
p='1'
q='1'
X="{0:b}".format(X)
N="{0:b}".format(N)
for i in range(xbit-1):
	p,q,X,N,k=nextbit(p,q,X,N,k)
		

print p
print q
print k

		
