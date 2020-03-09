#include <stdio.h> // for perror
#include <string.h> // for memset
#include <unistd.h> // for close
#include <arpa/inet.h> // for htons
#include <netinet/in.h> // for sockaddr_in
#include <sys/socket.h> // for socket
#include <thread>
#include <mutex>
#include <list>
#include <vector>
#include <openssl/ssl.h>
#include <openssl/err.h>

using namespace std;

list<SSL *> client;
mutex m;

void usage() {
	printf("syntax : ssl_server <port> [-b]\n");
	printf("sample : ssl_server 1234 -b\n");
}

int isRoot() {
    if (getuid() != 0) {
        return 0;
    }
    else {
        return 1;
    }
}

SSL_CTX* InitServerCTX(void) {
    SSL_METHOD *method;
    SSL_CTX *ctx;
    OpenSSL_add_all_algorithms();  /* Load cryptos, et.al. */
    SSL_load_error_strings();   /* Bring in and register error messages */
    method = (SSL_METHOD *)TLSv1_2_server_method();  /* Create new server-method instance */
    ctx = SSL_CTX_new(method);   /* Create new context */
    if ( ctx == NULL )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    return ctx;
}

void LoadCertificates(SSL_CTX* ctx, char* CertFile, char* KeyFile) {
    /* set the local certificate from CertFile */
    if ( SSL_CTX_use_certificate_file(ctx, CertFile, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    /* set the private key from KeyFile (may be the same as CertFile) */
    if ( SSL_CTX_use_PrivateKey_file(ctx, KeyFile, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    /* verify private key */
    if ( !SSL_CTX_check_private_key(ctx) )
    {
        fprintf(stderr, "Private key does not match the public certificate\n");
        abort();
    }
}

void relay(SSL *ssl, int flag) {
    int childfd = SSL_get_fd(ssl);
    if(SSL_accept(ssl) == -1) {
        ERR_print_errors_fp(stderr);
        m.lock();
        client.remove(ssl);
        m.unlock();
    }
    else{
        while (true) {
            const static int BUFSIZE = 1024;
            char buf[BUFSIZE];
            m.lock();
            ssize_t received = SSL_read(ssl, buf, BUFSIZE - 1);
            if (received == 0 || received == -1) {
                perror("recv failed");
                client.remove(ssl);
                break;
            }
            m.unlock();
            printf("Recv from %d : ", childfd);
            buf[received] = '\0';
            printf("%s\n", buf);
            m.lock();
            if(flag) {
                for(auto i = client.begin(); i != client.end(); i++) {
                    ssize_t sent = SSL_write(*i, buf, strlen(buf));
                    if(sent == 0) {
                        perror("send failed");
                        client.remove((*i));
                    }
                }
            }
            m.unlock();
        }
    }
}

int main(int argc, char *argv[]) {
    if ((argc != 3) && (argc != 2)) {
		usage();
		return -1;
	}

    SSL_library_init();
    SSL_CTX *ctx = InitServerCTX();
    LoadCertificates(ctx, "test.com.pem", "test.com.pem");
    SSL * ssl;

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
		if (childfd < 0) {
			perror("ERROR on accept");
			break;
		}
		printf("connected\n");
        ssl = SSL_new(ctx);
        SSL_set_fd(ssl, childfd);
        m.lock();
        client.push_back(ssl);
        m.unlock();
        v_thread.push_back(thread(relay, ssl, flag));		
	}

	close(sockfd);
    SSL_CTX_free(ctx);
}

