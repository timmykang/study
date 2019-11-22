import data
import itertools
def sxor(a,b):
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(a,b)) 
text = 'hajjzvajvzqyaqbendzvajvqauzarlapjzrkybjzenzuvczjvastlj'
print len(text)

