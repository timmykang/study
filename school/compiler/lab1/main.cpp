#include "Graph.h"

int
main(int argc, char* argv[])
{
	Graph NFA;			/**< The input NFA. */
	Set A, B, C, D, E;		/**< Sets for test. */

	if(argc<2) {
		cerr<<"Usage : "<<argv[0]<<" <input file>"<<endl;
		return 1;
	}
	NFA.readFile(argv[1]);

	A = NFA.getEClosure(0);
	B = NFA.getEClosure(NFA.move(A, 'a'));
	C = NFA.getEClosure(NFA.move(A, 'b'));
	D = NFA.getEClosure(NFA.move(B, 'b'));
	E = NFA.getEClosure(NFA.move(D, 'b'));
	cout<<A;
	cout<<B;
	cout<<C;
	cout<<D;
	cout<<E;

	return 0;
}
