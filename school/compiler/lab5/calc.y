%{

#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;

void yyerror(const char* s);
%}

%union {
	int ival;
    float fval;
}

%token<ival> T_INT
%token<fval> T_FLOAT
%token T_PLUS T_MINUS T_MULTIPLY T_DIVIDE T_LEFT T_RIGHT
%token T_NEWLINE T_QUIT
%left T_PLUS T_MINUS
%left T_MULTIPLY T_DIVIDE

%type<fval> expr

%start start

%%

start: 	
	| start line
;

line: 	T_NEWLINE
    	| expr T_NEWLINE 	{ printf("\tResult: %.5f\n", $1); }
    	| T_QUIT T_NEWLINE 	{ printf("\tBye!\n"); exit(0); }
;

expr: 	T_INT			{ $$ = $1; }
    | T_FLOAT      { $$ = $1; }
	| expr T_PLUS expr	{ $$ = $1 + $3; }
	| expr T_MINUS expr	{ $$ = $1 - $3; }
	| expr T_MULTIPLY expr	{ $$ = $1 * $3; }
	| expr T_DIVIDE expr	{ $$ = $1 / $3; }
	| T_LEFT expr T_RIGHT	{ $$ = $2; }
;

%%

int main() {
	yyin = stdin;

	do {
		yyparse();
	} while(!feof(yyin));

	return 0;
}

void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(1);
}
