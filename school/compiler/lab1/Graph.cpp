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
	Set a;
	vector<int> tmp;
	vector<int> tmp1;
	tmp.push_back(s);
	while(1)
	{
		for(int i=0; i<tmp.size(); i++)
		{
			for(int j=0; j<m_vecEdges.size(); j++)
			{
				if(m_vecEdges[j].getFrom() == tmp[i] && m_vecEdges[j].getInput() ==0)
				{
					if(a.find(m_vecEdges[j].getTo()) == a.end() && find(tmp.begin(), tmp.end(), m_vecEdges[j].getTo()) == tmp.end() && find(tmp1.begin(), tmp1.end(), m_vecEdges[j].getTo()) == tmp1.end())
					{
						//printf("%d\n",m_vecEdges[j].getTo());
						tmp1.push_back(m_vecEdges[j].getTo());
					}
				}
			}
			a.insert(tmp[i]);
		}
		tmp.clear();
		if(tmp1.size() == 0)
		{
			break;
		}
		else
		{
			for(int i=0; i<tmp1.size(); i++)
			{
				tmp.push_back(tmp1[i]);
			}
		}
		tmp1.clear();
	}
	return a; 
}

Set
Graph::getEClosure(Set T)
{
	Set a;
	Set tmp;
	for(Set::iterator it=T.begin(); it!=T.end(); ++it)
	{
		tmp = getEClosure(*it);
		a=a|tmp;
	}
	return a;
}

Set
Graph::move(Set T, char a)
{
	Set b = getEClosure(T);
	Set c;
	for(int i=0; i<b.size(); i++)
	{
		for(int j=0; j<m_vecEdges.size(); j++)
		{
			if(m_vecEdges[j].getInput() == a && b.find(m_vecEdges[j].getFrom()) != b.end())
				c.insert(m_vecEdges[j].getTo());
		}
	}
	return c;
}
