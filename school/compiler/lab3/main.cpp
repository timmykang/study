#include "Prod.h"

int
main(int argc, char* argv[])
{
	Prod P;

	if(argc<2) {
		cerr<<"Usage : "<<argv[0]<<" <input file>"<<endl;
		return 1;
	}

	P.readFile(argv[1]);
	//cout<<P;
	P.computeFirst();
	P.computeFollow();

	return 0;
}
