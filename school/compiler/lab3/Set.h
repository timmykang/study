#ifndef	__SET_H__
#define	__SET_H__

#include <iostream>
#include <set>
using namespace std;

/**
 * A class to handle a set which is an extension of the standard set class.
 */
class Set: public set<char> {
public:
	/** An empty constructor. */
	Set() {};

	/** An overloaded operator to print the set. */
	friend ostream& operator<<(ostream& os, const Set& s) { s.print(os); return os; }
	/** An overloaded operator to check equality. */
	friend bool operator==(Set& l, Set& r) { return l.isEqual(r); }
	/** An overloaded operator to implement union. */
	friend Set operator|(Set lhs, const Set& rhs) { for(Set::iterator it=rhs.begin(); it!=rhs.end(); ++it) lhs.insert(*it); return lhs; }
	/** An overloaded operator to implement union. */
	Set& operator|=(const Set& rhs) { (*this) = (*this) | rhs; return (*this); }

protected:
        /**
         * Print all elements of the set.
         *
         * @param os    The output stream the graph is printed to.
         */
	void print(ostream& os) const;
	/**
	 * Check whether the given set is equal to this set.
	 *
	 * @param r	The set to be compared.
	 * @return	True if the given set is same with this set.
	 *		False otherwise.
	 */
	bool isEqual(Set& r);
};
#endif
