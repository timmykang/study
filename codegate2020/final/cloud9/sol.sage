from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.number import *

a = 38240914061990796438737366831519229758147826122081713763266278781817042433002
b = 46190729283374747896507274087688474070284211702985162903204546328076483000624


class Chall:

    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.E  = EllipticCurve(Zmod(self.n), [a, b])
        self.E1 = EllipticCurve(Zmod(p), [a, b])

        # Not Implemented, but you get the point :D
        self.G = E.random_point()
        self.d = randint(1, 1 << 128) & (p >> 1)
        self.Q = self.d * self.G

    def expose(self):
        print(self.n)
        print(self.E1.order())
        print(self.G.xy())
        print(self.Q.xy())

    def getkey(self):
        return self.d


p1 = 37
q1 = 59
n1 = 2183
g1 = (132, 1142)
point1 = (910, 1641)
n2 = 5836992596022446937012188954528837967652088799787297418688161952734029742601918639776384293816907277293165804095447608755394244018171460874413413360601287
order2 = 97940012926710762153437884674079301076079191877203953722437921714333988067208
g2 = (4791064145174837833113077069599757584947381216841105432787931481123835537923996904590176334618000141035959257993847069760040827648845993882710813263422518, 2007135516277895026771627676893419200766568709594031697039637947675097596595809713825936430608820664600227626467013163201670055105153466868380086912003923)
point2 = (2906660915459424515040277093002683642589488507112805139726386938933880929506501185082819430093812825540133325640097413100449877310669418449600698325701077, 3812143203765395705358551712573539116980648501774991245491977901798688330759954052153901303962483747022229555022370548381218346760417689877969168781021420)

E1 = EllipticCurve(Zmod(n2), [a, b])
g2 = E1(g2)
point2 = E1(point2)

E = EllipticCurve(Zmod(n1), [a,b])
g1 = E(g1)
point1 = E(point1)

p2 = 97940012926710762153437884674079301076391785734843620993390248274679651111717
q2 = n2 / p2
'''
tmp_E = EllipticCurve(GF(p1), [a,b])
tmp_g1 = tmp_E(g1)
tmp_point1 = tmp_E(point1)
print(tmp_g1.order())
print(tmp_g1.discrete_log(tmp_point1))

tmp_E = EllipticCurve(GF(q1), [a,b])
tmp_g1 = tmp_E(g1)
tmp_point1 = tmp_E(point1)
print(tmp_g1.order())
print(tmp_g1.discrete_log(tmp_point1))
'''
sd = 2

tmp_E = EllipticCurve(GF(p2), [a,b])
tmp_g2 = tmp_E(g2)
tmp_point2 = tmp_E(point2)
'''
ord_fac = [4,81 , 13 , 151 , 37277 , 63737, 743689, 14743331, 20904431, 3659465143, 38635749385473505471502894387389]
dlogs = []
ord = tmp_g2.order()
print(ord)

for fac in ord_fac[:-1]:
    t = int(ord) // int(fac)
    dlog = (t*tmp_g2).discrete_log(t*tmp_point2)
    dlogs += [dlog]
    print("factor: "+str(fac)+", Discrete Log: "+str(dlogs)) #calculates discrete logarithm for each prime order
l = crt(dlogs, ord_fac[:-1])
'''
ld = 26599269740846508910738525169119527042
l_mod = 1267479141527080354525135305541292599908188436
text = bin(p2 >> 1)[-128:]
size = 16
flag = 0xf512c0de4f899ac8d8e6481f2f9b9df22f0cd05f50f9d42750be913156bb27ea5a141f014082853aa97341499ca74d84
flag = long_to_bytes(flag)
key = int(sd + ld)
key = key.to_bytes(size, byteorder='big')
cipher = AES.new(key, AES.MODE_ECB)
enc_flag = cipher.decrypt(flag)

print(enc_flag)