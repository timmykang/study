#ifndef	__GRAPH_H__
#define	__GRAPH_H__

#include <iostream>
#include <vector>
#include "Edge.h"
#include "Set.h"
using namespace std;

/**
 * A class to manage a directed graph.
 * A node is denoted as a number, and an edge is denoted by (from, to, input).
 */
class Graph {
public:
	/** 
	 * An empty consturctor.
	 */
	Graph() {};
	/**
	 * A constructor reading an input file.
	 *
	 * @param in 	The input file name.
	 */
	Graph(const char* in) { readFile(in); }

	/**
	 * Read an input file.
	 *
	 * @param in 	The input file name. Each line of the file represents an edge.
	 *		The format of a line is "From To Input".
	 *		"From" and "To" are integers and "Input" is a character.
	 *		If "Input" is missing, it means an empty string (epsilon).
	 */
	void readFile(const char* in);
	/**
	 * Add an edge to the graph.
	 *
	 * @param from	The node number where the edge starts.
	 * @param to	The node number where the edge ends.
	 * @param input	The input character that triggers the transition.
	 */
	void insertEdge(int from, int to, char input);

	/**
	 * Print all edges of the graph.
	 * Edges are ordered by the "from" node and "to" node.
	 *
	 * @param os	The output stream the graph is printed to.
	 */
	void print(ostream& os) const;
	/**
	 * The overloaded operator to print the graph.
	 */
	friend ostream& operator<<(ostream& os, const Graph& graph) { graph.print(os); return os; }

	/**
	 * Get the e-closure of the node s.
	 *
	 * @param s	The node number from where the e-closure is obtained.
	 * @return	The e-closure of node s.
	 */
	Set getEClosure(int s);
	/**
	 * Get the e-closure of a set of nodes.
	 *
	 * @param T	The set of nodes from where the e-closure is obtained.
	 * @return	The e-closure of the set of nodes.
	 */
	Set getEClosure(Set T);
	/**
	 * Get the set of nodes triggered by input a from the nodes in T.
	 *
	 * @param T	The set of starting nodes.
	 * @param a	The triggering input.
	 * @return	The set of nodes triggered by input a from the nodes in T.
	 */
	Set move(Set T, char a);

protected:
	vector<Edge> m_vecEdges;	/**< The edges of the graph. */
};

#endif
