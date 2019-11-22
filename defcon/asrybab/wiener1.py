import sys
import random
import Crypto.PublicKey.RSA
#import argparse

def division_euclidienne(a, b):
	return (a // b, a % b)


def fraction_continue(n, d):

  developpement = []
  a = n
  b = d

  while b != 0:

    (q,r) = division_euclidienne(a,b)

    developpement.append(q)

    a = b
    b = r
  return (developpement)

    
def reduites_fraction_continue(a):

  l=len(a)

    

  reduites=[]

  h0 = 1
  h1 = 0
  k0 = 0
  k1 = 1
  
  count = 0

      

  while count < l:

    h = a[count] * h1 + h0
    h0 = h1
    h1 = h

    k = a[count] * k1 + k0
    k0 = k1
    k1 = k

    reduites.append((k,h))

    count += 1

  return (reduites)

    

def wiener( n, e):

    

  fc = fraction_continue(e, n)

    

  reduites = reduites_fraction_continue(fc)

    

  message_clair = random.randint(10**1,10**3)

  message_chiffre = pow(message_clair, e, n)
  l = len(reduites)

  i = 0
  while i<l:
	  tmp = reduites[i][1]
	  if(pow(message_chiffre, reduites[i][1], n) == message_clair):
		  break
	  i+=1

  if i != l:

    return (reduites[i][1])

  else:
    return -1

    
#print wiener(90581,17993)

print wiener(744818955050534464823866087257532356968231824820271085207879949998948199709147121321290553099733152323288251591199926821010868081248668951049658913424473469563234265317502534369961636698778949885321284313747952124526309774208636874553139856631170172521493735303157992414728027248540362231668996541750186125327789044965306612074232604373780686285181122911537441192943073310204209086616936360770367059427862743272542535703406418700365566693954029683680217414854103, 57595780582988797422250554495450258341283036312290233089677435648298040662780680840440367886540630330262961400339569961467848933132138886193931053170732881768402173651699826215256813839287157821765771634896183026173084615451076310999329120859080878365701402596570941770905755711526708704996817430012923885310126572767854017353205940605301573014555030099067727738540219598443066483590687404131524809345134371422575152698769519371943813733026109708642159828957941)
#print a.d
