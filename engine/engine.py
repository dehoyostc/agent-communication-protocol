#!/usr/bin/env python3
"""
CARP v0.2.3 deterministic compatibility engine.

Design commitments:
- Constraints are evaluated before compatibility.
- Patterns are the primary compatibility signal.
- Claims are used only for explanation.
- Divergences generate questions rather than automatic failures.
- Every conclusion carries trace metadata.

This implementation is intentionally conservative and inspectable. It is not an
LLM matcher; it is a rule-based CARP evaluator for v0.2 profiles.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    jsonschema = None


PROTOCOL_VERSION = "carp-0.2"
NOW = datetime.now(timezone.utc)

# Score normalization constants. Pattern deltas are deliberately small and
# transparent: +5 raw points maps to 1.0, -2.5 raw points maps to 0.0.
PATTERN_SCORE_BASELINE = 0.5
PATTERN_SCORE_SCALE = 5.0
MAX_POSITIVE_TAG_GROUP_DELTA = 1.00
MIN_GOOD_MATCH_CONFIDENCE = 0.40

CRITICAL_SCOPE_CATEGORIES = {"patterns", "constraints", "work_style", "work_environment", "communication", "compensation", "location"}

RELATIONSHIP_MULTIPLIERS = {
    "longitudinal": 1.15,
    "hybrid": 1.05,
    "transactional": 0.95,
    "document_based": 0.85,
}

NEGATION_TAGS = {
    "async": {"high_interaction", "collaborative", "team"},
    "isolated": {"collaborative", "team", "high_interaction"},
    "low_collaboration": {"collaborative", "team", "high_interaction"},
    "deep_work": {"high_meetings", "performative"},
    "autonomy": {"structured", "unclear_authority"},
    "collaborative": {"isolated", "low_collaboration"},
    "team": {"isolated", "low_collaboration"},
    "high_interaction": {"isolated", "low_collaboration", "deep_work"},
    "high_meetings": {"deep_work"},
    "performative": {"deep_work"},
    "management": {"independent", "deep_focus"},
    "team_growth": {"independent", "deep_focus"},
}


@dataclass
class Trace:
    source_object_ids: List[str]
    object_types: List[str]
    reason_code: str
    confidence_basis: str

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoadedProfile:
    path: Optional[str]
    raw: Dict[str, Any]
    objects_by_id: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    object_types_by_id: Dict[str, str] = field(default_factory=dict)
    filter_summary: Dict[str, int] = field(default_factory=dict)
    warnings: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def profile_id(self) -> str:
        return str(self.raw.get("profile_id", "unknown-profile"))

    @property
    def entity_id(self) -> str:
        return str(self.raw.get("entity", {}).get("id", "unknown-entity"))

    @property
    def handle(self) -> str:
        return str(self.raw.get("entity", {}).get("handle", self.entity_id))

    @property
    def relationship_depth(self) -> str:
        return str(self.raw.get("agent_relationship", {}).get("relationship_depth", "transactional"))

    @property
    def relationship_multiplier(self) -> float:
        return RELATIONSHIP_MULTIPLIERS.get(self.relationship_depth, 1.0)

    @property
    def purpose(self) -> Optional[str]:
        return self.raw.get("profile_scope", {}).get("purpose")

    @property
    def assessed_categories(self) -> set:
        return set(map(str.lower, self.raw.get("profile_scope", {}).get("assessed_categories") or []))

    @property
    def unassessed_categories(self) -> set:
        return set(map(str.lower, self.raw.get("profile_scope", {}).get("unassessed_categories") or []))

    @property
    def entity_authorized(self) -> Optional[bool]:
        return self.raw.get("agent_relationship", {}).get("entity_authorized")

    def claims(self) -> List[Dict[str, Any]]:
        return list(self.raw.get("claims") or [])

    def patterns(self) -> List[Dict[str, Any]]:
        return list(self.raw.get("patterns") or [])

    def constraints(self) -> List[Dict[str, Any]]:
        return list(self.raw.get("constraints") or [])

    def divergences(self) -> List[Dict[str, Any]]:
        return list(self.raw.get("divergences") or [])


class ProfileLoader:
    def __init__(self, schema_dir: Optional[Path] = None) -> None:
        self.schema_dir = schema_dir
        self.profile_schema: Optional[Dict[str, Any]] = None
        if schema_dir and (schema_dir / "profile.schema.json").exists():
            self.profile_schema = json.loads((schema_dir / "profile.schema.json").read_text())

    def load(self, path: Path) -> LoadedProfile:
        raw = json.loads(path.read_text())
        if raw.get("protocol_version") != PROTOCOL_VERSION:
            raise ValueError(f"{path}: expected protocol_version {PROTOCOL_VERSION}, got {raw.get('protocol_version')}")
        if self.profile_schema and jsonschema:
            jsonschema.validate(raw, self.profile_schema)
        profile = LoadedProfile(path=str(path), raw=raw)
        self._index(profile)
        return profile

    @staticmethod
    def _index(profile: LoadedProfile) -> None:
        for section, typ in [
            ("evidence", "evidence"),
            ("observations", "observation"),
            ("patterns", "pattern"),
            ("claims", "claim"),
            ("constraints", "constraint"),
            ("divergences", "divergence"),
        ]:
            for obj in profile.raw.get(section) or []:
                oid = obj.get("id")
                if oid:
                    profile.objects_by_id[oid] = obj
                    profile.object_types_by_id[oid] = typ


class LifecycleGuard:
    OPERATIVE_REMOVAL_STATES = {"archived", "revoked", "expired", "superseded"}

    def apply(self, profile: LoadedProfile, now: datetime = NOW) -> LoadedProfile:
        raw = dict(profile.raw)
        summary = {"expired": 0, "archived": 0, "revoked": 0, "superseded": 0, "kept": 0}
        warnings: List[Dict[str, Any]] = []
        warnings.extend(self._profile_time_warnings(raw, now))
        superseded_ids = self._superseded_ids(raw)

        for section in ["evidence", "observations", "patterns", "claims", "constraints", "divergences"]:
            kept = []
            for obj in raw.get(section) or []:
                state = self._lifecycle_state(obj)
                oid = obj.get("id")
                if oid in superseded_ids or state == "superseded":
                    summary["superseded"] += 1
                    continue
                if self._is_expired(obj, now) or state == "expired":
                    summary["expired"] += 1
                    continue
                if state == "archived":
                    summary["archived"] += 1
                    continue
                if state == "revoked":
                    summary["revoked"] += 1
                    continue
                kept.append(obj)
                summary["kept"] += 1
            raw[section] = kept

        guarded = LoadedProfile(path=profile.path, raw=raw, filter_summary=summary, warnings=warnings)
        ProfileLoader._index(guarded)
        warnings.extend(self._validate_linked_refs(guarded))
        warnings.extend(self._validate_divergence_refs(guarded))
        return guarded

    def _lifecycle_state(self, obj: Dict[str, Any]) -> str:
        lifecycle = obj.get("lifecycle") or {}
        return str(lifecycle.get("state", obj.get("lifecycle_state", obj.get("status", "")))).lower()

    def _superseded_ids(self, raw: Dict[str, Any]) -> set:
        ids = set()
        for section in ["evidence", "observations", "patterns", "claims", "constraints", "divergences"]:
            for obj in raw.get(section) or []:
                lifecycle = obj.get("lifecycle") or {}
                supersedes = lifecycle.get("supersedes", obj.get("supersedes"))
                if supersedes:
                    ids.add(supersedes)
        return ids

    def _is_expired(self, obj: Dict[str, Any], now: datetime) -> bool:
        lifecycle = obj.get("lifecycle") or {}
        expires_at = lifecycle.get("expires_at", obj.get("expires_at"))
        if not expires_at:
            return False
        try:
            dt = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
            return dt < now
        except Exception:
            return False

    def _profile_time_warnings(self, raw: Dict[str, Any], now: datetime) -> List[Dict[str, Any]]:
        warnings: List[Dict[str, Any]] = []
        generated_at = raw.get("generated_at")
        if generated_at:
            try:
                dt = datetime.fromisoformat(str(generated_at).replace("Z", "+00:00"))
                if dt > now:
                    warnings.append({
                        "warning_type": "profile_generated_in_future",
                        "generated_at": generated_at,
                        "message": "Profile generated_at is in the future relative to evaluator time; lifecycle/expiry behavior should be reviewed."
                    })
            except Exception:
                warnings.append({
                    "warning_type": "invalid_profile_generated_at",
                    "generated_at": generated_at,
                    "message": "Profile generated_at could not be parsed."
                })
        return warnings

    def _validate_linked_refs(self, profile: LoadedProfile) -> List[Dict[str, Any]]:
        warnings: List[Dict[str, Any]] = []
        for c in profile.constraints():
            for ref in c.get("linked_pattern_refs") or []:
                if ref not in profile.objects_by_id:
                    warnings.append({
                        "warning_type": "dangling_linked_pattern_ref",
                        "constraint_id": c.get("id"),
                        "missing_ref": ref,
                        "message": "Constraint linked_pattern_refs contains a reference that does not resolve after lifecycle filtering."
                    })
        return warnings

    def _validate_divergence_refs(self, profile: LoadedProfile) -> List[Dict[str, Any]]:
        warnings: List[Dict[str, Any]] = []
        for d in profile.divergences():
            for side in ["object_a", "object_b"]:
                ref = (d.get(side) or {}).get("object_id")
                if ref and ref not in profile.objects_by_id:
                    warnings.append({
                        "warning_type": "dangling_divergence_ref",
                        "divergence_id": d.get("id"),
                        "side": side,
                        "missing_ref": ref,
                        "message": "Divergence references an object that does not resolve after lifecycle filtering."
                    })
        return warnings


class TraceBuilder:
    @staticmethod
    def make(ids: Sequence[str], types: Sequence[str], reason_code: str, basis: str) -> Dict[str, Any]:
        return Trace(list(ids), list(types), reason_code, basis).to_json()


class ConstraintEvaluator:
    def evaluate(self, a: LoadedProfile, b: LoadedProfile) -> Dict[str, Any]:
        blocking, passed, unknown, tensions = [], [], [], []
        all_pairs = [(a, b), (b, a)]

        for left, right in all_pairs:
            for c in left.constraints():
                result = self._evaluate_single(c, left, right)
                if result["status"] == "hard_fail":
                    blocking.append(result)
                elif result["status"] in {"hard_pass", "soft_pass"}:
                    passed.append(result)
                elif result["status"] == "soft_tension":
                    tensions.append(result)
                else:
                    unknown.append(result)

        status = "passed"
        if blocking:
            status = "blocked"
        elif unknown:
            status = "unknown"
        elif tensions:
            status = "passed_with_tensions"

        return {
            "status": status,
            "blocking_constraints": blocking,
            "passed_constraints": passed,
            "unknown_constraints": unknown,
            "constraint_tensions": tensions,
        }

    def _evaluate_single(self, c: Dict[str, Any], owner: LoadedProfile, other: LoadedProfile) -> Dict[str, Any]:
        firmness = c.get("firmness", "soft")
        ctype = c.get("constraint_type")
        domain = c.get("domain")
        cid = c.get("id", "unknown-constraint")
        text = c.get("text", "")

        trace = TraceBuilder.make([cid], ["constraint"], "constraint_evaluated_first", "constraints are viability boundaries")

        # Compensation floor/ceiling pair.
        if domain == "compensation":
            if ctype == "floor":
                ceiling = self._find_constraint(other, "compensation", "ceiling")
                if ceiling:
                    ok = float(c.get("value", 0)) <= float(ceiling.get("value", 0))
                    return self._constraint_result(c, owner, other, "hard_pass" if ok else "hard_fail", text, [cid, ceiling.get("id")], "compensation_floor_vs_ceiling")
                return self._constraint_result(c, owner, other, "unknown", "No compensation ceiling found on opposing profile.", [cid], "missing_compensation_ceiling")
            if ctype == "ceiling":
                floor = self._find_constraint(other, "compensation", "floor")
                if floor:
                    ok = float(floor.get("value", 0)) <= float(c.get("value", 0))
                    return self._constraint_result(c, owner, other, "hard_pass" if ok else "hard_fail", text, [cid, floor.get("id")], "compensation_ceiling_vs_floor")
                return self._constraint_result(c, owner, other, "unknown", "No compensation floor found on opposing profile.", [cid], "missing_compensation_floor")

        # Location / fully remote requirement.
        # Important: async work style is not evidence of remote eligibility.
        # Remote/location requirements only pass against explicit opposing location constraints.
        if domain == "location" and ctype == "requirement":
            value = str(c.get("value", "")).lower().replace("-", "_").replace(" ", "_")
            explicit = self._explicit_location_values(other)
            remote_values = {"remote", "fully_remote", "remote_first", "distributed"}
            non_remote_values = {"on_site", "onsite", "in_office", "office", "hybrid_required", "hybrid", "relocation_required"}
            if value in remote_values:
                if explicit & remote_values:
                    status = "hard_pass" if firmness == "hard" else "soft_pass"
                    reason = "location_requirement_explicit_remote_match"
                elif explicit & non_remote_values:
                    status = "hard_fail" if firmness == "hard" else "soft_tension"
                    reason = "location_requirement_explicit_non_remote_conflict"
                else:
                    status = "unknown"
                    reason = "location_requirement_missing_explicit_location_constraint"
                return self._constraint_result(c, owner, other, status, text if status != "unknown" else "No explicit remote/location capability found on opposing profile.", [cid], reason)
            if value in non_remote_values:
                if explicit & non_remote_values:
                    status = "hard_pass" if firmness == "hard" else "soft_pass"
                    reason = "location_requirement_explicit_non_remote_match"
                elif explicit & remote_values:
                    status = "hard_fail" if firmness == "hard" else "soft_tension"
                    reason = "location_requirement_explicit_remote_conflict"
                else:
                    status = "unknown"
                    reason = "location_requirement_missing_explicit_location_constraint"
                return self._constraint_result(c, owner, other, status, text if status != "unknown" else "No explicit remote/location capability found on opposing profile.", [cid], reason)

        # Environment requirements are compared against opposing positive/negative patterns.
        if ctype == "environment_requirement" or domain in {"work_environment", "environment"}:
            required_tags = self._constraint_tags(c)
            if not required_tags:
                return self._constraint_result(c, owner, other, "unknown", "Environment requirement had no comparable tags.", [cid], "environment_requirement_no_tags")
            positive = self._pattern_tags_by_valence(other, "positive")
            negative = self._pattern_tags_by_valence(other, "negative")
            has_positive = bool(required_tags & positive)
            has_opposed = bool(required_tags & negative or self._opposing_tags(required_tags) & positive)
            if has_positive and not has_opposed:
                status = "hard_pass" if firmness == "hard" else "soft_pass"
            elif has_opposed or not has_positive:
                # v0.2.1 honors declared firmness: hard environment requirements block.
                # This prevents the v0.1-style false positive where a required environment
                # is unmet but the match survives due to unrelated positive patterns.
                status = "hard_fail" if firmness == "hard" else "soft_tension"
            else:
                status = "unknown"
            return self._constraint_result(c, owner, other, status, text, [cid], "environment_requirement_vs_patterns")

        # Soft requirements with opposing pattern tags produce tensions, not blocks.
        if ctype in {"requirement", "preference"}:
            tags = self._constraint_tags(c)
            if tags:
                pos = self._pattern_tags_by_valence(other, "positive")
                mixed = self._pattern_tags_by_valence(other, "mixed")
                if tags & pos:
                    return self._constraint_result(c, owner, other, "soft_pass" if firmness != "hard" else "hard_pass", text, [cid], "requirement_supported_by_patterns")
                if tags & mixed:
                    return self._constraint_result(c, owner, other, "soft_tension", text, [cid], "requirement_hits_mixed_pattern")
            return self._constraint_result(c, owner, other, "soft_tension" if firmness != "hard" else "unknown", text, [cid], "requirement_unresolved")

        return {"constraint_id": cid, "owner": owner.handle, "status": "unknown", "text": text, "trace": [trace]}

    def _constraint_result(self, c: Dict[str, Any], owner: LoadedProfile, other: LoadedProfile, status: str, text: str, ids: List[str], reason: str) -> Dict[str, Any]:
        return {
            "constraint_id": c.get("id"),
            "owner": owner.handle,
            "opposing_profile": other.handle,
            "status": status,
            "firmness": c.get("firmness"),
            "domain": c.get("domain"),
            "constraint_type": c.get("constraint_type"),
            "text": text,
            "trace": [TraceBuilder.make([i for i in ids if i], ["constraint"] * len([i for i in ids if i]), reason, "constraint comparison")],
        }

    def _find_constraint(self, p: LoadedProfile, domain: str, ctype: str) -> Optional[Dict[str, Any]]:
        for c in p.constraints():
            if c.get("domain") == domain and c.get("constraint_type") == ctype:
                return c
        return None

    def _constraint_tags(self, c: Dict[str, Any]) -> set:
        tags = set(map(str.lower, c.get("tags") or []))
        for v in [c.get("value"), c.get("domain"), c.get("text")]:
            if isinstance(v, str):
                normalized = v.lower().replace("-", "_").replace(" ", "_")
                tags.add(normalized)
                for token in normalized.replace(".", "").replace(",", "").split("_"):
                    if token:
                        tags.add(token)
        return tags


    def _explicit_location_values(self, p: LoadedProfile) -> set:
        values = set()
        for c in p.constraints():
            if c.get("domain") == "location":
                for v in [c.get("value"), c.get("text"), c.get("constraint_type")]:
                    if isinstance(v, str):
                        norm = v.lower().replace("-", "_").replace(" ", "_")
                        values.add(norm)
                        values |= {tok for tok in norm.replace(",", "").replace(".", "").split("_") if tok}
                values |= set(map(str.lower, c.get("tags") or []))
        return values

    def _all_pattern_tags(self, p: LoadedProfile) -> set:
        tags = set()
        for pat in p.patterns():
            tags |= set(map(str.lower, pat.get("environment_profile", {}).get("tags") or []))
        return tags

    def _pattern_tags_by_valence(self, p: LoadedProfile, valence: str) -> set:
        tags = set()
        for pat in p.patterns():
            if pat.get("outcome_valence") == valence:
                tags |= set(map(str.lower, pat.get("environment_profile", {}).get("tags") or []))
        return tags

    def _opposing_tags(self, tags: Iterable[str]) -> set:
        out = set()
        for t in tags:
            out |= NEGATION_TAGS.get(t, set())
        return out


class PatternComparator:
    def compare(self, a: LoadedProfile, b: LoadedProfile) -> Dict[str, Any]:
        alignments, moderate, tensions, risks, unknowns = [], [], [], [], []
        raw_score = 0.0
        raw_conf = 0.0
        comparisons = 0
        positive_group_contrib: Dict[Tuple[Any, ...], float] = {}
        capped_positive_groups: Dict[str, Dict[str, Any]] = {}

        for pa in a.patterns():
            for pb in b.patterns():
                cmp = self._compare_pair(pa, pb, a, b)
                if not cmp:
                    continue
                comparisons += 1
                kind = cmp.pop("kind")
                effective_delta = cmp["score_delta"]
                if effective_delta > 0:
                    group_key = tuple(cmp.get("tag_group_key") or [])
                    previous = positive_group_contrib.get(group_key, 0.0)
                    allowed = max(0.0, MAX_POSITIVE_TAG_GROUP_DELTA - previous)
                    capped_delta = min(effective_delta, allowed)
                    positive_group_contrib[group_key] = previous + capped_delta
                    if capped_delta < effective_delta:
                        capped_positive_groups[str(group_key)] = {
                            "tag_group_key": list(group_key),
                            "attempted_delta": round(previous + effective_delta, 3),
                            "applied_delta": round(positive_group_contrib[group_key], 3),
                            "cap": MAX_POSITIVE_TAG_GROUP_DELTA,
                            "reason": "duplicate_positive_pattern_group_capped"
                        }
                    effective_delta = capped_delta
                    cmp["effective_score_delta"] = round(effective_delta, 3)
                    if effective_delta != cmp["score_delta"]:
                        cmp["score_capped"] = True
                    else:
                        # Keep tag_group_key internal unless it is needed to explain capping.
                        cmp.pop("tag_group_key", None)
                else:
                    cmp.pop("tag_group_key", None)
                raw_score += effective_delta
                raw_conf += cmp["confidence"]
                if kind == "strong_alignment":
                    alignments.append(cmp)
                elif kind == "moderate_alignment":
                    moderate.append(cmp)
                elif kind == "risk":
                    risks.append(cmp)
                elif kind == "tension":
                    tensions.append(cmp)
                else:
                    unknowns.append(cmp)

        # Normalize into 0..1. 0.50 is neutral.
        normalized = max(0.0, min(1.0, PATTERN_SCORE_BASELINE + raw_score / PATTERN_SCORE_SCALE))
        confidence = max(0.0, min(1.0, raw_conf / max(comparisons, 1)))
        return {
            "score": round(normalized, 3),
            "confidence": round(confidence, 3),
            "strong_alignments": alignments,
            "moderate_alignments": moderate,
            "tensions": tensions,
            "risks": risks,
            "unknowns": unknowns,
            "comparisons": comparisons,
            "capped_positive_groups": list(capped_positive_groups.values()),
        }

    def _compare_pair(self, pa: Dict[str, Any], pb: Dict[str, Any], a: LoadedProfile, b: LoadedProfile) -> Optional[Dict[str, Any]]:
        tags_a = set(map(str.lower, pa.get("environment_profile", {}).get("tags") or []))
        tags_b = set(map(str.lower, pb.get("environment_profile", {}).get("tags") or []))
        if not tags_a or not tags_b:
            return None
        overlap = tags_a & tags_b
        opposed = self._opposition(tags_a, tags_b)
        overlap_ratio = len(overlap) / max(1, min(len(tags_a), len(tags_b)))
        ev = min(float(pa.get("evidential_weight", 0.5)), float(pb.get("evidential_weight", 0.5)))
        st = min(float(pa.get("claim_stability", pa.get("stability", 0.5))), float(pb.get("claim_stability", pb.get("stability", 0.5))))
        rel = (a.relationship_multiplier + b.relationship_multiplier) / 2.0
        # Per-pair confidence is evidence/stability only. Relationship depth is applied once
        # at the evaluation-confidence layer to avoid double-counting and saturation.
        confidence = max(0.0, min(1.0, ev * st))
        va, vb = pa.get("outcome_valence"), pb.get("outcome_valence")

        reason = "pattern_pair_compared"
        kind = "unknown"
        delta = 0.0
        description = "Pattern relationship is weak or unresolved."

        if va == "positive" and vb == "positive" and overlap:
            delta = overlap_ratio * ev * rel
            kind = "strong_alignment" if overlap_ratio >= 0.6 else "moderate_alignment"
            reason = "positive_positive_tag_overlap"
            description = f"Positive patterns overlap on {sorted(overlap)}."
        elif (va == "negative" and vb == "positive") or (va == "positive" and vb == "negative"):
            bad_overlap = overlap | opposed
            if bad_overlap:
                delta = -1.15 * max(len(bad_overlap) / max(1, min(len(tags_a), len(tags_b))), 0.5) * ev * rel
                kind = "risk"
                reason = "negative_pattern_activated_by_opposing_environment"
                description = f"A negative pattern is activated by opposing environment tags {sorted(bad_overlap)}."
        elif "mixed" in {va, vb}:
            if overlap or opposed:
                delta = -0.35 * max(overlap_ratio, 0.4) * ev * rel
                kind = "tension"
                reason = "mixed_valence_pattern_tension"
                description = f"Mixed-valence pattern creates uncertainty around {sorted(overlap or opposed)}."
        elif va == "negative" and vb == "negative" and overlap:
            delta = 0.15 * overlap_ratio * ev
            kind = "moderate_alignment"
            reason = "shared_negative_environment_awareness"
            description = f"Both profiles identify risks around {sorted(overlap)}."

        if delta == 0.0 and not overlap and not opposed:
            return None

        return {
            "kind": kind,
            "profile_a_pattern_id": pa.get("id"),
            "profile_b_pattern_id": pb.get("id"),
            "description": description,
            "overlap_tags": sorted(overlap),
            "opposed_tags": sorted(opposed),
            "tag_group_key": [va or "", vb or "", *sorted(tags_a), "::", *sorted(tags_b)],
            "score_delta": round(delta, 3),
            "confidence": round(confidence, 3),
            "trace": [TraceBuilder.make([pa.get("id", ""), pb.get("id", "")], ["pattern", "pattern"], reason, "patterns are primary predictive objects")],
        }

    def _opposition(self, a: set, b: set) -> set:
        opposed = set()
        for t in a:
            opposed |= NEGATION_TAGS.get(t, set()) & b
        for t in b:
            opposed |= NEGATION_TAGS.get(t, set()) & a
        return opposed


class DivergenceEngine:
    def collect(self, a: LoadedProfile, b: LoadedProfile, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any]) -> Dict[str, Any]:
        profile_divs = [self._format_profile_divergence(d, a) for d in a.divergences()] + [self._format_profile_divergence(d, b) for d in b.divergences()]
        inferred = []
        for item in pattern_result.get("risks", []) + pattern_result.get("tensions", []):
            inferred.append({
                "divergence_type": "pattern_environment_conflict",
                "status": "unresolved",
                "interpretation": item.get("description"),
                "salience": {"value": self._salience_from_severity(item), "purpose": a.purpose or b.purpose},
                "trace": item.get("trace", []),
            })
        for item in constraint_result.get("constraint_tensions", []) + constraint_result.get("unknown_constraints", []):
            inferred.append({
                "divergence_type": "constraint_pattern_conflict" if item.get("status") == "soft_tension" else "constraint_unknown",
                "status": "unresolved",
                "interpretation": item.get("text"),
                "salience": {"value": 0.72 if item.get("status") == "soft_tension" else 0.55, "purpose": a.purpose or b.purpose},
                "trace": item.get("trace", []),
            })
        return {"profile_divergences": profile_divs, "inferred_divergences": inferred}

    def _format_profile_divergence(self, d: Dict[str, Any], p: LoadedProfile) -> Dict[str, Any]:
        sal = d.get("salience")
        if isinstance(sal, dict):
            sal_value = sal.get("value", d.get("divergence_score", 0.5))
            sal_purpose = sal.get("purpose") or d.get("salience_context") or p.purpose
        elif sal is not None:
            sal_value = sal
            sal_purpose = d.get("salience_context") or p.purpose
        else:
            sal_value = d.get("divergence_score", 0.5)
            sal_purpose = d.get("salience_context") or p.purpose
        return {
            "divergence_id": d.get("id"),
            "owner": p.handle,
            "divergence_type": d.get("divergence_type"),
            "status": d.get("status"),
            "divergence_score": d.get("divergence_score"),
            "interpretation": d.get("interpretation"),
            "salience": {"value": sal_value, "purpose": sal_purpose},
            "trace": [TraceBuilder.make([d.get("id", "")], ["divergence"], "profile_declared_divergence", "divergences are question-generating first-class objects")],
        }

    def _salience_from_severity(self, item: Dict[str, Any]) -> float:
        return round(min(1.0, 0.55 + abs(float(item.get("score_delta", 0))) / 2.0), 3)


class QuestionGenerator:
    def generate(self, divergences: Dict[str, Any], constraint_result: Dict[str, Any], pattern_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        questions = []
        for d in divergences.get("profile_divergences", []) + divergences.get("inferred_divergences", []):
            sal = d.get("salience", {}).get("value") or d.get("divergence_score") or 0.5
            dtype = d.get("divergence_type")
            interp = d.get("interpretation") or "A meaningful divergence exists."
            q = self._template(dtype, interp)
            questions.append({"question": q, "question_type": self._question_type(dtype), "priority": round(float(sal), 3), "trace": d.get("trace", [])})
        for c in constraint_result.get("blocking_constraints", []):
            questions.append({
                "question": f"Can the blocking {c.get('domain')} constraint be changed, or should this exchange terminate?",
                "question_type": "constraint_question",
                "priority": 1.0,
                "trace": c.get("trace", []),
            })
        questions.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return questions[:8]

    def _question_type(self, dtype: Optional[str]) -> str:
        if dtype and "constraint" in dtype:
            return "constraint_question"
        if dtype and "self_perception" in dtype:
            return "self_perception_question"
        if dtype and "environment" in dtype:
            return "environment_question"
        return "clarifying_question"

    def _template(self, dtype: Optional[str], interp: str) -> str:
        if dtype == "self_perception_gap":
            return f"How should this self-perception gap be interpreted in this exchange: {interp}"
        if dtype == "pattern_environment_conflict":
            return f"How often will the environment activate this risk: {interp}"
        if dtype == "constraint_pattern_conflict":
            return f"Is this constraint/environment tension negotiable or structurally fixed: {interp}"
        if dtype == "constraint_unknown":
            return f"What missing information is needed to evaluate this constraint: {interp}"
        return f"What should be clarified about this divergence: {interp}"


class ClaimExplainer:
    def explain(self, a: LoadedProfile, b: LoadedProfile, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any]) -> Dict[str, Any]:
        involved_tags = set()
        for bucket in ["strong_alignments", "moderate_alignments", "tensions", "risks"]:
            for item in pattern_result.get(bucket, []):
                involved_tags |= set(item.get("overlap_tags") or [])
                involved_tags |= set(item.get("opposed_tags") or [])
        supporting, contrasting = [], []
        for p in [a, b]:
            for c in p.claims():
                claim_tags = set(map(str.lower, c.get("tags") or []))
                formatted = {
                    "claim_id": c.get("id"),
                    "owner": p.handle,
                    "text": c.get("text"),
                    "tags": sorted(claim_tags),
                    "trace": [TraceBuilder.make([c.get("id", "")], ["claim"], "claim_used_for_explanation_only", "claims are communicable assertions, not scoring inputs")],
                }
                if claim_tags & involved_tags:
                    supporting.append(formatted)
                elif len(contrasting) < 3:
                    contrasting.append(formatted)
        return {
            "supporting_claims": supporting[:8],
            "contrasting_claims": contrasting[:4],
            "note": "Claims were used only for explanation, not scoring or constraint override.",
        }


class CompatibilityEvaluator:
    def __init__(self, schema_dir: Optional[Path] = None) -> None:
        self.loader = ProfileLoader(schema_dir)
        self.guard = LifecycleGuard()
        self.constraints = ConstraintEvaluator()
        self.patterns = PatternComparator()
        self.divergences = DivergenceEngine()
        self.questions = QuestionGenerator()
        self.claims = ClaimExplainer()

    def evaluate_files(self, profile_a_path: Path, profile_b_path: Path) -> Dict[str, Any]:
        return self.evaluate(self.loader.load(profile_a_path), self.loader.load(profile_b_path))

    def evaluate(self, loaded_a: LoadedProfile, loaded_b: LoadedProfile) -> Dict[str, Any]:
        start = time.perf_counter()
        a = self.guard.apply(loaded_a)
        b = self.guard.apply(loaded_b)
        constraint_result = self.constraints.evaluate(a, b)

        if constraint_result["status"] == "blocked":
            pattern_result = {"score": None, "confidence": 0.0, "strong_alignments": [], "moderate_alignments": [], "tensions": [], "risks": [], "unknowns": [], "comparisons": 0}
            classification = "constraint_blocked"
            score = None
            confidence = self._blocked_confidence(constraint_result)
        else:
            pattern_result = self.patterns.compare(a, b)
            score = pattern_result["score"]
            confidence = self._confidence(pattern_result, constraint_result, a, b)
            classification = self._classify(score, pattern_result, constraint_result, confidence)
            if classification == "insufficient_data":
                # Baseline pattern score is a normalization artifact, not a
                # compatibility score, when no comparisons were possible.
                score = None

        divergence_result = self.divergences.collect(a, b, pattern_result, constraint_result)
        question_result = self.questions.generate(divergence_result, constraint_result, pattern_result)
        claim_explanation = self.claims.explain(a, b, pattern_result, constraint_result)
        duration = round(time.perf_counter() - start, 6)
        scope_warnings = self._scope_warnings(a, b)

        result = {
            "evaluation_type": "CompatibilityEvaluation",
            "protocol_version": PROTOCOL_VERSION,
            "metadata": {
                "engine": "engine_v02_3.py",
                "engine_version": "0.2.3-alpha",
                "evaluation_duration_seconds": duration,
                "objects_loaded": self._objects_loaded(a, b),
                "objects_scored": self._objects_scored(a, b, pattern_result, constraint_result),
                "filter_summary": {a.profile_id: a.filter_summary, b.profile_id: b.filter_summary},
                "scope_warnings": scope_warnings,
                "lifecycle_warnings": {a.profile_id: a.warnings, b.profile_id: b.warnings},
                "semantic_model_notes": ["NEGATION_TAGS is a provisional engine-local semantic opposition table and should be promoted to a documented ontology/taxonomy before independent conformance claims.", "Positive pattern contribution is capped by tag-group to reduce duplicate-pattern stuffing and low-evidence spam."],
            },
            "profile_a": self._profile_ref(a),
            "profile_b": self._profile_ref(b),
            "result": {
                "classification": classification,
                "constraint_status": constraint_result["status"],
                "compatibility_score": score,
                "confidence": round(confidence, 3) if confidence is not None else None,
                "evaluation_confidence": round(confidence if confidence is not None else self._evaluation_confidence(classification, pattern_result, constraint_result), 3),
                "confidence_basis": self._confidence_basis(classification, pattern_result, constraint_result),
            },
            "constraint_evaluation": constraint_result,
            "pattern_comparison": pattern_result,
            "divergences": divergence_result,
            "questions": question_result,
            "claim_based_explanation": claim_explanation,
            "recommendation": self._recommendation(classification, question_result),
            "summary": self._summary(a, b, classification, score, constraint_result, pattern_result),
        }
        return result

    def _classify(self, score: float, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any], confidence: Optional[float] = None) -> str:
        if int(pattern_result.get("comparisons") or 0) == 0:
            return "insufficient_data"
        risk_count = len(pattern_result.get("risks", []))
        tension_count = len(pattern_result.get("tensions", [])) + len(constraint_result.get("constraint_tensions", []))
        unknown_count = len(constraint_result.get("unknown_constraints", []))
        strong_count = len(pattern_result.get("strong_alignments", []))
        if ((score >= 0.68) or (strong_count >= 1 and score >= 0.66)) and risk_count == 0 and tension_count <= 1 and unknown_count == 0:
            if confidence is not None and confidence < MIN_GOOD_MATCH_CONFIDENCE:
                return "ambiguous_match"
            return "good_match"
        if score <= 0.43 or risk_count >= 2:
            return "bad_match"
        if score >= 0.62 and tension_count + risk_count >= 1:
            return "moderate_high_with_tensions"
        if strong_count >= 1 and tension_count + risk_count >= 1:
            return "moderate_high_with_tensions"
        return "ambiguous_match"

    def _confidence(self, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any], a: LoadedProfile, b: LoadedProfile) -> Optional[float]:
        if int(pattern_result.get("comparisons") or 0) == 0:
            # No compatibility confidence is available when there is no comparable
            # pattern signal. The output's evaluation_confidence/confidence_basis
            # explains that the engine is confident about signal absence, not about
            # compatibility.
            return None
        base = float(pattern_result.get("confidence") or 0.45)
        rel = (a.relationship_multiplier + b.relationship_multiplier) / 2.0
        unknown_penalty = 0.05 * len(constraint_result.get("unknown_constraints", []))
        scope_penalty = 0.03 * len(self._critical_scope_gaps(a, b))
        auth_penalty = 0.1 * sum(1 for p in [a, b] if p.entity_authorized is False)
        relationship_penalty = 0.08 * sum(1 for p in [a, b] if self._relationship_depth_warning_needed(p))
        return max(0.0, min(1.0, base * rel - unknown_penalty - scope_penalty - auth_penalty - relationship_penalty))

    def _blocked_confidence(self, constraint_result: Dict[str, Any]) -> float:
        # Confidence should reflect unique logical violations and epistemic source,
        # not duplicated constraint objects. Numeric floor/ceiling conflicts are
        # more certain than tag-inferred environment conflicts.
        unique: Dict[Tuple[Any, ...], float] = {}
        for c in constraint_result.get("blocking_constraints", []):
            ids = []
            reasons = []
            for tr in c.get("trace", []):
                ids.extend(tr.get("source_object_ids") or [])
                if tr.get("reason_code"):
                    reasons.append(str(tr.get("reason_code")))
            key = (c.get("domain"), tuple(sorted(set(ids))) or (c.get("constraint_id"),))
            unique[key] = max(unique.get(key, 0.0), self._block_confidence_for_constraint(c, reasons))
        if not unique:
            return 0.0
        strongest = max(unique.values())
        return min(0.97, strongest + 0.02 * max(0, len(unique) - 1))

    def _block_confidence_for_constraint(self, c: Dict[str, Any], reasons: Sequence[str]) -> float:
        domain = c.get("domain")
        ctype = c.get("constraint_type")
        reason_text = " ".join(reasons)
        if domain == "compensation":
            return 0.95
        if domain == "location" and "explicit" in reason_text:
            return 0.90
        if ctype == "environment_requirement" or domain in {"work_environment", "environment"}:
            return 0.78
        return 0.82

    def _evaluation_confidence(self, classification: str, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any]) -> float:
        if classification == "insufficient_data":
            return 0.95
        if classification == "constraint_blocked":
            return self._blocked_confidence(constraint_result)
        return float(pattern_result.get("confidence") or 0.45)

    def _confidence_basis(self, classification: str, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any]) -> str:
        if classification == "insufficient_data":
            return "compatibility confidence is null because no comparable pattern signal was present; evaluation_confidence reflects high confidence that the engine lacks sufficient data."
        if classification == "constraint_blocked":
            domains = sorted({str(c.get("domain")) for c in constraint_result.get("blocking_constraints", []) if c.get("domain")})
            return f"confidence reflects certainty of hard constraint block, adjusted by constraint type; blocking domains={domains}."
        return "confidence reflects pattern evidence/stability, relationship depth applied once, and penalties for unknown constraints, scope gaps, and authorization restrictions."

    def _objects_loaded(self, a: LoadedProfile, b: LoadedProfile) -> Dict[str, int]:
        return {
            "claims": len(a.claims()) + len(b.claims()),
            "patterns": len(a.patterns()) + len(b.patterns()),
            "constraints": len(a.constraints()) + len(b.constraints()),
            "divergences": len(a.divergences()) + len(b.divergences()),
        }

    def _objects_scored(self, a: LoadedProfile, b: LoadedProfile, pattern_result: Dict[str, Any], constraint_result: Dict[str, Any]) -> Dict[str, int]:
        return {
            "pattern_comparisons": int(pattern_result.get("comparisons") or 0),
            "constraints_evaluated": len(a.constraints()) + len(b.constraints()),
            "blocking_constraints": len(constraint_result.get("blocking_constraints", [])),
            "claims_scored": 0,
        }

    def _critical_scope_gaps(self, a: LoadedProfile, b: LoadedProfile) -> List[Dict[str, Any]]:
        gaps: List[Dict[str, Any]] = []
        broad_required = {"patterns", "constraints", "work_style"}
        for p in [a, b]:
            assessed = p.assessed_categories
            unassessed = p.unassessed_categories
            for category in sorted(CRITICAL_SCOPE_CATEGORIES):
                if category in unassessed:
                    gaps.append({"profile_id": p.profile_id, "category": category, "reason": "declared_unassessed"})
                elif category in broad_required and category not in assessed:
                    # Empty assessed_categories means the category was not assessed;
                    # do not let Python truthiness hide the most important Workspace
                    # case: document/profile generation with no scope coverage yet.
                    gaps.append({"profile_id": p.profile_id, "category": category, "reason": "not_declared_assessed"})
        return gaps

    def _scope_warnings(self, a: LoadedProfile, b: LoadedProfile) -> List[Dict[str, Any]]:
        warnings = []
        for gap in self._critical_scope_gaps(a, b):
            warnings.append({
                "warning_type": "critical_scope_gap",
                **gap,
                "message": "A critical category was not assessed; silence should be treated as unknown, not absence."
            })
        for p in [a, b]:
            if p.entity_authorized is False:
                warnings.append({
                    "warning_type": "entity_not_authorized",
                    "profile_id": p.profile_id,
                    "message": "Profile declares entity_authorized=false; disclosure/evaluation should be treated as restricted."
                })
            if self._relationship_depth_warning_needed(p):
                warnings.append({
                    "warning_type": "relationship_depth_evidence_mismatch",
                    "profile_id": p.profile_id,
                    "relationship_depth": p.relationship_depth,
                    "message": "Profile claims deep relationship depth without enough supporting observations/evidence; confidence should be treated cautiously."
                })
        return warnings

    def _relationship_depth_warning_needed(self, p: LoadedProfile) -> bool:
        if p.relationship_depth not in {"longitudinal", "hybrid"}:
            return False
        observation_count = len(p.raw.get("observations") or [])
        evidence_count = len(p.raw.get("evidence") or [])
        pattern_count = len(p.patterns())
        return observation_count + evidence_count == 0 and pattern_count <= 1

    def _profile_ref(self, p: LoadedProfile) -> Dict[str, Any]:
        return {"profile_id": p.profile_id, "entity_id": p.entity_id, "handle": p.handle, "relationship_depth": p.relationship_depth}

    def _recommendation(self, classification: str, questions: List[Dict[str, Any]]) -> str:
        if classification == "constraint_blocked":
            return "Strong constraint mismatch. Do not proceed unless the blocking constraint is explicitly renegotiated."
        if classification == "insufficient_data":
            return "Insufficient pattern signal to evaluate compatibility. Gather additional profile data before proceeding."
        if classification == "good_match":
            return "Proceed to human conversation; use the highest-priority question to confirm the main tension."
        if classification == "bad_match":
            return "Do not proceed without substantial environment or requirement changes."
        if classification == "moderate_high_with_tensions":
            return "Proceed cautiously with a focused conversation around the top tensions."
        return "Proceed only as an exploratory conversation; resolve the highest-priority questions first."

    def _summary(self, a: LoadedProfile, b: LoadedProfile, classification: str, score: Optional[float], constraints: Dict[str, Any], patterns: Dict[str, Any]) -> str:
        if classification == "constraint_blocked":
            return f"{a.handle} and {b.handle} are blocked before compatibility scoring because at least one hard constraint fails."
        if classification == "insufficient_data":
            return f"{a.handle} and {b.handle} could not be evaluated because no comparable pattern signal was present after constraints were evaluated."
        return f"{a.handle} and {b.handle} evaluated as {classification} based on pattern comparison after constraints were evaluated. Score={score}."


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate two CARP v0.2 profiles.")
    parser.add_argument("profile_a", type=Path)
    parser.add_argument("profile_b", type=Path)
    parser.add_argument("--schema-dir", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    evaluator = CompatibilityEvaluator(args.schema_dir)
    result = evaluator.evaluate_files(args.profile_a, args.profile_b)
    text = json.dumps(result, indent=2, sort_keys=False)
    if args.out:
        args.out.write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
