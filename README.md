# NYX — Numerical Yield eXchange

**Linguagem de programação científica orientada a dados**

*Think Scientifically. Compute Intelligently.*

NYX é um projeto autoral da NR TECH para conceber uma linguagem independente voltada à computação científica, à engenharia de dados e à integração de inteligência artificial.

> **Estado do projeto:** fase de especificação e estruturação. A gramática executável, o interpretador, o runtime, o sistema de tipos e o pacote instalável ainda não foram entregues. Os arquivos `.nyx` disponíveis neste estágio são exemplos conceituais de sintaxe e fluxo de trabalho; não devem ser tratados como programas executáveis.

## Objetivo

Desenvolver uma linguagem com sintaxe, gramática, frontend, representação intermediária, sistema de tipos e runtime próprios. A interoperabilidade com Python, SQL, bancos de dados e APIs será realizada por mecanismos de integração, sem transformar NYX em uma camada ou extensão dessas tecnologias.

## Diretrizes de projeto

- **Independência:** especificação e componentes centrais próprios.
- **Rigor científico:** precisão, consistência e reprodutibilidade.
- **Eficiência:** execução determinística e otimização mensurável.
- **Interoperabilidade:** integração com ecossistemas de dados e computação.
- **Observabilidade:** rastreabilidade de operações, erros e resultados.
- **Evolução incremental:** funcionalidades implementadas e validadas antes de serem declaradas disponíveis.

## Identidade

- **Nome:** NYX — Numerical Yield eXchange.
- **N:** Numerical — fundamento matemático e computacional.
- **Y:** Yield — produção de resultados e conhecimento.
- **X:** eXchange — integração e interoperabilidade.
- **Organização:** NR TECH.

## Documentação

- [Arquitetura](docs/ARQUITETURA.md)
- [Roadmap](docs/ROADMAP.md)
- [Exemplos científicos conceituais](docs/EXEMPLOS_CIENTIFICOS.md)

## Exemplos conceituais

Os arquivos em `examples/` ilustram cenários que a linguagem pretende atender, como análise de vendas, processamento de sensores e experimentos científicos. Eles documentam objetivos de sintaxe e API; ainda não podem ser executados por um interpretador NYX.

## Instalação e execução

Ainda não há uma distribuição instalável nem um comando `nyx` funcional nesta etapa. As instruções de instalação serão publicadas quando o código-fonte do frontend, runtime, CLI e testes estiver disponível e validado.

## Roadmap resumido

1. Consolidar especificação da linguagem e gramática formal.
2. Implementar lexer, parser e AST próprios.
3. Definir sistema de tipos e semântica.
4. Construir runtime e CLI com testes automatizados.
5. Desenvolver bibliotecas científicas e recursos de dados.
6. Evoluir para IR, otimização, paralelismo e integração com IA.
7. Publicar benchmarks, documentação e distribuição reproduzível.

Consulte [ROADMAP.md](docs/ROADMAP.md) para o planejamento detalhado.

## Contribuição

Contribuições, propostas de sintaxe e discussões arquiteturais são bem-vindas. Antes de propor funcionalidades, consulte a documentação para preservar a coerência da especificação.

## Licença

Este projeto está licenciado sob Apache License 2.0. Consulte o arquivo [LICENSE](LICENSE).
