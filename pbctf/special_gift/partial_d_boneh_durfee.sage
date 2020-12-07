from Crypto.Util.number import *

def matrix_overview(BB):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        print(a)

def partial_d_boneh_durfee(pol, N, e, R, k_near, m, t, X, Y, Z, W):
    n = X ** m * Y ** (m+t) * Z ** m * W
    pol_monomials = pol.monomials()
    pol_coeffs = pol.coefficients()
    f = 0
    for i in range(len(pol_coeffs)):
        pol_coeffs[i] = pol_coeffs[i] * inverse(pol_coeffs[-1], n) % n
        f += pol_monomials[i] * pol_coeffs[i]

    g = 0
    polynomial_list = []
    monomial_list = []
    for i in range(m+1):
        for j in range(m-i+1):
            for k in range(m-i+1):
                g = (X*x)**i * (Y*y)**j * (Z*z) **k * f(x*X, y*Y, z*Z) * X ** (m-i) * Y ** (m+t-j) * Z ** (m-k)
                polynomial_list.append(g)
                for l in g.monomials():
                    if l not in monomial_list:
                        monomial_list.append(l)
    print("make g")

    for i in range(m+1):
        for j in range(m-i+1, m-i+t+1):
            for k in range(m-i+1):
                h = (X*x)**i * (Y*y)**j * (Z*z) **k * f(x*X, y*Y, z*Z) * X ** (m-i) * Y ** (m+t-j) * Z ** (m-k)
                polynomial_list.append(h)
                for l in h.monomials():
                    if l not in monomial_list:
                        monomial_list.append(l)
    print("make h")

    for i in range(m+2):
        for j in range(m+t+2-i):
            g_1 = n * (x*X) ** i * (y*Y) ** j * (z * Z) ** (m+1-i)
            polynomial_list.append(g_1)
    print("make g_1")

    for i in range(m+1):
        for k in range(m-i+1):
            h_1 = n * (x*X) ** i * (y*Y) ** (m+t+1-i) * (z * Z) ** k
            polynomial_list.append(h_1)
    print("make h_1")

    monomial_list.sort()
    mov_polynomial_list = []
    M = matrix(len(monomial_list))
    for i in range(len(monomial_list)):
        for j in polynomial_list:
            if monomial_list[i] in j.monomials():
                mov_polynomial_list.append(j)
                polynomial_list.remove(j)
                break
        tmp_coef = j.coefficients()
        tmp_monomial = j.monomials()
        for j in range(len(tmp_monomial)):
            tmp = monomial_list.index(tmp_monomial[j])
            M[i,tmp] = (tmp_coef[j] // (X ** m * Y ** (m+t) * Z ** m))
            assert tmp_coef[j] % (X ** m * Y ** (m+t) * Z ** m) == 0

    matrix_overview(M)

    M = M.LLL()
    PR.<a,b> = PolynomialRing(QQ)
    pol1 = pol2 = 0

    for jj in range(len(monomial_list)):
        pol1 += monomial_list[jj]((N * a - a * b - k_near * b - R)/e,a,b) * M[0, jj] / monomial_list[jj](X,Y,Z)
        pol2 += monomial_list[jj]((N * a - a * b - k_near * b - R)/e,a,b) * M[1, jj] / monomial_list[jj](X,Y,Z)

    rr = pol1.resultant(pol2)
    PR.<q> = PolynomialRing(ZZ)
    rr = rr(q, q)
    print(rr.roots())


    
    





N = 124588792854585991543122421017579759242707321792822503200983206042530513248160179498235727796077646122690756838184806567078369714502863053151565317001149999657802192888347495811627518984421857644550440227092744651891241056244522365071057538408743656419815042273198915328775318113249292516318084091006804073157
e = 109882604549059925698337132134274221192629463500162142191698591870337535769029028534472608748886487359428031919436640522967282998054300836913823872240009473529848093066417214204419524969532809574214972094458725753812433268395365056339836734440559680393774144424319015013231971239186514285386946953708656025167
gift = 870326170979229749948990285479428244545993216619118847039141213397137332130507928675398
enc = 67594553703442235599059635874603827578172490479401786646993398183588852399713973330711427103837471337354320292107030571309136139408387709045820388737058807570181494946004078391176620443144203444539824749021559446977491340748598503240780118417968040337516983519810680009697701876451548797213677765172108334420

m = 1
t = 1

d_near = (gift << 120)
k_near = ((d_near * e - 1) // N) + 1
#d = d_0 + d_near
#k = k_0 + k_near

P.<x,y,z> = PolynomialRing(ZZ)
R = e * d_near - 1 - k_near * N
pol = e * x - N * y + y * z + k_near * z + R

X = 1 << 120
Y = 1 << 120
Z = (1 << 513)
W = 1 << (1024 + 121)
partial_d_boneh_durfee(pol, N, e, R, k_near, m, t, X, Y, Z, W)