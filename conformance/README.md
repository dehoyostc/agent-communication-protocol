# Conformance Suite

This directory contains the CARP v0.2 conformance suite, adversarial fixtures, and test runner.

## Structure

```
conformance/
├── tests/          — conformance test runner and expected outcomes
├── fixtures/       — named entity profiles used in conformance tests
└── adversarial/    — adversarial fixtures (AF-001 through AF-013)
```

## Running conformance tests

```bash
python engine/run_conformance.py
```

## Running adversarial fixtures

```bash
python engine/run_adversarial.py
```

## Adversarial fixtures

Each `AF-XXX` folder contains:
- `README.md` — description of the adversarial scenario
- `profile_a.json` / `profile_b.json` — input profiles
- `expected_result.json` — what a conforming engine must produce
- `observed_engine_v023.json` — actual output from engine v0.2.3

### Known issue: AF-009 (pattern stuffing)

AF-009 tests that a candidate with 50 low-evidence duplicate positive patterns
does not auto-promote to `good_match`.

**Status in v0.2.3:** Fixed. The engine correctly produces `ambiguous_match`
via `MAX_POSITIVE_TAG_GROUP_DELTA` capping. Prior v0.2.2 behavior
(incorrectly passing) is preserved in `observed_engine_v022_results.json`
for reference.

The v0.2.2 conformance suite reported 13/13 passes despite this check not
being enforced — the key mismatch meant the pattern stuffing test was not
actually validated. This is documented here for transparency.
