grammar result;

gr : output EOF ;

output : command (output)? ;

command : name result ; 

name : TYPE NAME SCOPE  ;

result : unsat  
	   | sat 	
	   ;

unsat : UNSATISFIABLE ;

sat : INSTANCE METAINFO sts ;

sts : st  	 
	| st sts 
	;

st : STATENAME descriptions  ;

descriptions : FIELDESCRIPTION ;


WHITESPACE : ('\t' | ' ' | '\r' | '\n')+ -> skip;

TYPE : 'Check ' ; 
NAME : 'prop_'[0-9]+' ' ;
SCOPE : 'for '[0-9]+' but '[0-9]+'..'[0-9]+' Time,'' exactly '[0-9]+' Value, '[0-9]+' Message';

UNSATISFIABLE : '---OUTCOME---\n''Unsatisfiable''.\n' ;

INSTANCE : '---INSTANCE---\n' ;
METAINFO : 'loop='[0-9]+'\nend='[0-9]+'\nintegers={'(('-'[0-9](',')? | [0-9](',')?)|(' '))+'}\n';
STATENAME : '------State '[0-9]+'-------\n' ;

FIELDESCRIPTION :  (('univ' | 'Int' | 'seq/Int' | 'String' | 'none' | 'this/')(.)*?'={'(.)*?'}\n')('skolem $'(.)+?'='(.)+?'}\n');
