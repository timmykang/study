#include "tcp_block.h"

void get_my_ip(char * interface) {
	struct ifreq ifr;
	struct sockaddr_in * sin;
	uint32_t s;

	s = socket(AF_INET, SOCK_DGRAM, 0);
	strncpy(ifr.ifr_name, interface, IFNAMSIZ);

	if (ioctl(s, SIOCGIFADDR, &ifr) < 0) {
		printf("Error0\n");
		close(s);
		exit(1);
  } 
	else {
		sin = (struct sockaddr_in *)&ifr.ifr_addr;
  	memcpy(my_ip, (void*)&sin->sin_addr, sizeof(sin->sin_addr));
		close(s);
  }
}

void get_my_mac(char * interface) {
	int sock;
	struct ifreq ifr;
	char mac_adr[18] = {0,};

	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)	{
		printf("ERROR1\n");
		exit(1);
	}
	strcpy(ifr.ifr_name, interface);

	if (ioctl(sock, SIOCGIFHWADDR, &ifr)< 0) {
		printf("ERROR1\n");
		close(sock);
		exit(1);
	}
	
	memcpy(my_mac, (struct ether_addr *)(ifr.ifr_hwaddr.sa_data), 6);
	close(sock);
}

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
	int http_len = ntohs(rcvpacket_ip -> len) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);
	struct ether_header * packet_ether = (struct ether_header *)(packet);

	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	memcpy(packet_ether -> shost, my_mac, 6);
	packet_ip -> tos = 0x44;
	packet_ip -> len = htons(ip_len + tcp_len);
	packet_ip -> ttl = 0xff;
	packet_tcp -> flag = 0x14;
	packet_tcp -> seq_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	packet_tcp -> window_size = 0;
	packet_tcp -> urg_ptr = 0;
	packet_ip -> checksum = 0;
	packet_ip -> checksum = htons(ip_checksum(packet + 14));
	packet_tcp -> checksum = 0;
	packet_tcp -> checksum = htons(ip_checksum(packet + 14, ntohs(packet_ip -> len));
	pcap_sendpacket(handle, packet, 14 + ntohs(packet_ip -> len));
}

void forward_fin(pcap_t* handle, uint8_t* pkt, char * data) {
	struct ip_header * rcvpacket_ip = (struct ip_header *)(pkt + 14);	
	int ip_len = (rcvpacket_ip -> ver_hl & 0x0f) * 4;
	int tcp_len = (rcvpacket_tcp -> tcp_len & 0xf0) / 4;
	int http_len = ntohs(rcvpacket_ip -> len) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len + strlen(data)];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);
	struct ether_header * packet_ether = (struct ether_header *)(packet);
	
	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	memcpy(packet + 14 + ip_len + tcp_len, data, strlen(data));
	packet_ip -> tos = 0x44;
	packet_ip -> len = htons(ip_len + tcp_len + strlen(data));
	packet_ip -> ttl = 0xff;
	packet_tcp -> flag = 0x11;
	packet_tcp -> seq_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	packet_tcp -> window_size = 0;
	packet_tcp -> urg_ptr = 0;
	packet_ip -> checksum = 0;
	packet_ip -> checksum = htons(ip_checksum(packet + 14));
	packet_tcp -> checksum = 0;
	packet_tcp -> checksum = htons(ip_checksum(packet + 14, ntohs(packet_ip -> len));
	pcap_sendpacket(handle, packet, 14 + ntohs(packet_ip -> len));
}

