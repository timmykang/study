#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main(int argc, char* argv[]){
	char text[20]="AAAAAAAAAAAAAAAAAAAA";
	strcpy(text, argv[1]);
	printf(text);
	return 0;
}
