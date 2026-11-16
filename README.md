# NYX — Numerical Yield eXchange

**Linguagem de programação científica orientada a dados**

*Think Scientifically. Compute Intelligently.*

NYX é um projeto autoral da NR TECH para desenvolver uma linguagem independente voltada à computação científica, à engenharia de dados e à integração de inteligência artificial.

> **Estado atual:** protótipo executável 0.1.0a1. O núcleo inicial já possui lexer, parser de descida recursiva, AST própria, interpretador e interface de linha de comando. A linguagem ainda está em estágio alfa e não oferece, nesta versão, estruturas tabulares, bibliotecas científicas, compilação nativa, IR ou recursos de IA.

## Identidade e propósito

- **N — Numerical:** fundamento matemático e computacional.
- **Y — Yield:** produção de resultados e conhecimento.
- **X — eXchange:** integração e interoperabilidade.

A NYX possui sintaxe, gramática, frontend, AST e regras de avaliação próprias. Python é utilizado como linguagem hospedeira do protótipo, não como gramática ou mecanismo semântico delegado.

## Núcleo implementado

- Lexer com localização de tokens.
- Parser recursivo e AST própria.
- Literais: Integer, Float, String, Boolean e Null.
- Declaração de variáveis com `let`.
- Expressões aritméticas, relacionais e lógicas.
- Precedência de operadores e agrupamento.
- Saída com `print(...)`.
- Diagnósticos léxicos, sintáticos e de execução com linha e coluna.
- CLI para executar arquivos `.nyx`.

## Exemplo executável

```nyx
let samples = 120;
let ratio = 0.875;
let title = "NYX — Numerical Yield eXchange";

print(title);
print(samples * ratio);
print(samples >= 100 and ratio < 1.0);
```

Consulte [examples/00_primeiro_programa.nyx](examples/00_primeiro_programa.nyx).

## Instalação para desenvolvimento

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/nrdataanalysis-1908/NYX.git
cd NYX
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências de desenvolvimento:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

# Linux/macOS
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Execute um programa:

```bash
nyx run examples/00_primeiro_programa.nyx
```

Ou, durante o desenvolvimento:

```bash
python -m nyx run examples/00_primeiro_programa.nyx
```

Execute os testes:

```bash
python -m pytest -q
```

## Especificação e arquitetura

- [Especificação inicial da linguagem](docs/ESPECIFICACAO_INICIAL.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Roadmap](docs/ROADMAP.md)
- [Exemplos científicos conceituais](docs/EXEMPLOS_CIENTIFICOS.md)

Os exemplos científicos anteriores continuam sendo propostas de sintaxe e domínio; apenas o exemplo `00_primeiro_programa.nyx` corresponde ao subconjunto executável do protótipo atual.

## Próximas etapas

1. Ampliar a cobertura de testes e consolidar diagnósticos.
2. Introduzir blocos, controle de fluxo e funções.
3. Formalizar análise semântica e sistema de tipos.
4. Desenvolver coleções e operações matemáticas.
5. Criar estruturas tabulares e operações de dados.
6. Projetar IR, otimização e paralelismo com benchmarks reproduzíveis.
7. Integrar recursos de IA por interfaces desacopladas.

## Licença

Apache License 2.0. Consulte [LICENSE](LICENSE).
