%{
#include <cstdlib>
#include <string>
using namespace std;

#ifdef __cplusplus
extern "C" {
#endif
void yyerror(char *msg);
int yyparse(void);
#ifdef __cplusplus
}
#endif

extern int yylex(void);
%}

%union {
  int num;
  double fnum;
  char *name;
}

%token <num> NUM
%token <fnum> FNUM
%token <name> STR

%%

input:
    /* empty */
  | input line
  ;

line:
    STR { }
  | NUM { }
  | FNUM { }
  ;

%%

// yyerror is defined in config_utils.cpp