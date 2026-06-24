# CARP v0.2 Ontology

## Status

Pre-specification draft.

This document defines the conceptual ontology of CARP v0.2. It does not define transport, authentication, authorization, exchange operations, discovery indexing, or negotiation mechanics.

Its purpose is narrower: define the fundamental representational objects that exist inside CARP.

CARP v0.1 treated the Claim as the primary object and built most representation around it. The v0.2 work shows that the Claim is necessary but insufficient. Several different kinds of knowledge were being compressed into Claims, producing ambiguity in extraction, disclosure, compatibility analysis, and human interpretation.

CARP v0.2 separates these representational types.

---

## 1. Design Principle

CARP v0.2 is built around one core idea:

> Representation is not a list of claims. Representation is a structured model of what is known, how it is known, how strongly it is supported, and where meaningful uncertainty remains.

The ontology must support long-term personal agents, short-lived document extractors, self-declared information, third-party information, outcome patterns, hard constraints, contradictions, divergences, and privacy-preserving disclosure.

The ontology must not assume that all knowledge enters the system in the same way.

---

## 2. First-Class Objects

CARP v0.2 defines seven first-class objects:

1. Evidence
2. Observation
3. Pattern
4. Claim
5. Constraint
6. Divergence
7. Profile

These are not a mandatory derivation chain.

A common flow may look like:

```text
Evidence → Observation → Pattern → Claim
```

But CARP v0.2 does not require that flow. Some Claims are self-declared and have no underlying Observations. Some Constraints are boundary conditions that do not require evidence. Some Patterns are the primary objects used by compatibility engines and may not need to be reduced into Claims. Some Divergences occur between Claims and Patterns rather than between Claims alone.

The model is therefore a type system with explicit grounding relationships, not a rigid hierarchy.

---

## 3. Evidence

### Definition

Evidence is a source artifact or record that may ground representational objects.

Evidence is not a conclusion. Evidence does not interpret itself. Evidence only establishes that a source exists and may be referenced.

### Examples

- resume
- performance review
- manager feedback
- interview transcript
- calendar history
- email thread
- project postmortem
- system log
- attestation
- behavioral record
- long-term agent memory excerpt

### Core fields

```yaml
evidence:
  id: string
  evidence_type: document | event | attestation | system_record | memory_record
  subtype: string
  authored_by: self | third_party | collaborative | system | agent
  authored_at: timestamp | null
  acquired_at: timestamp
  extracted_at: timestamp | null
  extraction_confidence: float | null
  temporal_scope:
    valid_from: timestamp | null
    valid_to: timestamp | null
  content_ref: string | null
  privacy_tier: public | disclosable | guarded | private
```

---

## 4. Observation

### Definition

An Observation is a discrete, timestamped data point about an entity or its environment.

Observations describe what happened. They do not generalize beyond the event or fact observed.

### Examples

- “Completed onboarding redesign without direct supervision.”
- “Attended 27 meetings during a 5-day period.”
- “Declined a management-track promotion.”
- “Stayed 42 months in an early-stage role.”
- “Submitted written decision memo before design review.”
- “Reported compensation floor of $180,000.”

### Core fields

```yaml
observation:
  id: string
  entity_id: string
  observed_at: timestamp
  observed_by: string
  observation_type: behavioral | stated | outcome | environmental | interaction
  description: string
  evidence_refs: [evidence_id]
  tags: [string]
  privacy_tier: public | disclosable | guarded | private
```

---

## 5. Pattern

### Definition

A Pattern is a generalization across observations. Patterns describe recurring tendencies, especially relationships between an entity, an environment, and an outcome. Patterns are predictive.

### Examples

- “Produces strongest outcomes in high-autonomy environments.”
- “Engagement declines in meeting-heavy environments.”
- “Performs well in analytical ambiguity but poorly in organizational ambiguity.”
- “Historically remains longer in early-stage organizations.”
- “Designers who thrive in this organization show autonomy, systems thinking, and ambiguity tolerance.”

### Core fields

```yaml
pattern:
  id: string
  entity_id: string
  pattern_type: outcome | behavioral | relational
  environment_profile:
    tags: [string]
    description: string
  outcome_valence: positive | negative | neutral | mixed
  outcome_description: string
  evidential_weight: float
  stability: float
  evidence_count: integer
  observation_refs: [observation_id]
  evidence_refs: [evidence_id]
  generated_by: string
  generated_at: timestamp
  privacy_tier: public | disclosable | guarded | private
```

---

## 6. Claim

### Definition

A Claim is a communicable assertion about an entity. Claims may be grounded in self-declaration, Observations, Patterns, Evidence, or third-party statements. Claims are not necessarily true. They are assertions with epistemic metadata.

### Examples

- “Prefers written communication.”
- “Skilled in design systems.”
- “Values ownership.”
- “Has four years of buy-side experience.”
- “Self-describes as collaborative.”
- “Seeks principal-level responsibilities.”

### Core fields

```yaml
claim:
  id: string
  entity_id: string
  text: string
  epistemic_origin: entity_stated | agent_observed | third_party | system_inferred
  derivation_method: direct | pattern_based | inference | extraction
  grounding:
    type: entity_statement | observation_refs | pattern_ref | evidence_refs | third_party_statement
    refs: [id]
  evidential_weight: float
  claim_stability: float
  evidence_count: integer
  evidence_summary: string
  claim_scope:
    temporal_range:
      valid_from: timestamp | null
      valid_to: timestamp | null
    environmental_context: string | null
    domain: string | null
    baseline: string | null
  generated_by: string
  generated_at: timestamp
  expires_at: timestamp | null
  privacy_tier: public | disclosable | guarded | private
  tags: [string]
```

