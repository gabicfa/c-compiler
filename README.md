# LogComp

### Diagrama Sintático
![](DiagramaSintatico/DS_v2.2(1).png)
![](DiagramaSintatico/DS_v2.2(2).png)
![](DiagramaSintatico/DS_v2.2(3).png)
### EBNF:
```
comandos = "{", comando, ";", { comando, ";" }, "}" ;
comando = atribuição | comandos | print | if | while;
print = printf, "(", expressão, ")" ;
atribuição = identificador, "=", (expressão | "scanf", "(", ")" ) ;
expressão = termo, { ("+" | "-"), termo } ;
termo = fator, { ("*" | "/"), fator } ;
fator = ("+" | "-"), fator | número | "(", expressão, ")" | identificador ;
printf = "printf";
while = "while","(", booleanExp , ")", comando;
if = "if", "(", booleanExp, ")", comando, ( | "else", comando);
booleanExp = booleanTerm, { "||" , booleanTerm};
booleanTerm = booleanFactor, { "&&" , booleanFactor};
booleanFactor = RelExp | "!", booleanFactor;
RelExp = expressão, (">"| "==" | "<"), expressão ;
```
