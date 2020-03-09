#include "web_proxy.h"

void usage() {
	printf("syntax : web_proxy <tcp port>\n");
	printf("sample : web_proxy 8080\n");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
		usage();
		return -1;
	}

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		perror("socket failed");
		return -1;
	}

	int optval = 1;
    int flag = 0;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,  &optval , sizeof(int));

	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(atoi(argv[1]));
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	memset(addr.sin_zero, 0, sizeof(addr.sin_zero));

	int res = bind(sockfd, reinterpret_cast<struct sockaddr*>(&addr), sizeof(struct sockaddr));
	if (res == -1) {
		perror("bind failed");
		return -1;
	}

	res = listen(sockfd, 2);
	if (res == -1) {
		perror("listen failed");
		return -1;
	}
    vector<thread> v_thread;
	while (true) {
		struct sockaddr_in addr;
		socklen_t clientlen = sizeof(sockaddr);
		int childfd = accept(sockfd, reinterpret_cast<struct sockaddr*>(&addr), &clientlen);
		if (childfd < 0) {
			perror("ERROR on accept");
			break;
		}
        //v_thread.push_back(thread(get_tcpsock, childfd));
        get_tcpsock(childfd);
        v_thread.push_back(thread(relay, childfd, client_server[childfd]));
        v_thread.push_back(thread(relay, client_server[childfd], childfd));
	}

	close(sockfd);
}
