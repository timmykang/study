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


    
    





N = 123463519828344660835965296108959625188149729700517379543746606603601816029557213728343115758280318474617032830851553509268562367217512005079977122560679743955588214135519642513042848616372204042776892196887455692479457740367547908255044784496969010537283159300508751036032559594474145098337531029291955103059
e = 85803665824396212221464259773478155183477895540333642019501498374139506738444521180470104195883386495607712971252463223185914391456070458788554837326327618859712794129800329295751565279950274474800740076285111503780662397876663144946831503522281710586712396810593754749589799811545251575782431569881989690861
gift = 46710143823773072238724337855139753113453277386728402328859555407710009799097841900723288768522450009531777773692804519189753306306645410280934372812
enc = 106121451638162677594573310940827829041097305506084523508481527070289767121202640647932427882853090304492662258820333412210185673459181060321182621778215705296467924514370932937109363645133019461501960295399876223216991409548390823510949085131028770701612550221001043472702499511394058569487248345808385915190

m = 2
t = 2

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