import dpkt
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
import math
import os, math, sys, binascii
f1 = open('newfile.pcap')
pcap = dpkt.pcap.Reader(f1)
flag = ''
challenge = []
response = []  
p = 21652247421304131782679331804390761485569
    
## (311*313*317*331*337*347*349*353)^2
denied_i = 0
for ts, pkt in pcap:
    tmp = dpkt.ethernet.Ethernet(pkt).data.data.data
    if(len(str(tmp)) != 0):
        tmp1 = []
        tcp_data = str(tmp)
        if('DENIED' in tcp_data):
            print 'denied_i = 15'
        elif('ACCESS GRANTED' in tcp_data):
            flag = tcp_data[15:-1]
            #denied_i += 1
        elif(len(tcp_data) > 200):
            tmp1 = tcp_data[:-1].split(" ")
            for i in range(len(tmp1)):
                tmp1[i] = int(tmp1[i])
            challenge.append(tmp1)
        else:
            response.append(int(tmp[:-1]))
f1.close()
#denied_i = 15
challenge.pop(15)
response.pop(15)
def pprint(A):
    flag = 0
    n = len(A)
    for i in range(0, n):
        line = ""
        for j in range(0, 41):
            if((GCD(A[i][j], p) % p) != 1 and (GCD(A[i][j], p) % p) != 0):
                flag += 1
            line += str((GCD(A[i][j], p) % p)) + " "
            if j == n:
                line += "| "
        print(line)
    print("")
    return flag

def gauss(A):
    n = len(A)
    sol_a = [0] * 40
    sol_b = [0] * 40

    for i in range(0, n):
        flag = 0
        # Search for coprime with p
        for k in range(i, n):
            if GCD(A[k][i],p) == 1:
                maxRow = k
                flag = 1
                break
        if flag == 0:
            print 'OMG'

        # Swap maximum row with current row (column by column)
        for k in range(i, n+2):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            tmp = inverse(A[i][i],p)
            if(GCD(A[i][i],p) != 1):
                print 'Ah....'
                print GCD(A[i][i],p)
                print GCD(A[k][i],p)
            c = (-A[k][i] * tmp) % p
            for j in range(i, n+2):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
                    A[k][j] = A[k][j] % p

    # Solve equation Ax=b for an upper triangular matrix A
    sol_a[39] = 1
    sol_b[39] = 0
 
    for i in range(38, -1, -1):
        tmp_a = 0
        tmp_b = (-A[i][40]) % p
        for j in range(0,40-i):
            tmp_a = (tmp_a + A[i][39-j]) % p
            tmp_b = (tmp_b + A[i][39-j]) % p
        tmp_inverse = inverse(p-A[i][i],p)
        sol_a[i] = (tmp_a * tmp_inverse) % p
        sol_b[i] = (tmp_b * tmp_inverse) % p    

    return (sol_a, sol_b)

challenge_sol = []
for i in range(39):
    tmp = []
    for j in challenge[i]:
        tmp.append(j)        
    tmp.append(response[i])
    challenge_sol.append(tmp)

(a,b) = gauss(challenge_sol)




'''
challenge_sol2=[]
for i in range(40):
    response[i] != sum(x*y%p for x, y in zip(challenge[i], key)):


cipher = AES.new(
            sha256(' '.join(map(str, key)).encode('utf-8')).digest(),
            AES.MODE_CFB,
            b'\0'*16)
print (cipher.decrypt(flag))
'''
