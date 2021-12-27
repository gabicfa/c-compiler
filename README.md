# C compiler

### Diagrama Sintático
![](DiagramaSintatico/DS_v2.4(1).png)
![](DiagramaSintatico/DS_v2.4(2).png)
![](DiagramaSintatico/DS_v2.4(3).png)
![](DiagramaSintatico/DS_v2.4(4).png)
![](DiagramaSintatico/DS_v2.4(5).png)
### EBNF:

```
programa = { tipo, identificador, "(" ( | { tipo, identificador, ',' }, tipo, identificador ), ")", comandos };

tipo = "void" | "int" | "char";

comandos = "{", { comando }, "}" ;

comando = atribuição | comandos | print | ifExp | whileExp | declaração | returnExp;

print = "printf", "(", expressão, ")", ";" ;

declaração = tipo, identificador, ( "(" ( | { tipo, identificador, ',' }, tipo, identificador), ")"  |  { ",", identificador}, ";" );

atribuição = identificador, "=", ( expressão | "scanf", "(", ")" | funcCall ) ;

returnExp = "return", "(", expressão,  ")", ";"

expressão = termo, { ( "+" | "-" ), termo } ;

termo = fator, { ( "*" | "/" ), fator } ;

fator = ( "+" | "-" ), fator | número | "(", expressão, ")" | identificador | funcCall;

funcCall = identificador, "(" , ( | expressão { "," expressão } ), ")";

whileExp = "while", "(", booleanExp, ")", comando;

ifExp = "if", "(", booleanExp, ")", comando, ( | "else", comando );

booleanExp = booleanTerm, { "||" , booleanTerm };

booleanTerm = booleanFactor, { "&&" , booleanFactor };

booleanFactor = RelExp | "!", booleanFactor;

RelExp = expressão, (">"| "==" | "<"), expressão ;
```
