#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <list>
#include "gmem.h"
using namespace std;

struct Obj
{
	uint64_t something;
};

void vector_test()
{
	vector<uint64_t> v;
	//v.reserve(5);
	v.push_back(1); //1
	v.push_back(3); //2
	v.push_back(5); //4
	v.push_back(2);
	v.push_back(4); //8
	v.push_back(7);
	v.push_back(9);
	v.push_back(8);
	v.push_back(6); //16
	for(vector<uint64_t>::iterator it = v.begin(); it != v.end(); it++)
		cout << *it << endl;
}

void set_test();
void map_test();
void unordered_set_test();
void list_test()
{
	list<uint64_t> l;
	l.push_back(1);
	l.push_back(2);
	l.push_back(3);
	l.push_back(5);
	l.push_back(4);

	for(list<uint64_t>::iterator it = l.begin(); it != l.end(); it++) 
		cout << *it << endl;
}

int main() {
	gmem_set_verbose(true);
	printf("Call vector_test\n");
	vector_test();
	//printf("Call list_test\n");
	//list_test();
	return 0;
}
