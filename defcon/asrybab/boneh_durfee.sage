# -*- coding: utf-8 -*-
import time
from Crypto.Util.number import *
debug = True
# display stats on helpful vectors
def helpful_vectors(BB, modulus):
	nothelpful = 0
	for ii in range(BB.dimensions()[0]):
		if BB[ii,ii] >= modulus:
			nothelpful += 1
	print nothelpful, "/", BB.dimensions()[0], " vectors are not helpful"
# display matrix picture with 0 and X
def matrix_overview(BB, bound):
	for ii in range(BB.dimensions()[0]):
		a = ('%02d ' % ii)
		for jj in range(BB.dimensions()[1]):
			a += '0' if BB[ii,jj] == 0 else 'X'
			a += ' '
		if BB[ii, ii] >= bound:
			a += '~'
		print a
def boneh_durfee(pol, modulus, mm, tt, XX, YY):
	PR.<u, x, y> = PolynomialRing(ZZ)
	Q = PR.quotient(x*y + 1 - u) 
	polZ = Q(pol).lift()
	UU = XX*YY + 1
	gg = []
	for kk in range(mm + 1):
		for ii in range(mm - kk + 1):
			xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
			gg.append(xshift)
	gg.sort()	
	monomials = []
	for polynomial in gg:
		for monomial in polynomial.monomials():
			if monomial not in monomials:
				monomials.append(monomial)
	monomials.sort()
	
	# y−shifts (selected by Herrman and May)
	for jj in range(1, tt + 1):
		for kk in range(floor(mm/tt) * jj, mm + 1):
			yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
			yshift = Q(yshift).lift()
			gg.append(yshift) # substitution
			# y−shifts monomials
	for jj in range(1, tt + 1):
		for kk in range(floor(mm/tt) * jj, mm + 1):
			monomials.append(u^kk * y^jj)
	nn = len(monomials)
	BB = Matrix(ZZ, nn)
	for ii in range(nn):
		BB[ii, 0] = gg[ii](0, 0, 0)
		for jj in range(1, ii + 1):
			if monomials[jj] in gg[ii].monomials():
				BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
	# check if vectors are helpful
	if debug:
		helpful_vectors(BB, modulus^mm)
	# check if determinant is correctly bounded
	if debug:
		det = BB.det()
		bound = modulus^(mm*nn)
		if det >= bound:
			print "kkk"
			print "We do not have det < bound. Solutions might not be found."
			diff = (log(det) - log(bound)) / log(2)
			print "size det(L) − size e^(m*n) = ", floor(diff)
		else:
			print "det(L) < e^(m*n)"
	# debug: display matrix
	if debug:
		matrix_overview(BB, modulus^mm)
	# LLL
	start_time = time.time()
	BB = BB.LLL()
	print("--- %s seconds ---" %(time.time() - start_time))
	# vectors −> polynomials
	PR.<x,y> = PolynomialRing(ZZ)
	pols = []
	for ii in range(nn):
		pols.append(0)
		for jj in range(nn):
			pols[-1] += monomials[jj](x*y+1,x,y) * BB[ii, jj] / monomials[jj](UU,XX,YY)
		#if pols[-1](xx,yy) != 0:
		#	pols.pop()
		#	break
	# find two vectors we can work with
	pol1 = pol2 = 0
	found = False
	for ii, pol in enumerate(pols):
		if found:
			break
		for jj in range(ii + 1, len(pols)):
			if gcd(pol, pols[jj]) == 1:
				print "using vectors", ii, "and", jj
				pol1 = pol
				pol2 = pols[jj]
				# break from that double loop
				found = True
				break
	# failure
	if pol1 == pol2 == 0:
		print "failure"
		return 0, 0
	# resultant
	PR.<x> = PolynomialRing(ZZ)
	rr = pol1.resultant(pol2)
	rr = rr(x, x)
	# solutions
	print rr.roots()
	soly = rr.roots()[0][0]
	print "found for y_0:", soly
	ss = pol1(x, soly)
	solx = ss.roots()[0][0]
	print "found for x_0:", solx
	#
	return solx, soly
