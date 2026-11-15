# Especificação inicial da linguagem NYX

Versão da especificação: 0.3 (MVP em evolução)
Estado: implementação alfa com declarações, expressões, blocos e controle condicional/iterativo.

## 1. Objetivo

Estabelecer uma linguagem própria e executável, com frontend, AST, semântica e interpretador independentes. Python é a tecnologia hospedeira do runtime atual; não define a gramática nem a semântica da NYX.

## 2. Arquivos e instruções

- Extensão: `.nyx`.
- Codificação: UTF-8 com ou sem BOM.
- Comentários de linha começam com `#`.
- Instruções podem ser separadas por quebra de linha ou ponto e vírgula.
- Ponto e vírgula é opcional quando a quebra de linha ou o fechamento do bloco delimita a instrução.
- Blocos são delimitados por `{` e `}`.

## 3. Tipos fundamentais

| Tipo | Literais |
|---|---|
| Integer | `0`, `42` |
| Float | `3.14` |
| String | `"NYX"` |
| Boolean | `true`, `false` |
| Null | `null` |

Inteiros usam precisão arbitrária na implementação hospedeira. Float utiliza ponto flutuante binário de dupla precisão.

## 4. Declarações e saída

```nyx
let samples = 120
let ratio = 0.875
let title = "NYX"
print(title)
print(samples * ratio)
```

Uma variável é declarada uma única vez por escopo. Atribuição/redefinição ainda não está implementada.

## 5. Controle de fluxo

Condicionais exigem condições booleanas e blocos delimitados por chaves:

```nyx
if (10 > 3) {
    print("condição verdadeira")
} else {
    print("condição falsa")
}
```

O ramo `else` é opcional. Laços `while` reavaliam uma condição booleana antes de cada iteração:

```nyx
while (false) {
    print("este bloco não será executado")
}
```

Os blocos criam escopos locais. Variáveis declaradas dentro deles não ficam visíveis fora do bloco. Como atribuição ainda não existe, laços cujo estado depende de mutação de variáveis ainda não são práticos; a implementação de atribuição é uma evolução necessária para laços gerais.

## 6. Operadores e precedência

Da menor para a maior precedência:

1. `or`
2. `and`
3. `==`, `!=`
4. `<`, `<=`, `>`, `>=`
5. `+`, `-`
6. `*`, `/`, `%`
7. `not`, `+` unário, `-` unário
8. Literais, identificadores e parênteses

Operadores aritméticos aceitam valores numéricos. Operadores lógicos e condições exigem booleanos. Comparações relacionais são numéricas. Igualdade compara tipo e valor.

## 7. Gramática EBNF

```ebnf
program          = { statement } ;
statement        = declaration | print_statement | if_statement
                 | while_statement | block ;
declaration      = "let" , identifier , "=" , expression , terminator ;
print_statement  = "print" , "(" , expression , ")" , terminator ;
if_statement     = "if" , "(" , expression , ")" , block
                 , [ "else" , block ] ;
while_statement  = "while" , "(" , expression , ")" , block ;
block            = "{" , { statement } , "}" ;
terminator       = ";" | line_break | "}" | EOF ;
expression       = logical_or ;
logical_or       = logical_and , { "or" , logical_and } ;
logical_and      = equality , { "and" , equality } ;
equality         = comparison , { ( "==" | "!=" ) , comparison } ;
comparison       = term , { ( "<" | "<=" | ">" | ">=" ) , term } ;
term             = factor , { ( "+" | "-" ) , factor } ;
factor           = unary , { ( "*" | "/" | "%" ) , unary } ;
unary            = ( "not" | "+" | "-" ) , unary | primary ;
primary          = number | string | "true" | "false" | "null"
                 | identifier | "(" , expression , ")" ;
number           = integer | float ;
identifier       = ( letter | "_" ) , { letter | digit | "_" } ;
```

## 8. Escopos e semântica

- O programa inicia em um escopo global.
- Cada bloco cria um escopo local.
- A resolução de nomes procura primeiro o escopo mais interno e segue em direção ao global.
- Declarações duplicadas no mesmo escopo geram erro.
- Condições não booleanas geram erro de execução.
- O interpretador interrompe a execução no primeiro erro.

## 9. Diagnósticos e limites

Erros léxicos, sintáticos e de execução informam linha e coluna no formato `[NYX:Lx:Cy]`.

Ainda não existem atribuição, funções, coleções, módulos, inferência estática, sistema de tipos em compilação, IR, otimização, operações tabulares, álgebra científica ou integração nativa com IA. A ausência de atribuição limita laços `while` a condições que possam terminar sem alteração de estado; atribuição é o próximo recurso necessário para tornar a iteração geral útil.

## 10. Independência

Lexer, parser, AST, regras de precedência e interpretador são componentes próprios. Python é apenas a linguagem hospedeira do protótipo alfa.
