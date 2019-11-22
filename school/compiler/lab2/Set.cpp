#include "Set.h"

void
Set::print(ostream& os) const
{
	Set::iterator it;
	os<<"{ ";
	for(it=begin(); it!=end(); ++it)
		os<<(*it)<<" ";
	os<<"}"<<endl;;
}

bool
Set::isEqual(Set& r)
{
	if(size() != r.size())
		return false;
	for(Set::iterator it=r.begin(); it!=r.end(); ++it)
		if(find(*it)==end())
			return false;
	return true;
}
