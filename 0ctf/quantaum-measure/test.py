import pickle
import numpy as np
from math import pi, sqrt, asin
from pyquil import Program, get_qc
from pyquil.gates import *
size = 4
num = 3200000
flag ='a123aabc12'
def encode(qid, msg):
    assert 0 <= msg < 16
    return RY(asin(sqrt(msg/16))*2, qid)

def get_choice(x):
	try:
		choice = Program(x)
		assert 'DE' not in str(choice)
		return choice
	except Exception as e:
		print(type(e), e)
		exit(b'What are you doing?!')

msg = [int(i, 16) for i in flag]
init = Program()
for i,m in enumerate(msg):
	init += encode(i,m)
init1 = Program()
qc = get_qc('16q-qvm')
with open('program1', 'rb') as f:
	main = pickle.load(f)
program = init+main
#print(program)
reg = program.declare('ro', 'BIT', size)
for i in range(size):
	program += MEASURE(i, reg[i])

#print (qc.run(qc.compile(program)))
with open('result','rb') as f:
	xxx=pickle.load(f)
x=[0]*16
y=[0]*16
for i in range(num):
	x[xxx[i][0]*8+xxx[i][1]*4+xxx[i][2]*2+xxx[i][3]] += 1
	y[xxx[i][4]*8+xxx[i][5]*4+xxx[i][6]*2+xxx[i][7]] += 1
print(x)
print(y)
