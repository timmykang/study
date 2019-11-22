#include "Edge.h"

void
Edge::print(ostream& os) const 
{ 
	os<<m_nFrom<<" "<<m_nTo; 
	if(m_cInput)
		os<<" "<<m_cInput; 
	os<<endl;
}
