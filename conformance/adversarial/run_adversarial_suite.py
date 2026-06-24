#!/usr/bin/env python3
"""Run CARP v0.2.3 adversarial fixtures against engine_v02_3.py."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path


def flatten_lifecycle_warnings(result):
    warnings=[]
    for items in result.get('metadata', {}).get('lifecycle_warnings', {}).values():
        warnings.extend(items or [])
    return warnings


def check_expected(result, expected):
    failures=[]
    res=result.get('result', {})
    if 'classification' in expected and res.get('classification') != expected['classification']:
        failures.append(f"classification expected {expected['classification']} got {res.get('classification')}")
    if 'must_not_be' in expected and res.get('classification') == expected['must_not_be']:
        failures.append(f"classification must not be {expected['must_not_be']}")
    if expected.get('compatibility_confidence') is None and 'compatibility_confidence' in expected and res.get('confidence') is not None:
        failures.append(f"confidence expected null got {res.get('confidence')}")
    if 'must_have_evaluation_confidence' in expected and res.get('evaluation_confidence') != expected['must_have_evaluation_confidence']:
        failures.append(f"evaluation_confidence expected {expected['must_have_evaluation_confidence']} got {res.get('evaluation_confidence')}")
    if 'must_have_scope_warning_count_at_least' in expected:
        count=len(result.get('metadata', {}).get('scope_warnings', []))
        if count < expected['must_have_scope_warning_count_at_least']:
            failures.append(f"scope_warning_count expected >= {expected['must_have_scope_warning_count_at_least']} got {count}")
    if 'must_include_scope_gap_reason' in expected:
        reasons={w.get('reason') for w in result.get('metadata', {}).get('scope_warnings', [])}
        if expected['must_include_scope_gap_reason'] not in reasons:
            failures.append(f"missing scope warning reason {expected['must_include_scope_gap_reason']}")
    if 'must_have_scope_warning_type' in expected:
        types={w.get('warning_type') for w in result.get('metadata', {}).get('scope_warnings', [])}
        if expected['must_have_scope_warning_type'] not in types:
            failures.append(f"missing scope warning type {expected['must_have_scope_warning_type']}")
    if 'must_have_lifecycle_warning_type' in expected:
        types={w.get('warning_type') for w in flatten_lifecycle_warnings(result)}
        if expected['must_have_lifecycle_warning_type'] not in types:
            failures.append(f"missing lifecycle warning type {expected['must_have_lifecycle_warning_type']}")
    if 'must_have_filter_summary_expired_at_least' in expected:
        total=sum((s or {}).get('expired', 0) for s in result.get('metadata', {}).get('filter_summary', {}).values())
        if total < expected['must_have_filter_summary_expired_at_least']:
            failures.append(f"expired filter count expected >= {expected['must_have_filter_summary_expired_at_least']} got {total}")
    if 'must_not_have_pass_reason' in expected:
        reasons=[]
        for item in result.get('constraint_evaluation', {}).get('passed_constraints', []):
            for tr in item.get('trace', []):
                reasons.append(tr.get('reason_code'))
        if expected['must_not_have_pass_reason'] in reasons:
            failures.append(f"found forbidden pass reason {expected['must_not_have_pass_reason']}")
    if 'must_have_unknown_constraint_reason' in expected:
        reasons=[]
        for item in result.get('constraint_evaluation', {}).get('unknown_constraints', []):
            for tr in item.get('trace', []):
                reasons.append(tr.get('reason_code'))
        if expected['must_have_unknown_constraint_reason'] not in reasons:
            failures.append(f"missing unknown constraint reason {expected['must_have_unknown_constraint_reason']}")
    if 'must_have_blocking_domain' in expected:
        domains={c.get('domain') for c in result.get('constraint_evaluation', {}).get('blocking_constraints', [])}
        if expected['must_have_blocking_domain'] not in domains:
            failures.append(f"missing blocking domain {expected['must_have_blocking_domain']}")
    if 'must_have_blocking_constraint_type' in expected:
        ctypes={c.get('constraint_type') for c in result.get('constraint_evaluation', {}).get('blocking_constraints', [])}
        if expected['must_have_blocking_constraint_type'] not in ctypes:
            failures.append(f"missing blocking constraint_type {expected['must_have_blocking_constraint_type']}")
    if expected.get('must_have_claims_scored_zero'):
        if result.get('metadata', {}).get('objects_scored', {}).get('claims_scored') != 0:
            failures.append('claims_scored was not zero')
    return failures


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--engine', type=Path, default=Path('/mnt/data/engine_v02_3.py'))
    ap.add_argument('--suite', type=Path, default=Path('/mnt/data/carp_v023_adversarial_fixtures'))
    args=ap.parse_args()
    failures=[]
    rows=[]
    for d in sorted(args.suite.glob('AF-*')):
        a=d/'profile_a.json'; b=d/'profile_b.json'; e=d/'expected_result.json'
        if not a.exists(): continue
        out=subprocess.check_output([sys.executable, str(args.engine), str(a), str(b)], text=True)
        result=json.loads(out)
        expected=json.loads(e.read_text()) if e.exists() else {}
        item_failures=check_expected(result, expected)
        rows.append((d.name, result['result']['classification'], item_failures))
        failures.extend((d.name, f) for f in item_failures)
    for name, classification, item_failures in rows:
        print(f"{name}: {classification} {'PASS' if not item_failures else 'FAIL'}")
        for f in item_failures:
            print(f"  - {f}")
    if failures:
        sys.exit(1)

if __name__ == '__main__':
    main()
