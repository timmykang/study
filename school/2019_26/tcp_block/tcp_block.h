#pragma once
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <string.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>
#include <pcap.h>
#include <map>
#include <vector>

using namespace std;

extern uint8_t my_mac[6], my_ip[4];


struct Pseudoheader{
    uint32_t src;
    uint32_t dest;
    uint8_t reserved=0;
    uint8_t protocol;
    uint16_t tcp_len;
};

struct ether_header {
	uint8_t	dhost[6];
	uint8_t	shost[6];
	uint16_t type;
};

struct ip_header {
	uint8_t ver_hl;		
	uint8_t tos;		
	uint16_t len;		
	uint16_t id;		
	uint16_t off;		
#define IP_RF 0x8000		
#define IP_DF 0x4000		
#define IP_MF 0x2000		
#define IP_OFFMASK 0x1fff	
	uint8_t ttl;		
	uint8_t p;		
	uint16_t checksum;		
	uint32_t ip_src,ip_dst; 
};
#define IP_HL(ip)		(((ip)->ip_vhl) & 0x0f)
#define IP_V(ip)		(((ip)->ip_vhl) >> 4)

struct tcp_header {
	uint16_t src;
	uint16_t dst;
	uint32_t seq_num;
	uint32_t ack_num;
	uint8_t tcp_len;
	uint8_t flag;
	uint16_t window_size;
	uint16_t checksum;
	uint16_t urg_ptr;
};

void get_my_ip(char * interface);
void get_my_mac(char * interface);
void forward_rst(pcap_t * handle, uint8_t * pkt);
void forward_fin(pcap_t * handle, uint8_t * pkt, const char * data);
void backward_rst(pcap_t * handle, uint8_t * pkt);
void backward_fin(pcap_t * handle, uint8_t * pkt, const char * data);
uint16_t ip_checksum(uint8_t * ip_packet);
uint16_t tcp_checksum(uint8_t * ip_packet, int ip_len);
