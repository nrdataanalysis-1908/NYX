# Especificação da linguagem NYX

**Documento:** NYX-LANG-SPEC  
**Versão da especificação:** 0.1.0-draft  
**Estado:** proposta inicial em revisão  
**Projeto:** NR TECH  
**Idioma normativo:** português

> Esta especificação define a primeira proposta formal da linguagem. Ela ainda não representa uma versão implementada nem uma gramática congelada. Alterações devem ser registradas por versão e acompanhadas de testes de conformidade.

## 1. Objetivo

NYX é uma linguagem de programação independente voltada à ciência de dados, computação científica e inteligência artificial. Sua sintaxe deve favorecer legibilidade, precisão semântica, reprodutibilidade e composição de operações.

A gramática não será uma camada sintática de Python. Lexer, parser, árvore sintática, sistema de tipos, representação intermediária e runtime serão componentes próprios.

## 2. Decisões sintáticas da versão 0.1

| Elemento | Proposta |
|---|---|
| Codificação | UTF-8 |
| Sensibilidade a maiúsculas | Sim |
| Identificadores | ASCII na primeira versão; Unicode poderá ser avaliado posteriormente |
| Blocos | Delimitados por chaves `{` e `}` |
| Fim de instrução | Quebra de linha ou ponto e vírgula |
| Comentário de linha | `#` |
| Comentário de bloco | `/* ... */` |
| Atribuição | `=` |
| Comparação de igualdade | `==` |
| Anotação de tipo | `:` |
| Composição de operações | Operador `|>` |
| Declaração imutável | `let` |
| Declaração mutável | `var` |
| Função | `fn` |
| Retorno | `return` |

A quebra de linha encerra uma instrução somente quando o parser não estiver dentro de delimitadores ou de uma construção que exija continuação. A regra exata de continuação será validada na implementação do lexer/parser.

## 3. Palavras reservadas

### 3.1 Núcleo da linguagem

`module`, `import`, `as`, `let`, `var`, `const`, `fn`, `return`, `if`, `else`, `for`, `in`, `while`, `break`, `continue`, `true`, `false`, `null`, `and`, `or`, `not`.

### 3.2 Diretriz para domínios científicos

Nomes como `science`, `statistics`, `math`, `data`, `ai`, `Array`, `Matrix`, `Tensor`, `Series` e `DataFrame` não serão palavras reservadas por padrão. Serão nomes de módulos, tipos ou símbolos da biblioteca padrão. Isso evita ocupar antecipadamente o espaço de nomes do usuário.

## 4. Regras léxicas

### 4.1 Identificadores

Na versão inicial, identificadores seguem:

```ebnf
identifier = (letter | "_"), { letter | digit | "_" } ;
letter     = "A"…"Z" | "a"…"z" ;
digit      = "0"…"9" ;
```

Identificadores são sensíveis a maiúsculas e minúsculas. Assim, `valor`, `Valor` e `VALOR` são símbolos distintos.

### 4.2 Literais

A proposta inicial contempla:

- Inteiros decimais: `0`, `42`, `-17`.
- Ponto flutuante: `3.14`, `0.5`, `1.0e-6`.
- Booleanos: `true` e `false`.
- Nulo: `null`.
- Strings: aspas duplas, com sequências de escape.
- Coleções literais: listas entre colchetes e mapas entre chaves.

A distinção entre inteiro e ponto flutuante será preservada na análise semântica. O sinal unário pertence à expressão, não ao token numérico.

### 4.3 Comentários

```nyx
# Comentário de linha

/*
   Comentário
   de bloco
*/
```

Comentários não produzem instruções executáveis.

## 5. Tipos fundamentais

Os nomes abaixo constituem a proposta inicial do sistema de tipos, não uma declaração de que os tipos já estejam implementados.

| Família | Tipos propostos | Finalidade |
|---|---|---|
| Numéricos | `Int`, `Int64`, `Float32`, `Float64` | Aritmética e precisão controlada |
| Lógico | `Bool` | Valores verdadeiro/falso |
| Texto | `String` | Texto Unicode |
| Binário | `Bytes` | Dados binários |
| Ausência | `Null` | Ausência explícita de valor |
| Coleções | `Array<T>`, `List<T>`, `Map<K,V>`, `Set<T>`, `Tuple<...>` | Estruturas genéricas |
| Científicos | `Vector<T>`, `Matrix<T>`, `Tensor<T>` | Computação numérica |
| Dados | `Series<T>`, `DataFrame`, `Dataset` | Dados tabulares e conjuntos |

Tipos compostos usarão parâmetros explícitos entre sinais de menor e maior. A inferência poderá ser oferecida em contextos inequívocos, sem ocultar conversões potencialmente destrutivas.

## 6. Gramática sintática preliminar

A gramática abaixo usa notação EBNF. É uma base normativa em elaboração; regras de precedência, recuperação de erro e detalhes de tokens serão refinados antes da implementação do parser.