### Note on domain-dependent claims

Some claims are too broad to be useful. For example, “operates well with ambiguity” may be true for analytical ambiguity and false for organizational ambiguity. CARP implementations should decompose domain-dependent claims into narrower claims when possible.

---

## 7. Constraint

### Definition

A Constraint is a boundary condition that determines whether an exchange, opportunity, or relationship remains viable. Constraints are not beliefs. They are not weighted signals. They are evaluated.

### Examples

- “Minimum compensation: $180,000.”
- “Must be remote.”
- “Requires security clearance.”
- “Will not relocate.”
- “Requires collaborative environment.”
- “Cannot accept role with more than 25% travel.”

### Core fields

```yaml
constraint:
  id: string
  entity_id: string
  text: string
  constraint_type: floor | ceiling | requirement | exclusion | preference | environment_requirement
  domain: compensation | location | role_type | environment | legal | availability | other
  value: string | number | null
  comparator: equals | not_equals | greater_than_or_equal | less_than_or_equal | includes | excludes | null
  firmness: hard | soft
  grounding:
    type: entity_statement | outcome_derived | pattern_ref | evidence_refs
    refs: [id]
  effective_from: timestamp | null
  expires_at: timestamp | null
  generated_by: string
  generated_at: timestamp
  privacy_tier: public | disclosable | guarded | private
```

### Environment requirement

The `environment_requirement` type exists for cases where the absence of a required environment condition activates a severe negative Pattern.

---

## 8. Divergence

### Definition

A Divergence is a meaningful conflict between representational objects. Divergences are not errors. They are first-class signals.

### Examples

- Self-description conflicts with observed behavior.
- Public company narrative conflicts with internal operating pattern.
- A claim from an old document conflicts with current behavior.
- Two self-authored documents make incompatible claims.
- A Claim conflicts with a Pattern.

### Core fields

```yaml
divergence:
  id: string
  divergence_type: self_perception_gap | narrative_reality_gap | temporal_drift | document_conflict | cross_agent_conflict
  object_a:
    object_type: claim | constraint | pattern | observation
    object_id: string
  object_b:
    object_type: claim | constraint | pattern | observation
    object_id: string
  divergence_score: float
  status: unresolved | acknowledged | transitional | aspirational | resolved
  interpretation: string
  salience:
    value: float | null
    purpose: string | null
    set_at: disclosure_time | profile_generation | null
  generated_by: string
  generated_at: timestamp
```

### Note on salience

Divergence salience is purpose-dependent. The same Divergence may be critical in one exchange and irrelevant in another. Therefore salience should not be treated as an intrinsic property of the Divergence. It should be attached relative to a disclosure purpose or compatibility evaluation.

---

## 9. Profile

### Definition

A Profile is a scoped, agent-generated representation of an entity. It contains selected representational objects and declares the agent’s relationship to the entity.

### Core fields

```yaml
profile:
  protocol_version: "carp-0.2"
  profile_id: string
  entity:
    id: string
    type: individual | team | organization | project | other
  generated_by: string
  generated_at: timestamp
  agent_relationship:
    relationship_depth: longitudinal | transactional | document_based | hybrid
    relationship_duration: string | null
    primary_observation_modes: [string]
    relationship_description: string | null
  profile_scope:
    purpose: string | null
    assessed_categories: [string]
    unassessed_categories: [string]
    disclosure_scope: full | partial | discovery | exchange | private
  claims: [claim]
  patterns: [pattern]
  constraints: [constraint]
  divergences: [divergence]
  exchange_protocol:
    constraint_first: boolean
    constraint_failed_behavior: terminate | continue_academic
```

---

## 10. Discovery Signal

Discovery Signals are not CARP ontology objects.

A Discovery Signal is a compiled projection derived from Profile contents for a specific discovery purpose. It may be generated from Patterns, Claims, Constraints, and Profile context, but it should not be treated as underlying knowledge.

Discovery Signals exist to answer:

> Is there enough coarse compatibility to justify a permissioned exchange?

They do not answer:

> Are these entities compatible?

---

## 11. Object Relationships

CARP v0.2 uses grounding relationships instead of strict hierarchy.

Examples:

```text
Evidence → Observation
Evidence → Claim
Observation → Pattern
Pattern → Claim
Pattern → Constraint
Claim ↔ Pattern Divergence
Claim ↔ Claim Divergence
Constraint → Exchange Viability
Profile → Disclosure
```

Objects must be traceable to their grounding where applicable. When grounding is absent, the object must state why.

---

## 12. Open Questions

1. Which objects may be transmitted directly in a Disclosure?
2. Are Patterns too sensitive to disclose by default?
3. How should cross-agent Divergences be represented?
4. Should salience live on Divergence, Exchange, or CompatibilityResult?
5. How should Discovery Signals be generated and authorized?
6. Should EnvironmentRequirement remain a Constraint type or become a Pattern severity field?
7. How should confidence calibration work across agents?
8. How should object histories and revisions be represented?

---

## 13. Summary

CARP v0.2 expands representation from a Claim-centered model to a multi-object ontology.

The central representational shift is from a claim list to a grounded model of evidence, observations, patterns, claims, constraints, and divergences.

CARP v0.2 does not eliminate uncertainty. It makes uncertainty representable.
