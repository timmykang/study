#include <stdio.h> // for perror
#include <string.h> // for memset
#include <unistd.h> // for close
#include <arpa/inet.h> // for htons
#include <netinet/in.h> // for sockaddr_in
#include <sys/socket.h> // for socket
#include <thread>

using namespace std;

void usage() {
	printf("syntax : echo_client <host> <port>\n");
	printf("sample : echo_client 127.0.0.1 1234\n");
}

void RECV(int sockfd) {
    while (true) {
        const static int BUFSIZE = 1024;
        char buf[BUFSIZE];
        
        ssize_t received = recv(sockfd, buf, BUFSIZE - 1, 0);
		if (received == 0 || received == -1) {
			perror("recv failed");
			break;
		}
		buf[received] = '\0';
		printf("%s\n", buf);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
		usage();
		return -1;
	}

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		perror("socket failed");
		return -1;
	}

	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(atoi(argv[2]));
	addr.sin_addr.s_addr = inet_addr(argv[1]);
	memset(addr.sin_zero, 0, sizeof(addr.sin_zero));

	int res = connect(sockfd, reinterpret_cast<struct sockaddr*>(&addr), sizeof(struct sockaddr));
	if (res == -1) {
		perror("connect failed");
		return -1;
	}
	printf("connected\n");
    thread Thread(RECV, sockfd);
	while (true) {
		const static int BUFSIZE = 1024;
		char buf[BUFSIZE];

		scanf("%s", buf);
		if (strcmp(buf, "quit") == 0) break;

		ssize_t sent = send(sockfd, buf, strlen(buf), 0);
		if (sent == 0) {
			perror("send failed");
			break;
		}
	}
    Thread.join();
	close(sockfd);
}

