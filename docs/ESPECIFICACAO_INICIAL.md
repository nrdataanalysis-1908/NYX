# Especificação inicial da linguagem NYX

Versão da especificação: 0.1 (MVP)
Estado: proposta implementada em protótipo; sujeita a evolução compatível.

## 1. Objetivo desta versão

Estabelecer uma linguagem mínima, própria e executável, com frontend, AST e interpretador independentes. A implementação inicial do runtime utiliza Python como tecnologia hospedeira; a semântica dos programas é definida pela NYX.

## 2. Arquivo e codificação

- Extensão: `.nyx`.
- Codificação: UTF-8.
- Comentários de linha: começam com `#`.
- Instruções terminam com ponto e vírgula.

## 3. Tipos fundamentais

| Tipo | Literais | Observação |
|---|---|---|
| Integer | `0`, `42` | Inteiro de precisão arbitrária nesta implementação |
| Float | `3.14` | Ponto flutuante binário de dupla precisão |
| String | `"NYX"` | Aspas duplas; escapes `\\n`, `\\t`, `\"` e `\\\\` |
| Boolean | `true`, `false` | Operações lógicas estritas |
| Null | `null` | Ausência explícita de valor |

## 4. Declaração e saída

```nyx
let samples = 120;
let ratio = 0.875;
let title = "NYX scientific runtime";
let validated = true;

print(title);
print(samples * ratio);
print(validated);
```

Uma variável é declarada uma única vez por escopo global nesta versão. Reatribuição, blocos e escopos locais ainda não fazem parte do MVP.

## 5. Operadores e precedência

Da menor para a maior precedência:

1. `or`
2. `and`
3. `==`, `!=`
4. `<`, `<=`, `>`, `>=`
5. `+`, `-`
6. `*`, `/`, `%`
7. `not`, `+` unário, `-` unário
8. Literais, identificadores e parênteses

Operadores aritméticos aceitam apenas valores numéricos. Operadores lógicos aceitam apenas booleanos. Comparações relacionais são numéricas. Igualdade compara tipo e valor.

## 6. Gramática EBNF

```ebnf
program       = { statement } ;
statement     = declaration | print_statement ;
declaration   = "let" , identifier , "=" , expression , ";" ;
print_statement = "print" , "(" , expression , ")" , ";" ;
expression    = logical_or ;
logical_or    = logical_and , { "or" , logical_and } ;
logical_and   = equality , { "and" , equality } ;
equality      = comparison , { ( "==" | "!=" ) , comparison } ;
comparison    = term , { ( "<" | "<=" | ">" | ">=" ) , term } ;
term          = factor , { ( "+" | "-" ) , factor } ;
factor        = unary , { ( "*" | "/" | "%" ) , unary } ;
unary         = ( "not" | "+" | "-" ) , unary | primary ;
primary       = number | string | "true" | "false" | "null"
              | identifier | "(" , expression , ")" ;
number        = integer | float ;
identifier    = letter | "_" , { letter | digit | "_" } ;
```

## 7. Diagnósticos

Erros léxicos, sintáticos e de execução informam linha e coluna no formato `[NYX:Lx:Cy]`. O interpretador interrompe a execução no primeiro erro.

## 8. Limites conhecidos

Esta versão ainda não implementa funções definidas pelo usuário, condicionais, laços, coleções, módulos, inferência estática, sistema de tipos em compilação, IR, otimização, operações tabulares, álgebra científica ou integração com IA. Esses recursos não devem ser anunciados como disponíveis.

## 9. Independência

O lexer, parser, nós de AST, regras de precedência e interpretador são componentes próprios do projeto. Python é apenas a linguagem hospedeira do protótipo 0.1; não é a gramática nem o mecanismo de avaliação delegado da NYX.
