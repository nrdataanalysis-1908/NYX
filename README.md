# NYX — Numerical Yield eXchange

**Scientific Data Programming Language** · *Think Scientifically. Compute Intelligently.*
Uma linguagem independente da NR TECH.

> Versão **0.0.1** — pré-alfa. O que existe hoje é a fundação: lexer, parser, AST e um
> interpretador executável. Ciência de dados, IR, otimizador e IA são fases futuras e **ainda não existem**.

## Instalação (desenvolvimento)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Uso

```powershell
nyx run examples\hello.nyx
nyx run examples\mean.nyx
nyx tokens examples\hello.nyx    # depuração do lexer
nyx ast examples\hello.nyx       # depuração do parser
```

Exemplo (`examples/mean.nyx`):

```
fn calculate_mean(values: Array<Float64>) -> Float64:
    return sum(values) / len(values)

observations = [12.5, 14.0, 13.2, 15.8, 11.9]
print("média:", calculate_mean(observations))
```

## Testes

```powershell
pytest
```

## Estado atual (0.0.1)

| Área | Estado |
|---|---|
| Lexer com indentação, comentários, strings, números | Implementado e testado |
| Parser (precedência de operadores, `fn`, `if/elif/else`, `while`, `for`) | Implementado e testado |
| Interpretador tree-walking | Implementado e testado |
| Erros com arquivo, linha, coluna e trecho do código | Implementado e testado |
| Tipos: `Int`, `Float64`, `Bool`, `String`, `Null`, `Array` (dinâmicos e estritos) | Implementado |
| Anotações de tipo (`values: Array<Float64>`) | Lidas pelo parser, **não verificadas** |
| Sistema de tipos estático, IR, bytecode/VM | Não iniciado |
| DataFrames, estatística, IA, otimizador de execução | Não iniciado |

Gramática do subconjunto atual: [`docs/grammar.ebnf`](docs/grammar.ebnf).

## Estrutura

```
src/nyx/        lexer.py · parser.py · nodes.py · interpreter.py · errors.py · cli.py
tests/          testes por camada
examples/       programas .nyx
docs/           gramática formal
```

## Licença

MIT — ver [`LICENSE`](LICENSE).
