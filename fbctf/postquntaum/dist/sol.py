from pwn import *
def s256(msg):
    # string hex sha256 of a string or hex string message
    try:
        return hashlib.sha256(binascii.unhexlify(msg)).hexdigest()
    except:
        return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def kth_bit(n, k):
    # flag of the kth bit
    # e.g. k(8,1) == 0; k(8,3) == 1
    return 1 if n & (1 << (k)) else 0


def group_by_n(s, n=2):
    # takes a list or tuple and chunks it up into pairs or other n
    # e.g. (1,2,3,4,5,6) -> ((1,2),(3,4),(5,6))
    return [s[i:i + n] for i in range(0, len(s), n)]


def make_top_hash_from_leaves(tree):
    # combine an ordered list key pairs to a top level public key.
    if len(tree) < 2:
        return tree[0]
    else:
        return make_top_hash_from_leaves(
            [s256(a + b) for a, b in group_by_n(tree)]
        )

def bit_stream_from_msg(msg):
    # given a hex string msg, generate a stream of 1 and 0
    # e.g. 'e8' -> (0,0,0,1,0,1,1,1)
    newmsg = int(msg, 16)
    for i in range(4 * len(msg))[::-1]:
        yield kth_bit(newmsg, i)

def make_msg(identity,money,to):
	if(len(to) != 64):
		return 0
	x=''
	x+=identity+' sent '+money+' zuccoins to '+to
	return x

def msg_to_hashes(msg, signature):
    # turn a message with signature into an ordered list of key pairs
    bit_stream = bit_stream_from_msg(msg)
    sign_stream = group_by_n(signature, 2)
    return_stream = []
    for bit, sign in zip(bit_stream, sign_stream):
        if bit:
            return_stream.append(sign[0])
            return_stream.append(s256(sign[1]))
        else:
            return_stream.append(s256(sign[0]))
            return_stream.append(sign[1])
    return return_stream

def make_signed_mes(identity, msg, signature, others):
	x=[]
	x.append(identity)
	x.append(msg)
	x.append(s256(msg))
	for i in range(len(signature)):
		x.append(signature[i])
	for i in range(len(others)):
		x.append(others[i])
	return x
sign=[]
x=''
for i in range(2,514):
	sign.append(i)
#print msg_to_hashes('aaaa',[])
#print make_top_hash_from_leaves([])
#print make_signed_mes('adf','asdf','','')
#print len(x)
print len(y)
r=remote('challenges.fbctf.com',8088)
r.recvuntil(': ')
r.send(y+'\n')
r.recvuntil(': ')
z=r.recvline()[:-1]
if y != z:
	print '1313'
for i in range(2658,5000):
	x='a'*i
	r=remote('challenges.fbctf.com', 8088)
	r.recvuntil(': ')
	r.send(x+'\n')
	r.recvuntil(': ')
	y=r.recvline()[:-1]
	if x!=y:
		print x
	
