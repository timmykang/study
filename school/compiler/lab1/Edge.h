#ifndef	__EDGE_H__
#define	__EDGE_H__

#include <iostream>
using namespace std;

/**
 * A class to represent an edge in a graph.
 */
class Edge {
public:
	/**
	 * A constructor of an edge.
	 *
         * @param from  The node number where the edge starts.
         * @param to    The node number where the edge ends.
         * @param input The input character that triggers the transition.
         */
	Edge(int from, int to, char input): m_nFrom(from), m_nTo(to), m_cInput(input) {};

	/**
	 * A getter function of "from" node.
	 *
	 * @return	"from" node of the edge.
	 */
	int getFrom(void) const { return m_nFrom; }
	/**
	 * A getter function of "to" node.
	 *
	 * @return	"to" node of the edge.
	 */
	int getTo(void) const { return m_nTo; }
	/**
	 * A getter function of the input.
	 *
	 * @return	The input of the edge.
	 */
	char getInput(void) const { return m_cInput; }

	/**
	 * Print the edge.
	 *
	 * @param os 	The output stream the edge is printed to.
	 */
	void print(ostream& os) const;
	/**
	 * The overloaded operator to print the edge.
	 */
	friend ostream& operator<<(ostream& os, const Edge& edge) { edge.print(os); return os; }
	/**
	 * The overloaded operator to compare edges.
	 */
	bool operator<(Edge e) const {
		if(m_nFrom < e.getFrom()) return true;
		if(m_nFrom == e.getFrom() && m_nTo < e.getTo()) return true;
		return false;
	}

protected:
	int m_nFrom;	/**< "from" node. */
	int m_nTo;	/**< "to" node. */
	char m_cInput;	/**< Input. */
};

#endif
