all: ssl_client ssl_server

ssl_client: ssl_client.cpp
	g++ -Wall -o ssl_client ssl_client.cpp -L/usr/lib -pthread -lssl -lcrypto

ssl_server: ssl_server.cpp
	g++ -Wall -o ssl_server ssl_server.cpp -L/usr/lib -pthread -lssl -lcrypto

clean:
	rm ssl_client ssl_server

