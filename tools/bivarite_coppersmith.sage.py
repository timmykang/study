
# This file was *autogenerated* from the file bivarite_coppersmith.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_45 = Integer(45); _sage_const_5 = Integer(5); _sage_const_256 = Integer(256); _sage_const_8 = Integer(8); _sage_const_512 = Integer(512); _sage_const_511 = Integer(511); _sage_const_0p5 = RealNumber('0.5'); _sage_const_1000 = Integer(1000); _sage_const_150 = Integer(150); _sage_const_30 = Integer(30); _sage_const_6 = Integer(6)
class IIter:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.arr = [_sage_const_0  for _ in range(n)]
        self.sum = _sage_const_0 
        self.stop = False
    
    def __iter__(self):
        return self

    def next(self):
        if self.stop:
            raise StopIteration
        ret = tuple(self.arr)
        self.stop = True
        for i in range(self.n - _sage_const_1 , -_sage_const_1 , -_sage_const_1 ):
            if self.sum == self.m or self.arr[i] == self.m:
                self.sum -= self.arr[i]
                self.arr[i] = _sage_const_0 
                continue
            
            self.arr[i] += _sage_const_1 
            self.sum += _sage_const_1 
            self.stop = False
            break
        return ret

# unknown_ans is for verification
def solve(N, unknown, known, unknown_ans=None, beta=_sage_const_0p5 , m=_sage_const_8 , t=_sage_const_2 ):
    assert len(unknown) > _sage_const_0 
    if len(unknown) > _sage_const_5 :
        print "Too many unknown variables!"
        print "This will be much slower"

    n = len(unknown)
    PR = PolynomialRing(Zmod(N), n, var_array=['x'])
    x = PR.objgens()[_sage_const_1 ]
    
		# Generate a function for unknown bits
    f = known
    for i in xrange(n):
        f += x[i] * _sage_const_2 **unknown[i][_sage_const_0 ]

    # Make function monic
    if unknown[_sage_const_0 ][_sage_const_0 ] != _sage_const_1 :
        f = f / _sage_const_2 **unknown[_sage_const_0 ][_sage_const_0 ]
    
    f = f.change_ring(ZZ)
    x = f.parent().objgens()[_sage_const_1 ]
    
    if unknown_ans is not None:
        v = f(unknown_ans)
        if v != _sage_const_0 :
            g = gcd(N, v)
            # g must be non-trivial value (p)
            assert g != _sage_const_1  and g != N

    # d is dimension, sN is sum from the paper
    d = binomial(m + n, m)
    # t = m * tau
    Xbits = beta * t * (d - n + _sage_const_1 )
    Xbits -= d * t
    Xbits += binomial(m + n, m - _sage_const_1 )
    Xbits -= binomial(m - t + n, m - t - _sage_const_1 )
    Xbits *= N.nbits() * (n + _sage_const_1 ) / (m * d)

    print "Xbits =", Xbits
    print "dim =", d

    Ubits = sum(map(lambda x: x[_sage_const_1 ], unknown))
    assert Ubits < Xbits, "Range is too big"

    X = [ _sage_const_2 **v[_sage_const_1 ] for v in unknown ]

    # Polynomial construction
    g = []
    monomials = []
    Xmul = []
   
    # g_k,i2,...,in = x2^i2 * x3^i3 * ... * xn^in * f^k * N^max{t-k, 0}
    # for ij in {0,...,m} and sum(ij) <= m - k
    # monomials : x1^k * x2^i2 * x3^i3 * ... * xn^in
    # Xmul : X1^k * X2^i2 * X3^i3 * ... * Xn^in
    for i in IIter(m,n):
        print(i)
    for ii in IIter(m, n):
        k = ii[_sage_const_0 ]
        g_tmp = f**k * N**max(t-k, _sage_const_0 )
        monomial = x[_sage_const_0 ]**k
        Xmul_tmp = X[_sage_const_0 ]**k

        for j in xrange(_sage_const_1 , n):
            g_tmp *= x[j]**ii[j]
            monomial *= x[j]**ii[j]
            Xmul_tmp *= X[j]**ii[j]
        
        g.append(g_tmp)
        monomials.append(monomial)
        Xmul.append(Xmul_tmp)

    B = Matrix(ZZ, len(g), len(g))
    for i in range(B.nrows()):
        for j in range(i + _sage_const_1 ):
            if j == _sage_const_0 :
                B[i,j] = g[i].constant_coefficient()
            else:
                v = g[i].monomial_coefficient(monomials[j])
                B[i,j] = v * Xmul[j]

    # DO LLL!!!
    B = B.LLL()

    print "LLL finished"

    # Polynomial reconstruction
    h = []
    for i in range(B.nrows()):
        h_tmp = _sage_const_0 
        for j in range(B.ncols()):
            if j == _sage_const_0 :
                h_tmp += B[i, j]
            else:
                assert B[i,j] % Xmul[j] == _sage_const_0 
                v = ZZ(B[i,j] // Xmul[j])
                h_tmp += v * monomials[j]
        h.append(h_tmp)

    if unknown_ans is not None:
        assert h[_sage_const_0 ](unknown_ans) == _sage_const_0 , "Failed to construct polynomial"
        print unknown_ans

    # From https://arxiv.org/pdf/1208.399.pdf
    x_ = [ var('x{}'.format(i)) for i in range(n) ]
    for ii in Combinations(range(len(h)), k=n):
        # It would be nice if there's better way than this :(
        # To use jacobian, we need symbolic variables
        f = symbolic_expression([ h[i](x) for i in ii ]).function(x_)
        jac = jacobian(f, x_)
        v = vector([ t // _sage_const_2  for t in X ])

        for _ in range(_sage_const_1000 ):
            kwargs = {'x{}'.format(i): v[i] for i in xrange(n)}
            tmp = v - jac(**kwargs).inverse() * f(**kwargs)
            # Precision is 150-bit now. If it's not enough, give bigger number
            v = vector((numerical_approx(d, prec=_sage_const_150 ) for d in tmp))

        v = [ int(_.round()) for _ in v ]
        if h[_sage_const_0 ](v) == _sage_const_0 :
            print("NICE", v)
            return v
        else:
            print("NO", i, j, v)

p = random_prime(_sage_const_2 **_sage_const_512 -_sage_const_1 ,False,_sage_const_2 **_sage_const_511 )
q = random_prime(_sage_const_2 **_sage_const_512 -_sage_const_1 ,False,_sage_const_2 **_sage_const_511 )

if p < q:
    p, q = q, p

# Two chunks

# Get lower kbits(x1) and upper kbits(x2)
kbits = _sage_const_45 

x1_real = p % (_sage_const_2 **kbits)
x2_real = p >> (_sage_const_512  - kbits)

known = p & (( (_sage_const_1  << (_sage_const_512  - _sage_const_2 *kbits) ) - _sage_const_1  ) << kbits)
N = p * q

ans = solve(N, [(_sage_const_0 , kbits), (_sage_const_512  - kbits, kbits)], known, unknown_ans=(x1_real, x2_real), m=_sage_const_8 , t=_sage_const_2 )
assert ans[_sage_const_0 ] == x1_real and ans[_sage_const_1 ] == x2_real

# Three chunks

kbits = _sage_const_30 
t1 = (_sage_const_1  << kbits) - _sage_const_1 
t2 = t1 << _sage_const_256 
t3 = t1 << (_sage_const_512  - kbits)

x1_real, x2_real, x3_real = p & t1, (p & t2) >> _sage_const_256 , (p & t3) >> (_sage_const_512  - kbits)
known = p & ( (_sage_const_1  << _sage_const_512 ) - _sage_const_1  - t1 - t2 - t3 )

ans = solve(N, [(_sage_const_0 , kbits), (_sage_const_256 , kbits), (_sage_const_512  - kbits, kbits)], known, unknown_ans=(x1_real, x2_real, x3_real), m=_sage_const_6 , t=_sage_const_1 )
assert ans[_sage_const_0 ] == x1_real and ans[_sage_const_1 ] == x2_real and ans[_sage_const_2 ] == x3_real

