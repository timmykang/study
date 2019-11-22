#ifndef	__PROD_H__
#define	__PROD_H__

#include <iostream>
#include <vector>
#include <utility>
#include <string>
#include "Set.h"
using namespace std;

/**
 * A class to manage production rules.
 */
class Prod {
public:
	/**
	 * An empty constructor.
	 */
	Prod() {};
	/**
	 * A constructor reading an input file.
	 *
	 * @param in	The input file name.
	 */
	Prod(const char* in) { readFile(in); }

	/**
	 * Read an input file.
	 *
	 * @param in	The input file name. Each line of the file represents a rule.
	 *		The format of a rule is "L R" which means a derivation L=>R.
	 *		All tokens are single characters.
	 *		Captial letters are non-terminals and others are terminals.
	 *		Epsilon is denoted by an empty string.
	 */
	void readFile(const char* in);

        /**
         * Print all production rules.
         *
         * @param os    The output stream the rules are printed to.
         */
	void print(ostream& os) const;
	/**
	 * The overloaded operator to print the rules.
	 */
	friend ostream& operator<<(ostream& os, const Prod& prod) { prod.print(os); return os; }


	/**
	 * Compute FIRST of production rules.
	 * This function is only for testing getFirst.
	 */
	void computeFirst(void);
	/**
	 * Compute FOLLOW of production rules.
	 * This function is only for testing getFollow.
	 */
	void computeFollow(void);

	/**
	 * Get FIRST of the given string.
	 *
	 * @param a	The right-hand string of the production rule.
	 * @return	FIRST(a).
	 */
	Set getFirst(string a);
	/**
	 * Get FOLLOW of the given non-terminal.
	 *
	 * @param A	The non-terminal character.
	 * @return	FOLLOW(A).
	 */
	Set getFollow(char A);

protected:
	/**
	 * Production rules.
	 */
	vector< pair<char, string> > m_vecRules;

	/**
	 * Check whether the character is non-terminal or not.
	 *
	 * @param n	The character.
	 * @return	True if the character is captial meaning it is a non-terminal.
	 *		False otherwise.
	 */
	inline bool isNonterminal(char n) { return ('A'<=n && n<='Z'); }
};

#endif
