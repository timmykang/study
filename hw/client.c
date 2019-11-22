#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<netinet/in.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#define UDP_PORT 4900
#define IP_ADDR "127.0.0.1"
int main(int argc, char** argv)
{
	int sockfd, n;
	socklen_t clisize;
	struct sockaddr_in servaddr, cliaddr;
	char sendline[BUFSIZ];
	char recvline[BUFSIZ];
	sockfd=socket(AF_INET, SOCK_DGRAM, 0); 
	memset(&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family=AF_INET;
	servaddr.sin_addr.s_addr = inet_addr(IP_ADDR);
	servaddr.sin_port=htons(UDP_PORT);
	printf("Client : ");
	fgets(sendline, BUFSIZ, stdin);
	printf("\n");
	sendto(sockfd, sendline, strlen(sendline), 0, (struct sockaddr *)&servaddr, sizeof(servaddr));
	while(1)
	{
		clisize=sizeof(cliaddr);
		n=recvfrom(sockfd, recvline, BUFSIZ, 0, (struct sockaddr*)&cliaddr, &clisize);
		recvline[n]='\0';
		printf("Server : %s\n",recvline);
		printf("Client : ");
		fgets(sendline,BUFSIZ, stdin);
		printf("\n");
		if(!strcmp(sendline, "Bye\n"))
		{
			sendto(sockfd, sendline, strlen(sendline), 0, (struct sockaddr *)&servaddr, sizeof(servaddr));
			break;
		}
		sendto(sockfd, sendline, strlen(sendline), 0, (struct sockaddr *)&servaddr, sizeof(servaddr));
	}
	close(sockfd);
	return 0;
}
