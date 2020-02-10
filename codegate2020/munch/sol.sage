from Crypto.PublicKey import RSA
from Crypto.Util.number import *
n = 123850820426090063939750639461336535800888872303996740868393788108622197265459429269747101462736954752274429639803614452794471290719054376275608856319222801843407104278834963103014930163521479153822223511859077469170499658852892275556238914610902748238728617276564375256445353397161395711740355127024574224311
c = 56546264931253064991800011273062933350432906376123256400827688151463707024780705798157442404868856565703869323810835490194009709876675990770476983384812994742572992276677277260443081273365933217994869622952757076883760367020628026475789906867095354686131932884540071471310629032433408073596634685260647480557
r_p = 6880599843336662467879109387236213815987292188507187559989074121615354243311606616327703377828006351833629583392546362975490427453804091142854644316412663
r_seed = 6115683512551493681429013672578437250992709174507633110965073551143324876511315798363722262299405597781297506013981949713431316382568201987118489728973776
bitlen = [111, 109, 111, 74]
f = open("output",'r')
temp = f.read().split('\n')
r_list = []
for i in temp:
    r_list.append(int(i))
for i in range(200):
    r_list[i] = (r_list[i] << 460)
r_list1 = []
r_list2 = []
r_list3 = []
r_list4 = []
for i in range(50):
    r_list1.append(r_list[4*i])
    r_list2.append(r_list[4*i+1])
    r_list3.append(r_list[4*i+2])
    r_list4.append(r_list[4*i+3])
r_list1 = vector(r_list1 + [0])
r_list2 = vector(r_list2 + [0])
r_list3 = vector(r_list3 + [0])
r_list4 = vector(r_list4 + [0])
def babai(A, w):
    ''' http://sage-support.narkive.com/HLuYldXC/closest-vector-from-a-lattice '''
    C = max(max(row) for row in A.rows())
    B = matrix([list(row) + [0] for row in A.rows()] + [list(w) + [C]])
    B = B.LLL(delta=0.9)
    return w - vector(B.rows()[-1][:-1])
'''
M1 = matrix(RationalField(),51)
M2 = matrix(RationalField(),51)
M3 = matrix(RationalField(),51)
M4 = matrix(RationalField(),51)
tmpseed = r_seed
for i in range(50):
    M1[i,i] = r_p
    M2[i,i] = r_p
    M3[i,i] = r_p
    M4[i,i] = r_p
    M1[50,i] = tmpseed
    tmpseed = tmpseed ** 2 % r_p
    M2[50,i] = tmpseed
    tmpseed = tmpseed ** 2 % r_p
    M3[50,i] = tmpseed
    tmpseed = tmpseed ** 2 % r_p
    M4[50,i] = tmpseed
    tmpseed = tmpseed ** 2 % r_p
k = 20
M1[50,50] = 1 / (2 ** k)
M2[50,50] = 1 / (2 ** k)
M3[50,50] = 1 / (2 ** k)
M4[50,50] = 1 / (2 ** k)
closest = babai(M1, r_list1)
x1 = (closest[-1] * (2 ** k) % r_p)
print(x1)
closest = babai(M2, r_list2)
x2 = (closest[-1] * (2 ** k) % r_p)
print(x2)
closest = babai(M3, r_list3)
x3 = (closest[-1] * (2 ** k) % r_p)
print(x3)
closest = babai(M4, r_list4)
x4 = (closest[-1] * (2 ** k) % r_p)
print(x4)
'''
x1 = 1554892145023627672041148335479693
x2 = 502255800511355120859629514746208
x3 = 1853790210514838017041045596385832
x4 = 14893066491606236837527

class IIter:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.arr = [0 for _ in range(n)]
        self.sum = 0
        self.stop = False
    
    def __iter__(self):
        return self

    def next(self):
        if self.stop:
            raise StopIteration
        ret = tuple(self.arr)
        self.stop = True
        for i in range(self.n - 1, -1, -1):
            if self.sum == self.m or self.arr[i] == self.m:
                self.sum -= self.arr[i]
                self.arr[i] = 0
                continue
            
            self.arr[i] += 1
            self.sum += 1
            self.stop = False
            break
        return ret

