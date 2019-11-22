all: arp_spoof

arp_spoof: main.o arp_spoof.o
	g++ -g -o arp_spoof main.o arp_spoof.o -lpcap -lpthread

arp_spoof.o: arp_spoof.cpp arp_spoof.h
	g++ -g -c -o arp_spoof.o arp_spoof.cpp

main.o: main.cpp arp_spoof.h
	g++ -g -c -o main.o main.cpp

clean:
	rm -f arp_spoof *.o