```ebnf
program         = { module_decl | statement } ;

module_decl     = "module", qualified_name, terminator ;
import_decl     = "import", qualified_name, [ "as", identifier ], terminator ;
qualified_name  = identifier, { ".", identifier } ;

statement       = import_decl
                | variable_decl
                | function_decl
                | assignment
                | return_stmt
                | conditional
                | while_stmt
                | for_stmt
                | expression_stmt ;

variable_decl   = ( "let" | "var" | "const" ),
                  identifier, [ ":", type_expr ],
                  "=", expression, terminator ;

function_decl   = "fn", identifier, "(", [ parameters ], ")",
                  [ "->", type_expr ], block ;

parameters      = parameter, { ",", parameter } ;
parameter       = identifier, [ ":", type_expr ] ;

return_stmt     = "return", [ expression ], terminator ;

conditional     = "if", expression, block,
                  [ "else", ( block | conditional ) ] ;

while_stmt      = "while", expression, block ;

for_stmt        = "for", identifier, "in", expression, block ;

assignment      = assignable, assignment_operator, expression, terminator ;
assignable      = identifier, { member_access | index_access } ;

assignment_operator = "=" | "+=" | "-=" | "*=" | "/=" ;

block           = "{", { statement }, "}" ;

type_expr       = qualified_name,
                  [ "<", type_expr, { ",", type_expr }, ">" ]
                | "[", type_expr, "]" ;

expression_stmt = expression, terminator ;

expression      = logical_or ;
logical_or      = logical_and, { "or", logical_and } ;
logical_and     = comparison, { "and", comparison } ;
comparison      = additive, [ comparison_operator, additive ] ;
additive        = multiplicative, { ( "+" | "-" ), multiplicative } ;
multiplicative  = unary, { ( "*" | "/" | "%" ), unary } ;
unary           = [ "-" | "+" | "not" ], unary | pipeline ;
pipeline        = postfix, { "|>", postfix } ;
postfix         = primary, { call | member_access | index_access } ;

call            = "(", [ arguments ], ")" ;
arguments       = expression, { ",", expression } ;
member_access   = ".", identifier ;
index_access    = "[", expression, "]" ;

primary         = literal
                | identifier
                | "(", expression, ")"
                | array_literal
                | map_literal ;

array_literal   = "[", [ arguments ], "]" ;
map_literal     = "{", [ map_entry, { ",", map_entry } ], "}" ;
map_entry       = expression, ":", expression ;

literal         = integer
                | float
                | string
                | "true"
                | "false"
                | "null" ;

terminator      = newline | ";" ;
```

## 7. Operadores e precedência

Da maior para a menor precedência, a proposta é:

1. Acesso a membro, chamada e indexação: `.`, `()`, `[]`.
2. Operadores unários: `-`, `+`, `not`.
3. Multiplicativos: `*`, `/`, `%`.
4. Aditivos: `+`, `-`.
5. Comparação: `==`, `!=`, `<`, `<=`, `>`, `>=`.
6. Conjunção: `and`.
7. Disjunção: `or`.
8. Composição de pipeline: `|>` — a associatividade e a interação com chamadas serão formalizadas na próxima revisão.

A tabela é uma decisão preliminar. A gramática EBNF será ajustada para representar essa precedência sem ambiguidades antes do parser ser considerado estável.

## 8. Declarações e semântica inicial

- `let`: vinculação imutável; o símbolo não pode receber nova atribuição após sua inicialização.
- `var`: vinculação mutável, sujeita às regras de tipo.
- `const`: constante de compilação quando o valor puder ser determinado estaticamente; os limites dessa avaliação serão especificados posteriormente.
- `fn`: declaração de função nomeada.
- `return`: encerra a execução da função corrente e entrega um valor, quando presente.
- `if`, `else`, `while` e `for`: estruturas de controle explícitas.
- Escopos são delimitados por blocos. Resolução de nomes e sombreamento serão especificados na camada semântica.

## 9. Exemplo de programa conceitual

O exemplo ilustra a direção sintática desejada. Não é executável na versão atual do projeto.

```nyx
module analise_vendas

import data.io
import science.statistics

let vendas: DataFrame = data.io.read_csv("vendas.csv")

let vendas_validas = vendas
    |> data.filter(amount > 0)
    |> data.group_by("region")
    |> data.aggregate(
        total = sum(amount),
        media = mean(amount)
    )

fn calcular_media(valores: Array<Float64>) -> Float64 {
    return statistics.mean(valores)
}

print(vendas_validas)
```

## 10. Regras de erro e diagnóstico

O compilador/interpretador deverá distinguir, no mínimo:

- Erro léxico: caractere ou sequência não reconhecida.
- Erro sintático: construção fora da gramática.
- Erro semântico: símbolo não declarado, escopo inválido ou operação incompatível.
- Erro de tipo: incompatibilidade não permitida pelas regras de conversão.
- Erro de execução: falha ocorrida durante a avaliação de um programa válido.

Diagnósticos deverão identificar arquivo, linha e coluna, apresentar a categoria do erro e, quando possível, indicar o trecho relacionado. A implementação deverá testar mensagens e posições, não apenas o fato de uma exceção ocorrer.

## 11. Pontos que exigem decisão antes da gramática estável

1. Semântica exata de quebras de linha e continuação de expressões.
2. Associatividade e sintaxe definitiva do operador `|>`.
3. Inferência de tipos, conversões implícitas e promoção numérica.
4. Mutabilidade de coleções e semântica de referências.
5. Funções anônimas, closures e funções de ordem superior.
6. Tratamento de erros recuperáveis: tipos `Result<T, E>` e/ou exceções.
7. Regras de módulos, visibilidade e resolução de imports.
8. Semântica de comparação entre estruturas científicas e operações vetorizadas.

Esses pontos não serão decididos implicitamente durante a implementação. Cada decisão deverá ser documentada e acompanhada de exemplos e testes.

## 12. Critérios de aceitação da especificação

A versão 0.1 somente poderá deixar o estado de rascunho quando:

- a gramática não apresentar ambiguidades conhecidas;
- cada construção tiver semântica descrita;
- houver exemplos válidos e inválidos;
- precedência e associatividade estiverem definidas;
- os tipos e as conversões iniciais estiverem delimitados;
- a especificação puder orientar lexer, parser e testes sem depender de interpretação informal.

---

**NYX — Numerical Yield eXchange**  
**NR TECH**  
*Think Scientifically. Compute Intelligently.*
