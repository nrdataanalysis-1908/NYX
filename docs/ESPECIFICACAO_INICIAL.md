# Especificação da linguagem NYX

Versão da especificação: 0.4
Estado: alfa — frontend próprio e interpretador tree-walk.

## 1. Identidade e objetivo

NYX significa Numerical Yield eXchange. É uma linguagem de programação independente, concebida para computação científica, engenharia de dados, automação e interoperabilidade.

A implementação atual possui lexer, parser recursivo descendente, árvore sintática abstrata (AST), regras de avaliação e interpretador próprios. Python é, neste estágio, a tecnologia hospedeira usada para executar o protótipo; não define a sintaxe nem a semântica da linguagem.

Esta especificação descreve somente os recursos efetivamente implementados. Recursos planejados são identificados como não implementados.

## 2. Arquivos, codificação e comentários

- Extensão de arquivo: `.nyx`.
- Codificação aceita: UTF-8 com ou sem BOM no início do arquivo.
- Comentários de linha começam com `#` e terminam na quebra de linha.
- Espaços, tabulações e retornos de carro são ignorados.
- Quebras de linha são registradas nas posições dos tokens, mas não geram tokens próprios.
- Instruções simples podem terminar com ponto e vírgula ou com uma quebra de linha reconhecida pelo parser.
- O ponto e vírgula é opcional antes do fim do arquivo ou do fechamento de um bloco.
- Blocos usam `{` e `}`.

Uma quebra de linha delimita uma instrução simples quando o próximo token começa em uma linha posterior à linha do token anterior consumido pela instrução. Se a expressão ainda não foi concluída — por exemplo, depois de um operador binário — o parser continua a expressão na linha seguinte.

## 3. Tipos e valores

| Tipo | Exemplos | Observações |
|---|---|---|
| Integer | `0`, `42` | Inteiro de precisão arbitrária na implementação hospedeira |
| Float | `3.14` | Ponto flutuante binário de dupla precisão |
| String | `"NYX"` | Aspas duplas; sem strings multilinha |
| Boolean | `true`, `false` | Tipo lógico estrito |
| Null | `null` | Ausência de valor |

O lexer reconhece sequências de escape `\\n`, `\\t`, `\\"` e `\\\\` em strings.

## 4. Variáveis, atribuição e saída

```nyx
let samples = 120
let ratio = 0.875
let title = "NYX"

print(title)
print(samples * ratio)

samples = samples + 1
print(samples)
```

- `let nome = expressão` declara uma variável no escopo atual.
- Uma variável não pode ser declarada novamente no mesmo escopo.
- `nome = expressão` atualiza uma variável já declarada, procurando do escopo mais interno para o mais externo.
- Atribuir a um identificador não declarado gera erro de execução.
- `print(expressão)` avalia a expressão e envia o valor ao mecanismo de saída.

## 5. Expressões e operadores

Da menor para a maior precedência:

| Nível | Operadores / formas | Associatividade |
|---:|---|---|
| 1 | `or` | Esquerda |
| 2 | `and` | Esquerda |
| 3 | `==`, `!=` | Esquerda |
| 4 | `<`, `<=`, `>`, `>=` | Esquerda |
| 5 | `+`, `-` binários | Esquerda |
| 6 | `*`, `/`, `%` | Esquerda |
| 7 | `not`, `+` unário, `-` unário | Prefixa |
| 8 | Literais, identificadores e agrupamento | Primária |

Regras semânticas:

- Operadores aritméticos exigem operandos numéricos; booleanos não são aceitos como números.
- Operadores relacionais aceitam operandos numéricos.
- Igualdade compara tipo e valor; valores de tipos distintos não são iguais.
- `and` e `or` exigem booleanos e usam avaliação de curto-circuito.
- `not` exige um booleano.
- Divisão e módulo por zero geram erro de execução.
- O operador `!` isolado não é suportado; use `not`.

## 6. Controle de fluxo e escopos

### Condicional

```nyx
if (10 > 3) {
    print("condição verdadeira")
} else {
    print("condição falsa")
}
```

O bloco `else` é opcional. A condição precisa resultar em Boolean.

### Laço

```nyx
let index = 0
while (index < 4) {
    print(index)
    index = index + 1
}
```

