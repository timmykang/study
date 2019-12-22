all: echo_client echo_server

echo_client: echo_client.cpp
	g++ -o echo_client echo_client.cpp -pthread

echo_server: echo_server.cpp
	g++ -o echo_server echo_server.cpp -pthread

clean:
	rm echo_client echo_server

