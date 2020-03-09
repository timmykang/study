#include <stdio.h> // for perror
#include <string.h> // for memset
#include <unistd.h> // for close
#include <arpa/inet.h> // for htons
#include <netinet/in.h> // for sockaddr_in
#include <sys/socket.h> // for socket
#include <thread>
#include <mutex>
#include <set>
#include <vector>

using namespace std;

set<int> client;
mutex m;

void usage() {
	printf("syntax : echo_server <port> [-b]\n");
	printf("sample : echo_server 1234 -b\n");
}

void relay(int childfd, int flag) {
    while (true) {
        const static int BUFSIZE = 1024;
        char buf[BUFSIZE];
        m.lock();
        ssize_t received = recv(childfd, buf, BUFSIZE - 1, 0);
		if (received == 0 || received == -1) {
			perror("recv failed");
            client.erase(childfd);
			break;
		}
        m.unlock();
        printf("Recv from %d : ", childfd);
		buf[received] = '\0';
		printf("%s\n", buf);
        m.lock();
        if(flag) {
            for(auto i = client.begin(); i != client.end(); i++) {
                ssize_t sent = send(*i, buf, strlen(buf), 0);
                if(sent == 0) {
                    perror("send failed");
                    client.erase(*i);
                }
            }
        }
        m.unlock();
    }
}

int main(int argc, char *argv[]) {
    if ((argc != 3) && (argc != 2)) {
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

    if(argc == 3) {
        if(!(strcmp(argv[2], "-b")))
            flag = 1;
        else {
            printf("Option error\n");
            usage();
            exit(-1);
        }
    }

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
        printf("111\n");
		if (childfd < 0) {
			perror("ERROR on accept");
			break;
		}
		printf("connected\n");
        m.lock();
        client.insert(childfd);
        m.unlock();
        v_thread.push_back(thread(relay, childfd, flag));		
	}

	close(sockfd);
}

