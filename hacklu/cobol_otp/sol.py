#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Crypto.Util.number import *
x='A6 D2 13 96 79 3B 10 64 68 75 9F DD 46 9F 5D 17 55 6A 68 43 8F 8C 2D 92 31 07 54 60 68 26 9F CD 46 87 31 2A 54 7B 04 5F A6 EB 06 A4 70 30 11 32 4A 0A'
tmp = ''
tmp1 = ''
for i in range(50):
	tmp = tmp + x[3*i:3*i+2]
print (tmp)
for i in range(41,42):
	print i
	tmp1 = (hex(i)[2:]) * 50
	sol = hex(int(tmp,16)^int(tmp1,16))
	print (sol)
