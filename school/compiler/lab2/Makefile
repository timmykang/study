CXX=g++
CXXFLAGS=
LDFLAGS=
LDLIBS=

SRCS=main.cpp Graph.cpp Edge.cpp Set.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

TARGET=lab2

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(LDFLAGS) -o $(TARGET) $(OBJS) $(LDLIBS)

depend: .depend

.depend: $(SRCS)
	rm -f ./.depend
	$(CXX) $(CPPFLAGS) -MM $^ >> ./.depend;

clean:
	rm -f $(OBJS) $(TARGET) *~ .depend core

new:
	make clean; make all

include .depend
