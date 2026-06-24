#!/usr/bin/env python3
"""Run the CARP v0.2.3 engine against the adversarial fixture suite."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine_v02_3 import CompatibilityEvaluator


def flatten_lifecycle_warnings(result: dict) -> list[dict]:
    warnings = []
    for items in result.get("metadata", {}).get("lifecycle_warnings", {}).values():
        warnings.extend(items or [])
    return warnings


def check_expected(result: dict, expected_doc: dict) -> list[str]:
    """Evaluate fixture expectations.

    Supports both the fixture wrapper shape:
      {"expected_result": {...}}
    and a direct expectation object. This runner intentionally checks every
    assertion key used by the adversarial fixture suite, so a fixture cannot
    pass merely because its assertion key was ignored.
    """
    expected = expected_doc.get("expected_result", expected_doc)
    failures = []
    res = result.get("result", {})
    classification = res.get("classification")

    if "classification" in expected and classification != expected["classification"]:
        failures.append(f"classification expected {expected['classification']} got {classification}")
    if "desired_classification" in expected and classification != expected["desired_classification"]:
        failures.append(f"desired_classification expected {expected['desired_classification']} got {classification}")
    if "must_not_be" in expected and classification == expected["must_not_be"]:
        failures.append(f"classification must not be {expected['must_not_be']}")
    if "must_not_classify_as" in expected and classification in set(expected["must_not_classify_as"]):
        failures.append(f"classification must not be in {expected['must_not_classify_as']}")

    if expected.get("compatibility_confidence") is None and "compatibility_confidence" in expected and res.get("confidence") is not None:
        failures.append(f"confidence expected null got {res.get('confidence')}")
    if "expected_confidence_min" in expected:
        conf = res.get("confidence")
        if conf is None or conf < expected["expected_confidence_min"]:
            failures.append(f"confidence expected >= {expected['expected_confidence_min']} got {conf}")
    if "must_have_evaluation_confidence" in expected and res.get("evaluation_confidence") != expected["must_have_evaluation_confidence"]:
        failures.append(f"evaluation_confidence expected {expected['must_have_evaluation_confidence']} got {res.get('evaluation_confidence')}")

    metadata = result.get("metadata", {})
    if "must_have_scope_warning_count_at_least" in expected:
        count = len(metadata.get("scope_warnings", []))
        if count < expected["must_have_scope_warning_count_at_least"]:
            failures.append(f"scope_warning_count expected >= {expected['must_have_scope_warning_count_at_least']} got {count}")
    if "must_include_scope_gap_reason" in expected:
        reasons = {w.get("reason") for w in metadata.get("scope_warnings", [])}
        if expected["must_include_scope_gap_reason"] not in reasons:
            failures.append(f"missing scope warning reason {expected['must_include_scope_gap_reason']}")
    if "must_have_scope_warning_type" in expected:
        types = {w.get("warning_type") for w in metadata.get("scope_warnings", [])}
        if expected["must_have_scope_warning_type"] not in types:
            failures.append(f"missing scope warning type {expected['must_have_scope_warning_type']}")

    if "must_have_lifecycle_warning_type" in expected:
        types = {w.get("warning_type") for w in flatten_lifecycle_warnings(result)}
        if expected["must_have_lifecycle_warning_type"] not in types:
            failures.append(f"missing lifecycle warning type {expected['must_have_lifecycle_warning_type']}")
    if "must_have_filter_summary_expired_at_least" in expected:
        total = sum((s or {}).get("expired", 0) for s in metadata.get("filter_summary", {}).values())
        if total < expected["must_have_filter_summary_expired_at_least"]:
            failures.append(f"expired filter count expected >= {expected['must_have_filter_summary_expired_at_least']} got {total}")
    if "must_filter_superseded_count_at_least" in expected:
        total = sum((s or {}).get("superseded", 0) for s in metadata.get("filter_summary", {}).values())
        if total < expected["must_filter_superseded_count_at_least"]:
            failures.append(f"superseded filter count expected >= {expected['must_filter_superseded_count_at_least']} got {total}")

    if "must_not_have_pass_reason" in expected:
        reasons = []
        for item in result.get("constraint_evaluation", {}).get("passed_constraints", []):
            reasons.extend(tr.get("reason_code") for tr in item.get("trace", []))
        if expected["must_not_have_pass_reason"] in reasons:
            failures.append(f"found forbidden pass reason {expected['must_not_have_pass_reason']}")
    if "must_have_unknown_constraint_reason" in expected:
        reasons = []
        for item in result.get("constraint_evaluation", {}).get("unknown_constraints", []):
            reasons.extend(tr.get("reason_code") for tr in item.get("trace", []))
        if expected["must_have_unknown_constraint_reason"] not in reasons:
            failures.append(f"missing unknown constraint reason {expected['must_have_unknown_constraint_reason']}")
    if "must_have_blocking_domain" in expected:
        domains = {c.get("domain") for c in result.get("constraint_evaluation", {}).get("blocking_constraints", [])}
        if expected["must_have_blocking_domain"] not in domains:
            failures.append(f"missing blocking domain {expected['must_have_blocking_domain']}")
    if "must_have_blocking_constraint_type" in expected:
        ctypes = {c.get("constraint_type") for c in result.get("constraint_evaluation", {}).get("blocking_constraints", [])}
        if expected["must_have_blocking_constraint_type"] not in ctypes:
            failures.append(f"missing blocking constraint_type {expected['must_have_blocking_constraint_type']}")

    scored = metadata.get("objects_scored", {})
    claims_scored_expected = expected.get("claims_scored")
    if claims_scored_expected is not None and scored.get("claims_scored") != claims_scored_expected:
        failures.append(f"claims_scored expected {claims_scored_expected} got {scored.get('claims_scored')}")
    if expected.get("must_have_claims_scored_zero") and scored.get("claims_scored") != 0:
        failures.append("claims_scored was not zero")

    if expected.get("must_have_profile_divergence"):
        if not result.get("divergences", {}).get("profile_divergences"):
            failures.append("expected at least one profile divergence")
    if expected.get("must_generate_questions"):
        if not result.get("questions"):
            failures.append("expected generated questions")

    if "must_not_score_pattern_id" in expected:
        forbidden = expected["must_not_score_pattern_id"]
        pattern_section = result.get("pattern_comparison", {})
        scored_ids = set()
        for bucket in ("strong_alignments", "moderate_alignments", "tensions", "risks", "unknowns"):
            for item in pattern_section.get(bucket, []):
                for key in ("profile_a_pattern_id", "profile_b_pattern_id"):
                    if item.get(key):
                        scored_ids.add(item[key])
        if forbidden in scored_ids:
            failures.append(f"forbidden pattern id was scored: {forbidden}")

    return failures

def main() -> int:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Run CARP adversarial fixture checks.")
    parser.add_argument("--suite", type=Path, default=root / "carp_v023_adversarial_fixtures")
    parser.add_argument("--schema-dir", type=Path, default=root / "carp_v022_conformance_suite" / "schemas", help="Schema directory used by the engine for input validation.")
    parser.add_argument("--write-outputs", action="store_true", help="Write observed JSON outputs into each fixture folder.")
    args = parser.parse_args()
    evaluator = CompatibilityEvaluator(args.schema_dir)

    failures = []
    rows = []
    for fixture_dir in sorted(args.suite.glob("AF-*")):
        profile_a = fixture_dir / "profile_a.json"
        profile_b = fixture_dir / "profile_b.json"
        expected_path = fixture_dir / "expected_result.json"
        if not profile_a.exists() or not profile_b.exists():
            continue
        result = evaluator.evaluate_files(profile_a, profile_b)
        expected = json.loads(expected_path.read_text()) if expected_path.exists() else {}
        item_failures = check_expected(result, expected)
        rows.append((fixture_dir.name, result.get("result", {}).get("classification"), item_failures))
        failures.extend((fixture_dir.name, f) for f in item_failures)
        if args.write_outputs:
            (fixture_dir / "observed_engine_v023_local.json").write_text(json.dumps(result, indent=2))

    for name, classification, item_failures in rows:
        print(f"{name}: {classification} {'PASS' if not item_failures else 'FAIL'}")
        for failure in item_failures:
            print(f"  - {failure}")
    if failures:
        print("\nAdversarial suite failed.")
        return 1
    print("\nAdversarial suite passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
