#include<stdio.h>
#include<stdint.h>
uint16_t my_ntohs(uint16_t n){
	return ((n & 0xFF00) >> 8) | ((n & 0x00FF) << 8);
}
uint32_t my_ntohl(uint32_t n){
	return ((n & 0xFF000000) >> 24) | ((n & 0x00FF0000) >> 8) | ((n & 0x0000FF00) << 8) | ((n & 0x000000FF) << 24);
}
int main(){
	{
		unsigned char packet[] = {0x12, 0x34};
		uint16_t *p = (uint16_t *)packet;
		uint16_t port = my_ntohs(*p);
		printf("%x\n", port);
	}
	{	
		unsigned char packet[] = {0x12, 0x34, 0x56, 0x78};
		uint32_t *p = (uint32_t *)packet;
		uint32_t ip = my_ntohl(*p);
		printf("%x\n", ip);
	}
}

