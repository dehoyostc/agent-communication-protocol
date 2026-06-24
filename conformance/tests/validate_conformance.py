import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit("Install dependency first: pip install jsonschema")

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "schemas" / "profile.schema.json").read_text())
fixture_dir = ROOT / "fixtures"

validator = Draft202012Validator(schema, format_checker=FormatChecker())

failures = []
for path in sorted(fixture_dir.glob("*.profile.json")):
    instance = json.loads(path.read_text())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        failures.append((path.name, errors))
    else:
        print(f"PASS {path.name}")

if failures:
    print("\nValidation failures:")
    for name, errors in failures:
        print(f"\n{name}")
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "<root>"
            print(f"  - {loc}: {err.message}")
    raise SystemExit(1)

print("\nAll CARP v0.2 conformance fixtures passed schema validation.")
