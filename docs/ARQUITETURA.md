# Arquitetura da NYX

## 1. Diretriz arquitetural

A NYX será uma linguagem independente. Sua implementação não deve delegar a semântica da linguagem a Python, nem tratar bibliotecas externas como substitutas de seus componentes centrais.

A primeira implementação poderá utilizar Python como tecnologia de prototipação do compilador/interpretador. Essa escolha é de implementação, não uma dependência semântica da linguagem. A arquitetura deverá permitir a substituição progressiva da infraestrutura por componentes nativos, inclusive em Rust, sem alterar os programas NYX.

## 2. Pipeline de execução

O fluxo conceitual é:

`Código-fonte → Lexer → Parser → AST → Análise semântica → IR → Planejador/otimizador → Runtime`

Cada estágio terá contratos explícitos e testes independentes.

### Lexer

Converte caracteres em tokens, preservando posição no arquivo para diagnóstico preciso.

### Parser

Reconhece a gramática oficial e constrói uma árvore sintática abstrata (AST). Erros sintáticos devem indicar linha, coluna e contexto.

### Análise semântica e sistema de tipos

Verifica declarações, escopos, nomes, compatibilidade de tipos e regras de execução. Inferência de tipos deverá ser previsível e documentada.

### Representação intermediária (IR)

Desacopla a sintaxe da execução. A IR permitirá análise, transformação e otimização sem modificar o código-fonte.

### Planejador e otimizador

Aplica transformações válidas com preservação semântica. Otimizações fundamentais serão determinísticas e independentes de serviços de IA.

### Runtime

Executa as operações da linguagem e administra valores, erros, recursos e observabilidade.

## 3. Domínios da biblioteca padrão

- **Core:** entrada e saída, strings, coleções, erros e módulos.
- **Science:** álgebra, estatística, probabilidade, vetores, matrizes e tensores.
- **Data:** arquivos, tabelas, séries, conjuntos de dados e transformações.
- **AI:** interfaces para modelos, inferência e fluxos de aprendizado de máquina.

Os domínios serão adicionados por etapas e não devem antecipar funcionalidades ainda inexistentes.

## 4. Interoperabilidade

Conectores poderão integrar SQL, bancos de dados, arquivos, APIs e bibliotecas externas. A interoperabilidade deve ocorrer por interfaces delimitadas, com conversões explícitas e tratamento de erros.

A existência de adaptadores não altera a independência da gramática, do sistema de tipos ou do runtime.

## 5. Requisitos não funcionais

- Correção numérica e semântica.
- Reprodutibilidade e controle de aleatoriedade.
- Desempenho medido por benchmarks reproduzíveis.
- Diagnósticos úteis e rastreáveis.
- Segurança de memória e gestão previsível de recursos.
- Paralelismo com semântica documentada.
- Instalação e execução local.

## 6. Estratégia de evolução

1. Especificar sintaxe mínima e semântica.
2. Implementar lexer, parser e AST.
3. Implementar valores, escopos, tipos e runtime mínimo.
4. Criar testes de conformidade e diagnósticos.
5. Introduzir operações matemáticas e estatísticas.
6. Introduzir estruturas e operações de dados.
7. Projetar IR e otimizações com evidência de desempenho.
8. Integrar recursos de IA por interfaces desacopladas.

Nenhuma etapa será considerada concluída apenas por existir código: deverá haver testes, documentação e critérios objetivos de aceitação.
