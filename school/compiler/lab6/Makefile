TARGET=lab6

all: $(TARGET)

calc.tab.c calc.tab.h:	calc.y
	bison -d calc.y

lex.yy.c: calc.l calc.tab.h
	flex calc.l

$(TARGET): lex.yy.c calc.tab.c calc.tab.h
	gcc -o $(TARGET) calc.tab.c lex.yy.c

clean:
	rm -f $(TARGET) calc.tab.c lex.yy.c calc.tab.h *~ core

new:
	make clean; make all
