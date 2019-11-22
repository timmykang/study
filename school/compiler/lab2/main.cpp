#include "Graph.h"

int
main(int argc, char* argv[])
{
	Graph NFA;			/**< The input NFA. */
	Graph DFA;			/**< The output DFA. */
	char sigma[] = {'a', 'b'};	/**< The set of possible inputs. */
	vector<Set> Dstate;		/**< The set of states in DFA. */
	int T = 0;			/**< The state number in DFA. */

	if(argc<2) {
		cerr<<"Usage : "<<argv[0]<<" <input file>"<<endl;
		return 1;
	}
	
	NFA.readFile(argv[1]);
	Dstate.push_back(NFA.getEClosure(0));
	Set tmp;
	int tmp1 = 0;
	int flag = 0;
	while(1) {
		for(int j=0; j<sizeof(sigma); j++)
		{
			tmp = NFA.getEClosure(NFA.move(Dstate[tmp1],sigma[j]));
			for(int i=0; i<Dstate.size(); i++) {
				if(tmp == Dstate[i]) {
					DFA.insertEdge(tmp1, i, sigma[j]);
					flag = 1;
					break;
				}
			}
			if(flag == 0) {
				Dstate.push_back(tmp);
				DFA.insertEdge(tmp1, Dstate.size()-1, sigma[j]);
			}
			flag = 0;
		}
		tmp1 = tmp1+1;
		if(tmp1 == Dstate.size())
			break;
	}
	
	cout<<DFA;
	return 0;
}
