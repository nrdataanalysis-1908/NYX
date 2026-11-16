"""Generate synthetic NYX benchmark preview data. Not measured performance."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "benchmarks" / "results" / "demo_synthetic.csv"
FIELDS = ["runtime", "workload", "operations", "median_ms", "p95_ms", "stdev_ms", "throughput_ops_s", "peak_memory_kib"]

def main():
    rows = list(csv.DictReader(SOURCE.open(encoding="utf-8")))
    payload = {
        "classification": "SYNTHETIC_DEMONSTRATION_NOT_MEASURED",
        "warning": "Illustrative values only. Not measured NYX performance.",
        "results": rows,
    }
    target = SOURCE.with_name("demo_synthetic.json")
    target.write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    print(f"Synthetic demo metadata written to {target}")

if __name__ == "__main__":
    main()
