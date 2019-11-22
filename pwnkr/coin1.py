from pwn import *
import time
import sys

host = "pwnable.kr"
port = 9007

r = remote(host, port)
time.sleep(3)           # wait for 3 sec.

print r.recv()

cnt = 0
for i in range(100):
    r.recvuntil('N=')
    n = int( r.recvuntil(' ') )
    r.recvuntil('C=')
    c = int( r.recv() )
    
    st = 1
    des = n
    t = 0
    while(1):
        
        message = ''
        
        if(st > des):
            break
        
        message = ''
        for i in range(st, (st + des) // 2 + 1):
            message += '{0} '.format(i) 
        
        print "[-] guess : {0}".format(message)
        x = r.sendline(message)
        result = r.recv()
        
        print "[*] result : {0}".format(result)

        if result.find('Correct') > -1:
            t = 1
            break
        elif result[0] == 'N':
            des = n
        elif result.find('error') > -1:
            break
        elif result.find('time') > -1:
            print "\n\n[x] time expired.."
            sys.exit(1)
        elif int(result) % 10 != 0:
            des = (st + des)//2
        else:
            st = (st+des)//2 + 1
    if(t == 0):
        r.sendline(str(st))
        correctmsg = r.recv()
    cnt += 1
    print "[+] count : {0}\n".format(cnt)

flag = r.recv()
print "\n\n[*] FLAG : {0}".format(flag)

