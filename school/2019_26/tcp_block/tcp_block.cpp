#include "tcp_block.h"

uint16_t calculate(uint16_t * data, int len) {
	uint16_t result;
	int tempChecksum = 0;
	int length;
	bool flag = false;
	if((len % 2) == 0)
		length = len / 2;
	else {
			length = (len / 2) + 1;
			flag = true;
	}
			
	for (int i = 0; i < length; ++i) { 
		if(i == length - 1 && flag)
			tempChecksum += ntohs(data[i] & 0x00ff);
		else
			tempChecksum += ntohs(data[i]);
		if(tempChecksum > CARRY)
			tempChecksum = (tempChecksum - CARRY) + 1;
	}
	result = tempChecksum;
	return result;
}

uint16_t ip_checksum(uint8_t * ip_packet) {
	struct ip_header * iph = (struct ip_header *) ip_packet;
	iph -> checksum = 0;
	uint16_t checksum = calculate((uint16_t *)iph, ((iph -> ver_hl) & 0x0f) * 4);
	iph -> checksum = htons(checksum ^ 0xffff);
	return checksum;
}

uint16_t tcp_checksum(uint8_t * ip_packet, int len) {
	struct Pseudoheader pseudoheader;
	struct ip_header * iph = (struct ip_header *)data;
	struct tcp_header * tcph = (struct tcp_header *)(data + ((iph -> ver_hl) & 0x0f) * 4);
	
	memcpy(&pseudoheader.src, &iph -> ip_src, sizeof(pseudoheader.src));
	memcpy(&pseudoheader.dest, &iph -> ip_dst, sizeof(pseudoheader.dest));
	pseudoheader.protocol = iph -> p;
	pseudoheader.tcp_len = htons(dataLen - ((iph -> (iph -> ver_hl) & 0x0f) * 4));
	uint16_t pseudoResult = calculate((uint16_t *)&pseudoheader, sizeof(pseudoheader));
	
	tcph -> checksum = 0;
	uint16_t tcpHeaderResult = calculate((uint16_t *)tcph, ntohs(pseudoheader.tcp_len));
	uint16_t checksum;
	int tempCheck;
	if((tempCheck = pseudoResult + tcpHeaderResult) > CARRY)
		checksum = (tempCheck - CARRY) + 1;
	else
		checksum = tempCheck;
	checksum = ntohs(checksum ^ 0xffff); 
	tcph -> checksum = checksum;
	
	return checksum;
}

void forward_rst(pcap_t * handle, uint8_t* pkt) {
	struct ip_header * rcvpacket_ip = (struct ip_header *)(pkt + 14);	
	int ip_len = (rcvpacket_ip -> ver_hl & 0x0f) * 4;
	int tcp_len = (rcvpacket_tcp -> tcp_len & 0xf0) / 4;
	int http_len = ntohs(*((uint16_t*)(rcvpkt + eth_hdr_len + 2))) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);

	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	packet_ip -> len = htons(ip_len + tcp_len);
	packet_tcp -> flag = 0x14;
	packet_tcp -> seq_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	packet_ip -> checksum = 0;
	packet_ip -> checksum = htons(ip_checksum(packet + 14, ip_len));
	packet_tcp -> checksum = 0;
	packet_tcp -> checksum = htons(ip_checksum(packet + 14, tcp_len);
	pcap_sendpacket(handle, packet, eth_hdr_len + ip_len + tcp_len);
}

void forward_fin(pcap_t* handle, uint8_t* pkt) {
	struct ip_header * rcvpacket_ip = (struct ip_header *)(pkt + 14);	
	int ip_len = (rcvpacket_ip -> ver_hl & 0x0f) * 4;
	int tcp_len = (rcvpacket_tcp -> tcp_len & 0xf0) / 4;
	int http_len = ntohs(*((uint16_t*)(rcvpkt + eth_hdr_len + 2))) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);
	struct pcap_pktheader * header;
	
	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	packet_ip -> len = htons(ip_len + tcp_len);
	packet_tcp -> flag = 0x11;
	packet_tcp -> seq_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	
void backward_rst(pcap_t* handle, uint8_t* pkt, int ip_len, int tcp_len, int http_len)
void backward_fin(pcap_t* handle, uint8_t* pkt, int ip_len, int tcp_len, int http_len)

uint16_t tcp_checksum(uint8_t* ip_packet, int ip_len, int tcp_len, int http_len)
