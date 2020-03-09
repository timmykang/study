from Crypto.Util.number import *
f=open('chall.txt','r')
x=f.read()
tmp = x.split('\n')
enc = []
for i in tmp:
    enc.append(int(i))
print len(enc)
tmp1 = enc[362]
tmp2 = enc[363]
tmp_list = []
flag_tmp = '1111010011001010111001000110000011100000111010001110011' # zer0pts
for i in range(len(flag_tmp)):
    if(flag_tmp[i] == '0'):
        tmp3 = enc[366-i]
        tmp4 = enc[367-i]
        tmp_list.append(abs(tmp1*tmp4-tmp2*tmp3))
        tmp1 = tmp3
        tmp2 = tmp4
tmp_list.remove(0)
n = tmp_list[0]
for i in tmp_list:
    n = GCD(i,n)
'''
for e in range(271828, 314159):
    tmp = pow(2,e,n)
    if tmp1 == (tmp2 * tmp % n):
'''
e=305633
tmp = 0
powe= pow(2,e,n)
n = pow(2,160) * pow(3,380) * pow(7,318)

flag = ''
for i in range(366):
    if enc[i] == (enc[i+1] * powe %n):
        flag = '0'+flag
    else:
        flag = '1'+flag
flag = '1' + flag
flag = int(flag,2)
print long_to_bytes(flag)

#zer0pts{0h_1t_l34ks_th3_l34st_s1gn1f1c4nt_b1t}
