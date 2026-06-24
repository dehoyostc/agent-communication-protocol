#!/usr/bin/env python3
"""Run the CARP v0.2.3 engine against the canonical conformance fixture pairs."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Run CARP canonical conformance checks.")
    parser.add_argument("--engine", type=Path, default=root / "engine_v02_3.py")
    parser.add_argument("--suite", type=Path, default=root / "carp_v022_conformance_suite")
    parser.add_argument("--write-outputs", action="store_true", help="Write observed JSON outputs next to this script under examples/conformance_outputs.")
    args = parser.parse_args()

    expected_path = args.suite / "docs" / "expected-outcomes.json"
    fixtures_dir = args.suite / "fixtures"
    schema_dir = args.suite / "schemas"
    expected = json.loads(expected_path.read_text())

    output_dir = root / "examples" / "conformance_outputs"
    if args.write_outputs:
        output_dir.mkdir(parents=True, exist_ok=True)

    failures = []
    for item in expected.get("fixture_pairs", []):
        a_name, b_name = item["pair"]
        expected_class = item["expected"]
        cmd = [
            sys.executable,
            str(args.engine),
            str(fixtures_dir / a_name),
            str(fixtures_dir / b_name),
            "--schema-dir",
            str(schema_dir),
        ]
        raw = subprocess.check_output(cmd, text=True)
        result = json.loads(raw)
        actual = result.get("result", {}).get("classification")
        label = f"{a_name} ↔ {b_name}"
        ok = actual == expected_class
        print(f"{label}: expected={expected_class} actual={actual} {'PASS' if ok else 'FAIL'}")
        if args.write_outputs:
            safe = label.replace(" ↔ ", "__").replace(".profile.json", "").replace(" ", "_")
            (output_dir / f"{safe}.json").write_text(json.dumps(result, indent=2))
        if not ok:
            failures.append((label, expected_class, actual))

    if failures:
        print("\nFailures:")
        for label, expected_class, actual in failures:
            print(f"- {label}: expected {expected_class}, got {actual}")
        return 1
    print("\nCanonical conformance suite passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
