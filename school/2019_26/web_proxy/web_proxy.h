#include <stdio.h> // for perror
#include <string.h> // for memset
#include <stdlib.h>
#include <unistd.h> // for close
#include <arpa/inet.h> // for htons
#include <netinet/in.h> // for sockaddr_in
#include <sys/socket.h> // for socket
#include <netdb.h>
#include <thread>
#include <mutex>
#include <set>
#include <map>
#include <vector>
#include <openssl/ssl.h>
#include <openssl/err.h>

using namespace std;
extern mutex m;
extern map<int, int> check_fd;
extern map<int, int> client_server;

bool check_request(char * packet);
void get_tcpsock(int childfd);
void relay(int To_fd, int From_fd);


