#include "Graph.h"
#include <string>
#include <fstream>
#include <bits/stdc++.h>

void
Graph::readFile(const char* in)
{
	ifstream infile(in);	/**< Input file stream. */
	string line;		/**< One line of the file. */
	int from;		/**< Node number of where an edge starts. */
	int to;			/**< Node number of where an edge ends. */
	char input;		/**< The input that triggers the transition. */

	while(getline(infile, line)) {
		/** Split a line. */
		stringstream chk(line);
		vector<string> tokens;
		string inter;
		while(getline(chk, inter, ' '))
			tokens.push_back(inter);

		/** Create an edge for a line. */
		if(tokens.size() < 2) {
			cout<<"Format error"<<endl;
			exit(0);
		} else if(tokens.size() == 2) {
			insertEdge(atoi(tokens[0].c_str()), atoi(tokens[1].c_str()), 0);
		} else if(tokens.size() == 3) {
			insertEdge(atoi(tokens[0].c_str()), atoi(tokens[1].c_str()), tokens[2].c_str()[0]);
		} else {
			cout<<"Format error"<<endl;
			exit(0);
		}
	}
}

void
Graph::insertEdge(int from, int to, char input)
{
	Edge edge(from, to, input);
	m_vecEdges.push_back(edge);
}

void
Graph::print(ostream& os) const
{
	vector<Edge> sorted = m_vecEdges;
	sort(sorted.begin(), sorted.end());
	for(int i=0; i<sorted.size(); i++)
		os<<sorted[i];
}

Set
Graph::getEClosure(int s)
{
	Set ret;
	ret.insert(s);
	for(vector<Edge>::iterator it=m_vecEdges.begin(); it!=m_vecEdges.end(); ++it)
		if(it->getFrom() == s && it->getInput() == 0) {
			ret.insert(it->getTo());
			ret |= getEClosure(it->getTo());
		}
	return ret;
}

Set
Graph::getEClosure(Set T)
{
	Set ret;
	for(Set::iterator it=T.begin(); it!=T.end(); ++it)
		ret |= getEClosure(*it);
	return ret;
}

Set
Graph::move(Set T, char a)
{
	Set ret;
	for(Set::iterator s=T.begin(); s!=T.end(); ++s)
		for(vector<Edge>::iterator e=m_vecEdges.begin(); e!=m_vecEdges.end(); ++e)
			if((e->getFrom()) == (*s) && (e->getInput()) == a)
				ret.insert(e->getTo());
	return ret;
}
