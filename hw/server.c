#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<netinet/in.h>
#include<sys/socket.h>
#define UDP_PORT 4900
int main(int argc, char** argv)
{
	int sockfd,n;
	struct sockaddr_in servaddr, cliaddr;
	socklen_t clisize;
	char sendline[BUFSIZ];
	char recvline[BUFSIZ];
	sockfd=socket(AF_INET, SOCK_DGRAM, 0);
	memset(&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family=AF_INET;
	servaddr.sin_addr.s_addr=htonl(INADDR_ANY);
	servaddr.sin_port=htons(UDP_PORT);
	bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
	clisize = sizeof(cliaddr);
	n=recvfrom(sockfd, recvline, BUFSIZ, 0, (struct sockaddr *)&cliaddr, &clisize);
	recvline[n]='\0';
	if(strcmp(recvline,"Hello\n") != 0)
	{
		close(sockfd);
		return 0;
	}
	printf("Clilent : %s\n",recvline);
	while(1)
	{
		printf("Server : ");
		fgets(sendline,BUFSIZ,stdin);
		printf("\n");
		n=sendto(sockfd, sendline, BUFSIZ, 0, (struct sockaddr *)&cliaddr, sizeof(cliaddr));
		clisize=sizeof(cliaddr);
		n=recvfrom(sockfd, recvline, BUFSIZ, 0, (struct sockaddr *)&cliaddr, &clisize);
		recvline[n]='\0';
		if(!strcmp(recvline,"Bye\n"))
		{
			close(sockfd);
			return 0;
		}
		printf("Client: %s\n", recvline);
	}
}
