all: web_proxy

web_proxy: main.o web_proxy.o
	g++ -g -o web_proxy main.o web_proxy.o -lpthread

web_proxy.o: web_proxy.cpp web_proxy.h
	g++ -g -c -o web_proxy.o web_proxy.cpp

main.o: main.cpp
	g++ -g -c -o main.o main.cpp

clean:
	rm -f web_proxy
	rm -f *.o