void backward_rst(pcap_t* handle, uint8_t* pkt) {
	struct ip_header * rcvpacket_ip = (struct ip_header *)(pkt + 14);	
	int ip_len = (rcvpacket_ip -> ver_hl & 0x0f) * 4;
	int tcp_len = (rcvpacket_tcp -> tcp_len & 0xf0) / 4;
	int http_len = ntohs(rcvpacket_ip -> len) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);
	struct ether_header * packet_ether = (struct ether_header *)(packet);
	struct ether_header * rcvpacket_ether = (struct ether_header *)(pkt);

	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	memcpy(packet_ether -> dhost, rcvpacket_ether -> shost, 6);
	memcpy(packet_ether -> shost, my_mac, 6);
	memcpy(packet_ip -> ip_src, rcvpacket_ip -> ip_src, 4);
	memcpy(packet_ip -> ip_dst, rcvpacket_ip -> ip_dst, 4);
	memcpy(packet_tcp -> src, rcvpacket_tcp -> src, 2);
	memcpy(packet_tcp -> dst, rcvpacket_tcp -> dst, 2);
	packet_ip -> tos = 0x44;
	packet_ip -> len = htons(ip_len + tcp_len);
	packet_ip -> ttl = 0xff;
	packet_tcp -> flag = 0x14;
	packet_tcp -> seq_num = rcvpacket_tcp -> ack_num;
	packet_tcp -> ack_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	packet_tcp -> window_size = 0;
	packet_tcp -> urg_ptr = 0;
	packet_ip -> checksum = 0;
	packet_ip -> checksum = htons(ip_checksum(packet + 14));
	packet_tcp -> checksum = 0;
	packet_tcp -> checksum = htons(ip_checksum(packet + 14, ntohs(packet_ip -> len));
	pcap_sendpacket(handle, packet, 14 + ntohs(packet_ip -> len));
}

void backward_fin(pcap_t* handle, uint8_t* pkt, char * data) {
	struct ip_header * rcvpacket_ip = (struct ip_header *)(pkt + 14);	
	int ip_len = (rcvpacket_ip -> ver_hl & 0x0f) * 4;
	int tcp_len = (rcvpacket_tcp -> tcp_len & 0xf0) / 4;
	int http_len = ntohs(rcvpacket_ip -> len) - ip_len - tcp_len;
	struct tcp_header * rcvpacket_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
	uint8_t packet[14 + ip_len + tcp_len + strlen(data)];
	struct ip_header * packet_ip = (struct ip_header *)(packet + 14);
	struct tcp_header * packet_tcp = (struct tcp_header *)(packet + 14 + ip_len);
	struct ether_header * packet_ether = (struct ether_header *)(packet);
	struct ether_header * rcvpacket_ether = (struct ether_header *)(pkt);

	memcpy(packet, pkt, 14 + ip_len + tcp_len);
	memcpy(packet_ether -> dhost, rcvpacket_ether -> shost, 6);
	memcpy(packet_ether -> shost, my_mac, 6);
	memcpy(packet_ip -> ip_src, rcvpacket_ip -> ip_src, 4);
	memcpy(packet_ip -> ip_dst, rcvpacket_ip -> ip_dst, 4);
	memcpy(packet_tcp -> src, rcvpacket_tcp -> src, 2);
	memcpy(packet_tcp -> dst, rcvpacket_tcp -> dst, 2);
	memcpy(packet + 14 + ip_len + tcp_len, data, strlen(data));

	packet_ip -> tos = 0x44;
	packet_ip -> len = htons(ip_len + tcp_len + strlen(data));
	packet_ip -> ttl = 0xff;
	packet_tcp -> flag = 0x11;
	packet_tcp -> seq_num = rcvpacket_tcp -> ack_num;
	packet_tcp -> ack_num = htonl(ntohl(rcvpacket_tcp -> seq_num) + http_len);
	packet_tcp -> window_size = 0;
	packet_tcp -> urg_ptr = 0;
	packet_ip -> checksum = 0;
	packet_ip -> checksum = htons(ip_checksum(packet + 14));
	packet_tcp -> checksum = 0;
	packet_tcp -> checksum = htons(ip_checksum(packet + 14, ntohs(packet_ip -> len));
	pcap_sendpacket(handle, packet, 14 + ntohs(packet_ip -> len));
}
