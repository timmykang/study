#include "web_proxy.h"

mutex m;
map<int, int> check_fd;
map<int, int> client_server;

bool check_request(char * packet) {
    const char * method[6] = {"GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS"};
    for(int i = 0; i < 6; i++) {
		if(!memcmp(packet, method[i], strlen(method[i])) && packet[strlen(method[i])] == 0x20)
            return true;
	}
	return false;
}

void get_tcpsock(int childfd) {
    while(true) {
        int i = 0;
        const static int BUFSIZE = 1024;
        char buf[BUFSIZE];
        ssize_t received = recv(childfd, buf, BUFSIZE - 1, 0);
        if (received == -1 || received ==0) {
            break;
        }
        if(!check_request(buf)) {
            break;
        }
        char host[50];
        const char * head_host = "Host: ";
        char * tmp = strstr((char *)buf, head_host);
        if(tmp == NULL) {
            printf("No host");
            break;
        }
        while(tmp[i + strlen(head_host)] != 0x0d) {
            host[i] = tmp[i+strlen(head_host)];
            i++;
        }
        printf("Host : %s\n", host);

        struct hostent * host_entry = gethostbyname(host);
        char * ip_addr = inet_ntoa(*((struct in_addr*)host_entry->h_addr_list[0]));
        int sockfd = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(80);
        if(!inet_aton(ip_addr, &addr.sin_addr)) {
            printf("ip error\n");
            exit(1);
        }
        memset(addr.sin_zero, 0, sizeof(addr.sin_zero));
        int res = connect(sockfd, reinterpret_cast<struct sockaddr*>(&addr), sizeof(struct sockaddr));
        if (res == -1) {
            perror("connect failed");
            exit(1);
        }
        printf("%s",buf);
        ssize_t sent = send(sockfd, buf, strlen(buf), 0);
        check_fd[childfd] = 2;
        check_fd[sockfd] = 2;
        client_server[childfd] = sockfd;
        break;
    }
}

void relay(int To_fd, int From_fd)
{
    if(To_fd == 0 || From_fd == 0)
        return;
    printf("To : %d\n", To_fd);
    printf("From : %d\n",From_fd);
    while(true) {
        if(check_fd[From_fd] == 2) {
            if(check_fd[To_fd] == 0) {
                check_fd.erase(To_fd);
                check_fd.erase(From_fd);
                break;
            }
            const static int BUFSIZE = 1024;
            char buf[BUFSIZE];
            ssize_t received = recv(From_fd, buf, BUFSIZE - 1, 0);
            if (received == -1) {
                printf("received failed\n");
                check_fd[From_fd] = 0;
                break;
            }        
            else if (received == 0) {
                check_fd[From_fd] = 1;
            }
            else {
                printf("%s\n", buf);
                ssize_t sent = send(To_fd, buf, strlen(buf), 0);
                check_fd[To_fd] = 2;
            }
        }
    }
}