# unknown_ans is for verification
def solve(N, unknown, known, unknown_ans=None, beta=0.5, m=8, t=2):
    assert len(unknown) > 0
    if len(unknown) > 5:
        print "Too many unknown variables!"
        print "This will be much slower"

    n = len(unknown)
    PR = PolynomialRing(Zmod(N), n, var_array=['x'])
    x = PR.objgens()[1]

    # Generate a function for unknown bits
    f = known
    for i in xrange(n):
        f += x[i] * 2^unknown[i][0]

    # Make function monic
    if unknown[0][0] != 1:
        f = f / 2^unknown[0][0]
    
    f = f.change_ring(ZZ)
    x = f.parent().objgens()[1]

    if unknown_ans is not None:
        v = f(unknown_ans)
        if v != 0:
            g = gcd(N, v)
            # g must be non-trivial value (p)
            assert g != 1 and g != N

    # d is dimension, sN is sum from the paper
    d = binomial(m + n, m)
    # t = m * tau
    Xbits = beta * t * (d - n + 1)
    Xbits -= d * t
    Xbits += binomial(m + n, m - 1)
    Xbits -= binomial(m - t + n, m - t - 1)
    Xbits *= N.nbits() * (n + 1) / (m * d)

    print "Xbits =", Xbits
    print "dim =", d

    Ubits = sum(map(lambda x: x[1], unknown))
    assert Ubits < Xbits, "Range is too big"

    X = [ 2^v[1] for v in unknown ]

    # Polynomial construction
    g = []
    monomials = []
    Xmul = []

    # g_k,i2,...,in = x2^i2 * x3^i3 * ... * xn^in * f^k * N^max{t-k, 0}
    # for ij in {0,...,m} and sum(ij) <= m - k
    # monomials : x1^k * x2^i2 * x3^i3 * ... * xn^in
    # Xmul : X1^k * X2^i2 * X3^i3 * ... * Xn^in
    for ii in IIter(m, n):
        k = ii[0]
        g_tmp = f^k * N^max(t-k, 0)
        monomial = x[0]^k
        Xmul_tmp = X[0]^k

        for j in xrange(1, n):
            g_tmp *= x[j]^ii[j]
            monomial *= x[j]^ii[j]
            Xmul_tmp *= X[j]^ii[j]
        
        g.append(g_tmp)
        monomials.append(monomial)
        Xmul.append(Xmul_tmp)

    B = Matrix(ZZ, len(g), len(g))
    for i in range(B.nrows()):
        for j in range(i + 1):
            if j == 0:
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
        h_tmp = 0
        for j in range(B.ncols()):
            if j == 0:
                h_tmp += B[i, j]
            else:
                assert B[i,j] % Xmul[j] == 0
                v = ZZ(B[i,j] // Xmul[j])
                h_tmp += v * monomials[j]
        h.append(h_tmp)

    if unknown_ans is not None:
        assert h[0](unknown_ans) == 0, "Failed to construct polynomial"
        print unknown_ans

    # From https://arxiv.org/pdf/1208.399.pdf
    x_ = [ var('x{}'.format(i)) for i in range(n) ]
    for ii in Combinations(range(len(h)), k=n):
        # It would be nice if there's better way than this :(
        # To use jacobian, we need symbolic variables
        f = symbolic_expression([ h[i](x) for i in ii ]).function(x_)
        jac = jacobian(f, x_)
        v = vector([ t // 2 for t in X ])

        for _ in range(1000):
            kwargs = {'x{}'.format(i): v[i] for i in xrange(n)}
            tmp = v - jac(**kwargs).inverse() * f(**kwargs)
            # Precision is 150-bit now. If it's not enough, give bigger number
            v = vector((numerical_approx(d, prec=150) for d in tmp))

        v = [ int(_.round()) for _ in v ]
        if h[0](v) == 0:
            print("NICE", v)
            return v
        else:
            print("NO", i, j, v)

tmp = (1<<35)-1
t1 = tmp << 111
t2 = t1 << 146
t3 = t2 << 146
known = x1 + (x2 << 146) + (x3 << 292) + (x4 << 438)
#solve(n, [(111,35),(257,35),(403,35)], known,m=6, t=1)
unknown = [2916137381, 14174207518, 28127729793]
p = known + (unknown[0] << 111) + (unknown[1] << 257) + (unknown[2] << 403)
q = n / p
e = 65537
phin = (p-1) * (q-1)
d = inverse(e, phin)
flag = long_to_bytes(pow(c,d,n))
print(flag)
#CODEGATE2020{5e7c462214d48ea48045add289f70b0619a0552bdd4201d8c20cedbfd9ce43cd}