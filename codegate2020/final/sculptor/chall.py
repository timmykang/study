#!/usr/bin/env python3.6
from secrets import randbelow
from operator import mul, xor
from functools import reduce
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes


N = 32
RING = (1 << 64) - 1
HINT = 100
HIDDEN = 32
c = [17827132501379851035, 5851056884845272704, 1845704364124646650, 15836507227607295275, 1106964868274904891, 5845592521729879726, 91646535857391446, 15397131229965405302, 11191725307616665442, 12734483972872158347, 4506487327544846708, 18067557784618292003, 6510915725349296939, 14639792346136501810, 17276930815729787739, 11988420509120517358, 15360971264850667768, 58489665258696137, 4550637667337808278, 10392893776676367229, 14606305828993504764, 18176990710301326162, 12609713052491255944, 9000379525426469430, 13378472137155166126, 2752353359552421473, 1900460475227305085, 2114252013602600216, 15879419165026576562, 13969456881896057436, 11880820437209096217, 214333111987599963]
h = [519973979, 623383399, 1579195702, 1754023387, 3117142133, 1107028747, 1942991234, 2649665059, 102387579, 25959660, 4058586302, 2666013584, 171393018, 1875267814, 3702795761, 2155770919, 3288100614, 1782923713, 1531624490, 4019319433, 517109090, 2213388397, 404678846, 2261904930, 103076579, 629575836, 3065088411, 2270982688, 875718778, 1194519484, 1037961642, 577068345, 3380374039, 3728200265, 451658484, 1426379237, 1134146754, 136605769, 3149519492, 4228760231, 2342373475, 1890212848, 2893405259, 1884392206, 1676763632, 50388826, 4006273939, 918966644, 1000414053, 1481330241, 1879319862, 312167869, 3709576948, 2933699470, 3502068483, 214900782, 55883729, 542385118, 3116403337, 661241624, 2031173049, 873763702, 1713836441, 998578259, 290461426, 3749290885, 2296004039, 3405981950, 3292023544, 2061086519, 3510401205, 218282476, 1530806889, 3636287883, 2743698663, 2384736143, 4042249846, 373401650, 2098957877, 2940480206, 1015584170, 1769173508, 2420771613, 2002166859, 3313971679, 1164976756, 1726236129, 1121501871, 3385841262, 2668770947, 2141972091, 2974249608, 2064772452, 1201471501, 2575511574, 3316818187, 3167425598, 3842019234, 3950823601, 2430345589]
encflag = 0x3b1c62de25bcad16207435ebf54460579d6926856e40c3cd65fa53955af20c06b6e0f17c568d1e5fe053ab21df3c9602
y = [1972144224, 2627872095, 25616827, 2546659650, 1486700945, 3135390776, 1645382154, 3270169363, 4022243039, 1105862731, 1531958259, 858484709, 2387452042, 2898936390, 2232410918, 2656271523, 2681765966, 314333569, 1103213179, 2785173453, 3238467204, 1214172424, 3198812070, 676224441, 1206100467, 280956036, 3219171367, 46386436, 3748391170, 1850995786, 2975153847, 945238126]
s = []
for i in range(32):
    s.append((h[i] << 32) + y[i])


class Random:

    def __init__(self, ring, n):
        self.ring = ring
        self.n = n
        self.c = [randbelow(ring) for _ in range(n)]
        self.s = [randbelow(ring) for _ in range(n)]

    def f(self):
        return sum(map(mul, self.c, self.s)) % self.ring

    def update(self):
        self.s = self.s[1:] + [self.f()]
        return self.s[-1]


if __name__ == '__main__':
    r = Random(RING, N)
    r.c = c

    [r.update() for _ in range(N ** 2)]
    r.s = s
    hints = [r.update() >> HIDDEN for _ in range(HINT - 32)]

    [r.update() for _ in range(N ** 2)]

    size = RING.bit_length() // 4

    key = reduce(xor, r.s + r.c) ** 2
    key = key.to_bytes(size, byteorder='big')
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(long_to_bytes(encflag))

    print(flag)
#CODEGATE2020{Lattices_are_so_fxxking_cool}