############################################
# Test
##########################################
# RSA gen options (tweakable)
length_N = 1280
length_d = 0.26
# RSA gen (for the demo)

p = getStrongPrime(640)
q = getStrongPrime(640)
N = p*q


phi = (p-1)*(q-1)
d = getRandomRange(1<<334, 1<<335)
if d % 2 == 0:
	d += 1
while gcd(d, phi) != 1:
	d += 2
e = d.inverse_mod((p-1)*(q-1))

while e<N:
	e=e+phi
e=e+phi*(1<<24)
print N
print e
# Problem put in equation (default)
P.<x,y> = PolynomialRing(Zmod(e))
A = int((N+1)/2)
pol = 1 + x * (A + y)
# and the solutions to be found (for the demo)
yy = (-p -q)/2
xx = (e * d - 1) / (A + yy)
#
# Default values
# you should tweak delta and m. X should be OK as well
#

#(N,e) = (17188225063218630274888878256642848085451133462453673150725617317019810992352847416952999619245622177994142437556853366349991429498844691433147881954115917074543303208004042494688466699184051646680485854180430706170131818628778591624195028884135852813208353757983422726147876770494503111470209631173016409606277654471025177881526736335431598365866305203520291374695438953630302349045999L, 369121466968691703098127761041757877328644035602316483406750062133856559618447124231265788262793146433778006081434042184792910331130568028096424770429406506163350468292653123919198515541704709301469518929959923516473019914487785179282044627807301971896798659526137981230522503628627846765535517351523326793139088987227777936738710997810595797117964067450473323244113704369505736274635128232105695953L)
#(N,e)=(19258291611715869538292743324910875956863608000228239705737846395727284112036547279290102784546807645133565760689123981442494495659776849814884221243016420660225832557882903920783527331266008026040882870063597262997682250998980675498184199473173021996093137755767296169634734283767807904240785516760224684958632470599039578344439713162479763052572503750837940167794977240086808041196231L, 205851984587961981332571415525891366114949787701270461788614094075972195224065715820021109596924039870445318153466660337593475335604698350521275916993414206047659944243785240631628548164024976054578379082585578041212823294535499181619377639067640808979620568307071847451081373879821369877622498804162464179702587595687467735323299809102912062301313075912313522796894649831347552532553372846391280783L)
#N = 16856351304686462827673672632602165035618544480958520317878525198858469164406686098299554001799577475898291271418290705459068973899613070502465056852816293486632729957590414518796176415121387362559396913032464428892868066221704705687728462621981318822252038013995383622096195508722354180109960536544998087004051480654603939974179866515745452649965913152324591802985327892929941462022307
#e=434702420906241062631556804833808840389221899980380330510080714072964155335052373693767602964773964395150414457749054626533031525624026222177869151768353295452965251977328848048309628615894371472528218096651432291797652866645725967597773587760627624183960445850241561518924528106026696892278131231936189160908331995126459827817227558867741113850685712185560648625122364813782834986223346515457796367
P.<x,y> = PolynomialRing(Zmod(e))
A = int((N+1)/2)
pol = 1+ x * (A+y)
delta = 0.265 # < 0.292 (Boneh & Durfee's bound)
X = 2*floor(N^delta) # this _might_ be too much
Y = floor(N^(1/2)) # correct if p, q are ~ same size
m = 7 # bigger is better (but takes longer)
t = int((1-2*delta) * m) # optimization from Herrmann and May
# Checking bounds (for the demo)
#print "=== checking values ==="
#print "* |y| < Y:", abs(yy) < Y
#print "* |x| < X:", abs(xx) < X
#print "* d < N^0.292", d < N^(0.292)
#print "* size of d:", int(log(d)/log(2))
# boneh_durfee
print "=== running algorithm ==="
start_time = time.time()
solx, soly = boneh_durfee(pol, e, m, t, X, Y)
#print "d : " ,d
#print 'p :', p
#print 'q :', q

#print abs(soly)
# Checking solutions (for the demo)
'''
if xx == solx and yy == soly:
	print "\n=== the solutions are correct ==="
else:
	print "=== FAIL ==="
'''
# Stats
print("=== %s seconds ===" % (time.time() - start_time))
