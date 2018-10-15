from sage.all import *

n=sys.argv[1]
e=sys.argv[2]
for i in range(1,32):
	div = int(n/i)
	papprox = isqrt(div)
	qapprox = i*papprox + 2 ** 512
	F. = PolynomialRing(Zmod(n))
	f=x-qapprox
	d=f.small_roots(x=2**512, beta=0.5)
	if d:
		d=d[0]
		print qappprox-d
		break

#small_roots(x,beta)
