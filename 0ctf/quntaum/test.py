from pyquil import Program, get_qc
import os
qc = get_qc('16q-qvm')
print (qc.qubits())
def get_choice(x):
	try:
		choice = Program(x)
		assert 'DE' not in str(choice)
		return choice
	except Exception as e:
		print(type(e), e)
		exit(b'What are you doing?!')

x=get_choice('H 0\r')
y=get_choice('H 0\rX 0')

def rand_choice():
    if (os.urandom(1)[0] & 1):
        return Program('X 0')
    else:
        return Program('I 0')

prog = x+rand_choice()+y
prog = get_choice('X 0')
prog += get_choice('X 15')
print(prog)
x=qc.run_and_measure(prog,1)
print(x)
x=qc.run_and_measure(prog,1)[0]
print(x)
