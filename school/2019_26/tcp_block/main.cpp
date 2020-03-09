#include "tcp_block.h"

uint8_t my_mac[6], my_ip[4];
const char* HTTP_METHOD[] = {"GET","POST","HEAD","PUT","DELETE","OPTIONS"};
const char warning[7]="block!";

void usage() {
	printf("syntax : tcp_block <interface> <host>\n");
	printf("sample : tcp_block wlan0 test.gilgil.net\n");
}

int main(int argc, char * argv[]) {
	if (argc != 3) {
		usage();
		return -1;
	}
	char * interface = argv[1];
    char * block_site = argv[2];
	char errbuf[PCAP_ERRBUF_SIZE];
	struct pcap_pkthdr * header;	
	pcap_t * fp = pcap_open_live(interface, BUFSIZ, 1, 1, errbuf);
	if (fp == NULL) {
		printf("ERROR3\n");
		exit(1);
	}
	get_my_ip(interface);
	get_my_mac(interface);
	uint8_t * pkt;
	while(1) {
		int res = pcap_next_ex(fp, &header, (const u_char **)&pkt);
		if(res == 0) continue;
        if(res == -1 || res == -2) {
            pcap_close(fp);
            return 0;
        }
        struct ether_header * packet_ether = (struct ether_header *)pkt;
        if(ntohs(packet_ether -> type) != 0x0800) continue;
        struct ip_header * packet_ip = (struct ip_header *)(pkt + 14);
        int ip_len = (packet_ip -> ver_hl & 0x0f) * 4;
        if(packet_ip -> p != 6) continue;
        struct tcp_header * packet_tcp = (struct tcp_header *)(pkt + 14 + ip_len);
        int tcp_len = (packet_tcp -> tcp_len & 0xf0) / 4;
        int http_len = ntohs(packet_ip -> len) - ip_len - tcp_len;
        if(http_len < 7) continue;
        uint8_t * packet_http = pkt + 14 + ip_len + tcp_len;
        int i;
        for(i = 0; i < 6; ++i){
			if(memcmp(HTTP_METHOD[i], packet_http, strlen(HTTP_METHOD[i])) != 0)
				break;
		}
        if(i == 6) continue;
        for(i = 0; i < http_len - 6; i++) {
            if(!memcmp(packet_http + i, "Host: ", 6)) {
                if(!memcmp(packet_http + i + 6, block_site, strlen(block_site))) {
                    forward_rst(fp, pkt);
                    backward_fin(fp, pkt, warning);
                }
            }
        }
    }
    pcap_close(fp);
	return 0;
}
