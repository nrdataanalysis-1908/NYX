# Casos de uso para a especificação da NYX

Este documento registra três programas-proposta que serão usados como entradas de projeto para a gramática, a semântica e a biblioteca de dados da NYX.

> **Estado:** exemplos conceituais. Não são programas executáveis na versão atual e não representam funcionalidades implementadas.

## 1. Análise comercial

Arquivo: [01_analise_vendas.nyx](../examples/01_analise_vendas.nyx)

Necessidades de linguagem identificadas:

- leitura de arquivo CSV;
- declaração de valores tabulares;
- filtragem por expressão;
- seleção explícita de colunas;
- agrupamento por chave;
- agregações nomeadas;
- apresentação de resultados.

## 2. Análise de sensores

Arquivo: [02_analise_sensores.nyx](../examples/02_analise_sensores.nyx)

Necessidades adicionais:

- representação explícita de valores ausentes;
- comparação com `null`;
- filtros encadeados;
- estatísticas descritivas;
- preservação dos tipos numéricos;
- contagem de observações válidas.

## 3. Análise de experimento científico

Arquivo: [03_experimento_cientifico.nyx](../examples/03_experimento_cientifico.nyx)

Necessidades adicionais:

- mediana;
- tamanho amostral;
- dispersão estatística;
- nomenclatura de resultados;
- distinção entre dados ausentes e observações rejeitadas por critérios de qualidade.

## Núcleo comum extraído

Os três casos convergem para um primeiro domínio tabular mínimo:

1. `read_csv(path)`: carregar uma tabela e inferir ou validar seu esquema.
2. `filter(expression)`: selecionar linhas por expressão booleana.
3. `select(columns...)`: projetar colunas.
4. `group_by(keys...)`: definir agrupamento.
5. `aggregate(named_expressions...)`: calcular agregações.
6. `show()`: inspecionar o resultado no ambiente local.

## Decisões semânticas que ainda precisam ser formalizadas

- Como declarar variáveis e se a palavra `data` será um modificador de declaração ou um tipo.
- Se o encadeamento será baseado em ponto, operador de pipeline ou ambos.
- Como resolver nomes de colunas dentro de expressões.
- Como representar `null` e propagar valores ausentes em agregações.
- Qual será o tipo de retorno de cada transformação.
- Se a avaliação será eager, lazy ou híbrida.
- Como erros de coluna inexistente e tipos incompatíveis serão diagnosticados.
- Como garantir ordem determinística dos grupos e reprodutibilidade numérica.

## Critério de aceitação da primeira API tabular

A API inicial deverá executar os três cenários com resultados verificáveis, possuir testes positivos e negativos e documentar as regras para dados ausentes, tipos, agrupamento e agregações. Até lá, estes arquivos permanecem como propostas de sintaxe.
