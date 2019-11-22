#include "Prod.h"
#include <fstream>
#include <bits/stdc++.h>

void
Prod::readFile(const char* in)
{
	ifstream infile(in);	/**< Input file stream. */
	string line;		/**< One line of the file. */

	while(getline(infile, line)) {
		/** Split a line. */
		stringstream chk(line);
		vector<string> tokens;
		string inter;
		while(getline(chk, inter, ' '))
			tokens.push_back(inter);

		/** Create an edge for a line. */
		if(tokens.size() == 1) {
			m_vecRules.push_back( pair<char, string>(tokens[0][0], string("")) );
		} else if(tokens.size() == 2) {
			m_vecRules.push_back( pair<char, string>(tokens[0][0], tokens[1]) );
		} else {
			cout<<"Format error"<<endl;
			exit(0);
		}
	}
}

void
Prod::print(ostream& os) const
{
	for(int i=0; i<m_vecRules.size(); i++) {
		cout << m_vecRules[i].first;
		cout << " => ";
		cout << m_vecRules[i].second;
		cout << endl;
	}
}

void
Prod::computeFirst(void)
{
	for(int i=0; i<m_vecRules.size(); i++) {
		cout << "FIRST(";
		cout << m_vecRules[i].second;
		cout << ") = ";
		cout << getFirst(m_vecRules[i].second);
	}
}

void
Prod::computeFollow(void)
{
	Set nonterminal;
	for(int i=0; i<m_vecRules.size(); i++)
		nonterminal.insert(m_vecRules[i].first);
	for(Set::iterator it=nonterminal.begin(); it!=nonterminal.end(); ++it) {
		cout << "FOLLOW(";
		cout << *it;
		cout << ") = ";
		cout << getFollow(*it);
	}
}

Set
Prod::getFirst(string a)
{
	Set get_first;
	Set ep;
	Set tmp, tmp1;
	ep.insert(' ');
	int flag = 0;
	if(a.size() == 1)
	{
		if(!isNonterminal(a[0]))
			get_first.insert(a[0]);
		else
		{
			for(int i=0; i<m_vecRules.size(); i++)
			{
				if(m_vecRules[i].first == a[0]) {
					get_first |= getFirst(m_vecRules[i].second);
					if(m_vecRules[i].second.size() == 0)
						get_first |= ep;
				}
			}
		}
		return get_first;
	}
	for(int i=0; i<a.size(); i++) {
		if(flag == 0)
		{
			tmp = getFirst(a.substr(i,1));
			if(i == a.size()-1)
				get_first |= tmp;
			else {
				for(Set::iterator it = tmp.begin(); it != tmp.end(); ++it) {
					if(*it != ' ')
						tmp1.insert(*it);
				}
				get_first |= tmp1;
			}
			if(tmp != (tmp | ep))
				flag = 1;
		}
		else
			break;
	}
	return get_first;
}

Set
Prod::getFollow(char A)
{
	Set get_follow;
	Set tmp, tmp1;
	Set ep;
	string::size_type n;
	string::size_type n1;
	ep.insert(' ');
	if(A == m_vecRules[0].first) 
		get_follow.insert('$');
	for(int i=0; i<m_vecRules.size(); i++) {
		n=m_vecRules[i].second.find(A);
		if(n != string::npos) {
			if(m_vecRules[i].second.substr(n).size() == 1 && A != m_vecRules[i].first)
				get_follow |= getFollow(m_vecRules[i].first);
			else {
				tmp = getFirst(m_vecRules[i].second.substr(n+1));
				if(tmp == (tmp | ep)) {
					if(A != m_vecRules[i].first)
						get_follow |= getFollow(m_vecRules[i].first);
					for(Set::iterator it = tmp.begin(); it != tmp.end(); ++it) {
						if(*it != ' ')
							tmp1.insert(*it);
					}
					get_follow |= tmp1;
				}
				else
					get_follow |= tmp;
			}
		}
	}
	return get_follow;
}
