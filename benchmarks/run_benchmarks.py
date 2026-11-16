"""Reproducible NYX microbenchmarks.

Measures complete NYX source execution (lex + parse + tree-walk), cached-AST
tree-walk execution, and a Python reference compiled/executed on each sample.
The Python reference is a baseline, not a claim of equivalent language runtimes.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import statistics
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

from nyx import Interpreter, Lexer, Parser, run

# Keep workloads deterministic and small enough for repeatable CI measurements.
# Add scientific kernels only when the corresponding NYX features are executable.
WORKLOADS = {
    "arithmetic_loop": {
        "operations": 300,
        "nyx": """let i = 0
let total = 0
while (i < 300) {
    total = total + i
    i = i + 1
}
print(total)
""",
        "python": """def main():
    total = 0
    for i in range(300):
        total += i
    return total
""",
        "expected": 44850,
    },
    "list_append": {
        "operations": 150,
        "nyx": """let values = []
let i = 0
while (i < 150) {
    append(values, i)
    i = i + 1
}
print(len(values))
""",
        "python": """def main():
    values = []
    for i in range(150):
        values.append(i)
    return len(values)
""",
        "expected": 150,
    },
}


def _nyx_end_to_end(source: str, expected: object) -> None:
    output: list[object] = []
    run(source, output=output.append)
    if output != [expected]:
        raise AssertionError(f"NYX output mismatch: {output!r} != {[expected]!r}")


def _nyx_cached_ast(statements: list, expected: object) -> None:
    output: list[object] = []
    Interpreter(output=output.append).interpret(statements)
    if output != [expected]:
        raise AssertionError(f"NYX AST output mismatch: {output!r} != {[expected]!r}")


def _python_reference(source: str, expected: object) -> None:
    namespace: dict[str, object] = {}
    exec(compile(source, "<nyx-benchmark-python-reference>", "exec"), namespace)
    result = namespace["main"]()
    if result != expected:
        raise AssertionError(f"Python output mismatch: {result!r} != {expected!r}")


def _measure(callable_, warmups: int, repetitions: int) -> dict[str, float]:
    for _ in range(warmups):
        callable_()

    samples_ms: list[float] = []
    peak_bytes: list[int] = []
    for _ in range(repetitions):
        tracemalloc.start()
        start = time.perf_counter_ns()
        callable_()
        elapsed = (time.perf_counter_ns() - start) / 1_000_000
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        samples_ms.append(elapsed)
        peak_bytes.append(peak)

    ordered = sorted(samples_ms)
    p95_index = min(len(ordered) - 1, max(0, int(0.95 * len(ordered) + 0.5) - 1))
    median_ms = statistics.median(samples_ms)
    return {
        "median_ms": median_ms,
        "p95_ms": ordered[p95_index],
        "stdev_ms": statistics.stdev(samples_ms) if len(samples_ms) > 1 else 0.0,
        "peak_memory_kib": statistics.median(peak_bytes) / 1024,
    }


def _svg_chart(path: Path, title: str, ylabel: str, rows: list[dict], metric: str,
               scale: float = 1.0, suffix: str = "") -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise SystemExit("Install matplotlib and numpy to render benchmark charts.") from exc

    workloads = list(WORKLOADS)
    runtimes = ["NYX end-to-end", "NYX cached AST", "Python reference"]
    colors = ["#00D9FF", "#168BFF", "#9BB8CC"]
    x = np.arange(len(workloads))
    width = 0.23
    fig, ax = plt.subplots(figsize=(11, 5.6), dpi=150)
    fig.patch.set_facecolor("#050B18")
    ax.set_facecolor("#0B1B31")

    for index, runtime in enumerate(runtimes):
        values = []
        for workload in workloads:
            row = next(r for r in rows if r["runtime"] == runtime and r["workload"] == workload)
            values.append(float(row[metric]) * scale)
        bars = ax.bar(x + (index - 1) * width, values, width, label=runtime,
                      color=colors[index], edgecolor="#60E6FF", linewidth=0.45)
        ax.bar_label(bars, fmt=f"%.{2 if metric != 'peak_memory_kib' else 1}f{suffix}",
                     padding=3, color="#F2FAFF", fontsize=8)

    ax.set_title(title, color="#F2FAFF", fontsize=15, fontweight="bold", loc="left", pad=18)
    ax.set_ylabel(ylabel, color="#9BB8CC")
    ax.set_xticks(x, [w.replace("_", " ").title() for w in workloads], color="#F2FAFF")
    ax.tick_params(axis="y", colors="#9BB8CC")
    ax.grid(axis="y", color="#397BFF", alpha=0.25, linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#24517A")
    ax.legend(frameon=False, labelcolor="#F2FAFF", ncols=3, loc="upper right")
    fig.text(0.01, 0.01, "Measured locally by GitHub Actions · lower is better"
             if metric != "throughput_ops_s" else
             "Measured locally by GitHub Actions · higher is better",
             color="#9BB8CC", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run reproducible NYX runtime benchmarks.")
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--repetitions", type=int, default=25)
    parser.add_argument("--output-dir", type=Path, default=Path("benchmarks/results"))
    parser.add_argument("--chart-dir", type=Path, default=Path("assets/benchmarks"))
    args = parser.parse_args()
    if args.warmups < 0 or args.repetitions < 3:
        parser.error("warmups must be >= 0 and repetitions must be >= 3")

    rows: list[dict[str, object]] = []
    for workload, spec in WORKLOADS.items():
        source, py_source, expected = spec["nyx"], spec["python"], spec["expected"]
        ast = Parser(Lexer(source).scan_tokens()).parse()
        calls = {
            "NYX end-to-end": lambda s=source, e=expected: _nyx_end_to_end(s, e),
            "NYX cached AST": lambda a=ast, e=expected: _nyx_cached_ast(a, e),
            "Python reference": lambda s=py_source, e=expected: _python_reference(s, e),
        }
        for runtime, callable_ in calls.items():
            result = _measure(callable_, args.warmups, args.repetitions)
            operations = int(spec["operations"])
            rows.append({
                "runtime": runtime,
                "workload": workload,
                "operations": operations,
                **result,
                "throughput_ops_s": operations / (result["median_ms"] / 1000),
            })

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.chart_dir.mkdir(parents=True, exist_ok=True)
    fields = ["runtime", "workload", "operations", "median_ms", "p95_ms",
              "stdev_ms", "throughput_ops_s", "peak_memory_kib"]
    with (args.output_dir / "latest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor() or "not reported",
        "warmups": args.warmups,
        "repetitions": args.repetitions,
        "method": "median of wall-clock samples; tracemalloc peak sampled per invocation",
        "scope": "NYX end-to-end includes lexing, parsing and tree-walk; cached AST excludes lexing/parsing; Python reference compiles and executes equivalent loop code",
        "results": rows,
    }
    (args.output_dir / "latest.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    _svg_chart(args.chart_dir / "latency.svg", "Execution latency", "Median latency (ms)",
               rows, "median_ms", suffix=" ms")
    _svg_chart(args.chart_dir / "throughput.svg", "Workload throughput", "Operations / second",
               rows, "throughput_ops_s", suffix=" op/s")
    _svg_chart(args.chart_dir / "memory.svg", "Peak traced memory", "Peak memory (KiB)",
               rows, "peak_memory_kib", suffix=" KiB")

    print(f"Benchmark complete: {len(rows)} measurements, {args.repetitions} repetitions each.")
    print(f"CSV: {args.output_dir / 'latest.csv'}")
    print(f"JSON: {args.output_dir / 'latest.json'}")
    print(f"Charts: {args.chart_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