A condição é reavaliada antes de cada iteração e precisa resultar em Boolean.

### Blocos e resolução de nomes

- O programa começa em um escopo global.
- Cada bloco executado cria um escopo local.
- A busca de variáveis percorre os escopos do mais interno ao mais externo.
- Uma declaração interna pode ocultar uma variável externa de mesmo nome.
- A atribuição atualiza a declaração visível mais próxima.
- O escopo local é descartado ao término do bloco, inclusive quando ocorre erro durante sua execução.

## 7. Gramática sintática (EBNF)

A gramática abaixo descreve a estrutura sintática. A delimitação implícita de instruções depende também das posições de linha dos tokens, conforme a seção 2; `line_terminator` é uma condição do parser, não um token produzido pelo lexer.

```ebnf
program             = { statement } , EOF ;

statement           = declaration
                    | assignment
                    | print_statement
                    | if_statement
                    | while_statement
                    | block ;

declaration         = "let" , identifier , "=" , expression , terminator ;
assignment          = identifier , "=" , expression , terminator ;
print_statement     = "print" , "(" , expression , ")" , terminator ;

if_statement        = "if" , "(" , expression , ")" , block
                    , [ "else" , block ] ;
while_statement     = "while" , "(" , expression , ")" , block ;
block               = "{" , { statement } , "}" ;

terminator          = ";" | line_terminator | "}" | EOF ;

expression          = logical_or ;
logical_or          = logical_and , { "or" , logical_and } ;
logical_and         = equality , { "and" , equality } ;
equality            = comparison , { ( "==" | "!=" ) , comparison } ;
comparison          = term , { ( "<" | "<=" | ">" | ">=" ) , term } ;
term                = factor , { ( "+" | "-" ) , factor } ;
factor              = unary , { ( "*" | "/" | "%" ) , unary } ;
unary               = ( "not" | "+" | "-" ) , unary | primary ;
primary             = number | string | "true" | "false" | "null"
                    | identifier | "(" , expression , ")" ;

number              = integer | float ;
identifier          = ( letter | "_" ) , { letter | digit | "_" } ;
```

## 8. Léxico e diagnósticos

Tokens reconhecidos incluem palavras-chave, identificadores, literais, operadores aritméticos, operadores relacionais, operadores lógicos, parênteses, chaves e ponto e vírgula.

Erros léxicos, sintáticos e de execução usam o formato `[NYX:Lx:Cy]`, com linha e coluna de origem. O interpretador interrompe o programa no primeiro erro. Ainda não há recuperação de erros sintáticos para continuar a análise de um mesmo arquivo.

## 9. Pipeline de execução implementado

1. Leitura do código-fonte como texto.
2. Análise léxica: fonte para tokens.
3. Análise sintática: tokens para AST.
4. Interpretação: avaliação da AST e execução das instruções.

A AST representa expressões e instruções. O interpretador percorre essa árvore diretamente (tree-walk). Ainda não existe uma etapa independente de análise semântica estática, geração de IR, compilação ou máquina virtual.

## 10. Recursos ainda não implementados

Não fazem parte da versão 0.4:

- Funções definidas pelo usuário, parâmetros, retorno e recursividade.
- Coleções nativas, como listas, mapas, conjuntos e tensores.
- Módulos, pacotes e sistema de importação.
- Sistema de tipos estático, inferência de tipos e genéricos.
- Classes, estruturas e traits/interfaces.
- Laços `for`, `break` e `continue`.
- Tratamento de exceções na linguagem.
- Análise semântica estática e resolução antecipada de símbolos.
- Representação intermediária (IR), compilador, bytecode e máquina virtual.
- Concorrência, paralelismo e gerenciamento próprio de memória.
- Bibliotecas científicas, operações tabulares e conectores de dados.
- Integração nativa com IA.

Esses itens pertencem ao planejamento evolutivo e não devem ser tratados como capacidades disponíveis nesta versão.

## 11. Independência e evolução

A gramática, o lexer, o parser, a AST e as regras de avaliação pertencem à NYX. A implementação hospedeira poderá ser substituída ou complementada no futuro, desde que a semântica especificada seja preservada por testes de conformidade.

A evolução deve manter separadas a linguagem, o runtime, as bibliotecas científicas e as integrações externas.
