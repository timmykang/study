import dpkt
from Crypto.Util.number import *
f1 = open('newfile.pcap')
pcap = dpkt.pcap.Reader(f1)
flag = ''
challenge = []
response = []  
p = 21652247421304131782679331804390761485569
## (311*313*317*331*337*347*349*353)^2
for ts, pkt in pcap:
    tmp = dpkt.ethernet.Ethernet(pkt).data.data.data
    if(len(str(tmp)) != 0):
        tmp1 = []
        tcp_data = str(tmp)
        if('ACCESS' in tcp_data):
            flag = tcp_data[15:-1]
        elif(len(tcp_data) > 200):
            tmp1 = tcp_data[:-1].split(" ")
            for i in range(len(tmp1)):
                tmp1[i] = int(tmp1[i])
            challenge.append(tmp1)
        else:
            response.append(int(tmp[:-1]))
f1.close()