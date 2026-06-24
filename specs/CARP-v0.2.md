# Confidence-Aware Representation Protocol (CARP)
### Version 0.2 — Draft Specification

---

## Abstract

The Confidence-Aware Representation Protocol (CARP) defines a standardized method for AI agents to represent entities — including individuals, teams, and organizations — through structured, confidence-weighted, provenance-aware claims.

CARP establishes a foundational representation layer. It does not define compatibility scoring, matchmaking, negotiation, verification, or decision-making. Those operations may be built on top of CARP by conforming implementations.

> **The protocol is designed around epistemic transparency rather than certainty.**

---

## Status of This Document

This is a draft specification. It has not yet been submitted to any standards body. Feedback is welcome via the repository issue tracker.

**Version:** 0.1  
**Status:** Draft  
**Authors:** [TBD]  
**Repository:** [TBD]  
**License:** [TBD — recommended: CC BY 4.0 for the specification, MIT for reference implementations]

---

## 1. Core Principle

CARP does not attempt to determine whether a claim is true.

CARP communicates:

- What is being claimed
- How the claim was derived
- What evidence supports it
- How confident the originating agent is in that claim
- Whether conflicting observations exist

This distinction is foundational. A conforming implementation does not assert facts. It asserts confidence-weighted observations with explicit provenance.

---

## 2. Definitions

**Agent** — An AI system capable of generating, reading, and exchanging CARP-conforming representations on behalf of an entity it represents.

**Entity** — Any person, team, organization, or other subject that an agent represents. See Section 4 for entity types.

**Claim** — The atomic unit of the protocol. A single confidence-weighted, provenance-labeled statement about an entity. See Section 3.

**Observation** — The raw behavioral or contextual data from which claims are derived. Observations are the source material for claims but are not transmitted by this protocol. See Section 3.1.

**Profile** — A named, versioned collection of claims about a single entity. See Section 5.

**Divergence** — A first-class object representing a conflict between two claims about the same entity. See Section 6.

**Disclosure** — A controlled, purpose-bound, time-limited release of a subset of claims from one agent to another. See Section 7.

**Provenance** — The origin and derivation method of a claim. Every claim in CARP carries a provenance label.

**Confidence** — A float between 0.0 and 1.0 representing the originating agent's degree of certainty in a claim, based on available evidence.

---

## 3. The Claim — Atomic Unit

Everything in CARP is built from a single structure: the **Claim**.

```yaml
claim:
  id: string                    # unique identifier for this claim
  text: string                  # human-readable statement of the claim
  source: self_declared         # how this claim was derived (see 3.2)
         | agent_inferred
         | third_party
         | behaviorally_evident
  confidence: float             # 0.0 to 1.0
  evidence_count: integer       # number of observations supporting this claim
  evidence_summary: string      # human-readable description of the evidence basis
  generated_by: string          # identifier of the agent that generated this claim
  generated_at: timestamp       # ISO 8601
  expires_at: timestamp | null  # optional expiry for time-sensitive claims
```

### 3.1 The Observation Layer

Claims are abstractions derived from underlying observations. An observation is a discrete behavioral or contextual data point — a message sent, a decision made, a pattern repeated — from which an agent may derive one or more claims.

The structure of observations, and the process by which agents derive claims from them, is outside the scope of CARP v0.1. Conforming implementations should treat `evidence_count` as a reference to an underlying observation set. A future version of this specification may define the Observation object and the claim derivation process.

### 3.2 Provenance Labels

| Value | Meaning |
|---|---|
| `self_declared` | The entity stated this directly. Not independently verified. |
| `agent_inferred` | The agent derived this claim from observed patterns over time. |
| `third_party` | A separate agent or external source asserted this claim. |
| `behaviorally_evident` | The agent can cite specific, discrete instances as direct evidence. |

Provenance labels must not be omitted or approximated. A claim without a provenance label is not CARP-conforming.

### 3.3 Confidence

Confidence scores must reflect the agent's actual epistemic state based on evidence count and quality. Agents must not assign high confidence scores to claims with low evidence counts, nor must they artificially normalize scores to appear more certain.

A confidence score of `0.0` means the agent has no basis for the claim. A score of `1.0` means the agent considers the claim certain based on overwhelming, consistent evidence. Most real claims will fall between `0.4` and `0.9`.

---

## 4. Entity

A Profile describes a single entity. CARP does not restrict what constitutes a valid entity.

```yaml
entity:
  id: string          # unique identifier
  type: string        # free text — see note below
```

Common type values include `individual`, `team`, and `organization`. Implementations may define additional entity types. No type value is privileged or constrained by this specification.

This openness is intentional. The protocol is designed to represent any subject an agent may be asked to describe — a person, a department, a project, a community, or any future entity type not yet anticipated.

---

## 5. Profile

A Profile is a named, versioned collection of claims about a single entity.

```yaml
profile:
  protocol_version: "0.1"
  profile_id: string          # unique identifier for this profile
  entity: entity              # the subject of this profile
  generated_by: string        # identifier of the agent that generated this profile
  generated_at: timestamp     # ISO 8601
  claims: [claim]             # ordered list of claims
  divergences: [divergence]   # conflicts between claims, if any (see Section 6)
```

### 5.1 Profile Integrity

A Profile is not a curated highlight reel. A conforming agent must not selectively include only favorable claims while suppressing unfavorable ones it has derived about the same entity.

If an agent has derived both positive and negative claims about an entity with similar evidence counts and confidence levels, both must be included or neither should be included. Selective omission of negative signals is a conformance violation.

### 5.2 Profiles Are Generated, Not Stored

Profiles are generated on demand by agents and shared through the Disclosure operation. CARP does not define a profile storage or registry mechanism. Profiles are not assumed to be persistent artifacts.

---

## 6. Divergence

A Divergence is a first-class object representing a meaningful conflict between two claims about the same entity.

```yaml
divergence:
  id: string
  claim_a: claim_id             # typically self_declared
  claim_b: claim_id             # typically agent_inferred or behaviorally_evident
  divergence_score: float       # 0.0 to 1.0, magnitude of conflict
  status: unresolved            # see 6.1
         | acknowledged
         | transitional
         | aspirational
  interpretation: string        # human-readable explanation of the gap
```

### 6.1 Divergence Status

| Status | Meaning |
|---|---|
| `unresolved` | The conflict exists and has not been addressed by the entity. |
| `acknowledged` | The entity is aware of the divergence and has provided context. |
| `transitional` | The divergence is real but the entity is actively changing. |
| `aspirational` | The self-declared claim represents a goal, not a current reality. |

### 6.2 Divergences as Signal

Divergences are not failures of the protocol. They are among its most valuable outputs.

An entity that discloses divergences with status `acknowledged`, `transitional`, or `aspirational` is demonstrating a higher degree of epistemic honesty than one that surfaces only internally consistent claims. Receiving agents should treat disclosed divergences as a positive signal about the trustworthiness of the overall profile.

Example divergence:

```yaml
divergence:
  id: "div-001"
  claim_a: "cla-012"     # self_declared: "We empower teams to move fast"
  claim_b: "cla-047"     # agent_inferred: "87% of product decisions require VP approval"
  divergence_score: 0.79
  status: acknowledged
  interpretation: |
    The organization expresses a value of team autonomy but currently 
    operates with centralized decision-making. Leadership acknowledges 
    this gap and cites recent org growth as the cause.
```

---

## 7. Disclosure

A Disclosure is the controlled, purpose-bound, time-limited release of a subset of claims from one agent to another.

```yaml
disclosure:
  disclosure_id: string
  from_agent: string            # identifier of the disclosing agent
  to_agent: string              # identifier of the receiving agent
  purpose: string               # declared intent for this exchange
  scope:
    type: claim_list            # see 7.1
    value: [claim_id]
  minimum_confidence: float     # claims below this threshold are not released
  issued_at: timestamp
  expires_at: timestamp         # all disclosures must have an expiry
  revocable: boolean
```

### 7.1 Scope Types

In CARP v0.1, the only valid scope type is `claim_list` — an explicit list of claim IDs being released.

The scope field is designed for extension. Future versions of this specification may define additional scope types, including `view` (a named, reusable subset of claims) and `full_profile`. Implementations should treat unknown scope types as invalid rather than attempting to interpret them.

### 7.2 Disclosure Requirements

A conforming disclosure must:

- Declare a specific purpose. Generic or open-ended purpose declarations are not valid.
- Include an expiry timestamp. Disclosures without expiry are not conforming.
- Include all divergences that are directly relevant to the claims being disclosed. Disclosing claims while suppressing associated divergences is a conformance violation.
- Be revocable unless the disclosing agent explicitly sets `revocable: false` and the receiving agent acknowledges this.

### 7.3 Receiving Agent Obligations

A receiving agent must:

- Use disclosed claims only for the stated purpose.
- Not retain disclosed claims beyond the expiry timestamp.
- Not forward disclosed claims to a third agent without initiating a new Disclosure with the originating agent's consent.

---

## 8. Privacy Requirements

CARP is designed to enable honest representation without requiring access to private information.

### 8.1 What the Protocol Transmits

The protocol transmits **distilled understanding**, not raw data. An agent that has observed thousands of interactions with an entity should transmit claims derived from those interactions — not the interactions themselves.

For example:

- **Transmit:** `prefers written communication | agent_inferred | confidence: 0.89`
- **Do not transmit:** The specific messages from which this was inferred

### 8.2 Entity Control

Entities own their profiles. An agent generates a profile on behalf of an entity and with that entity's authorization. An agent must not generate or disclose a profile without the explicit consent of the entity it represents.

### 8.3 No Central Repository

CARP does not require or define a central profile registry. Profiles are generated on demand and shared peer-to-peer through the Disclosure operation. Implementations must not assume the existence of a central authority.

### 8.4 Right to Revocation

Entities have the right to revoke any active Disclosure at any time. Receiving agents must honor revocations promptly. Revocation does not retroactively invalidate decisions already made using disclosed claims within the stated purpose and prior to revocation.

---

## 9. Conformance

### 9.1 A Conforming CARP Agent Must Be Able To

1. Generate Claims with valid provenance labels and confidence scores supported by evidence counts
2. Assemble Claims into a Profile, including relevant Divergences
3. Identify and surface Divergences between conflicting claims about the same entity
4. Execute a Disclosure operation with explicit purpose binding, claim scoping, confidence filtering, and expiry
5. Respond to a provenance query: *"How was this claim derived?"*
6. Honor Disclosure expiry and revocation

### 9.2 A Conforming CARP Agent Must Not

- Generate claims without provenance labels
- Assign confidence scores not substantiated by evidence counts
- Release claims without an explicit Disclosure operation
- Suppress divergences when disclosing related claims
- Retain or use disclosed claims beyond their stated expiry or purpose
- Generate or disclose a profile without the entity's consent

---

## 10. What This Protocol Does Not Define

The following are explicitly outside the scope of CARP v0.1:

- Compatibility scoring or matching algorithms
- Negotiation between agents
- Verification of claims by third parties
- Search or discovery of profiles
- The internal format of observations from which claims are derived
- Any specific application domain (employment, consulting, investment, or otherwise)

These may be defined in future versions of this specification or in separate specifications built on top of CARP.

---

## 11. Governance

CARP is an open standard. No single entity controls it.

### 11.1 Authorship and Stewardship

The authors of CARP v0.1 commit to transferring governance to an independent body upon [milestone TBD]. Until that transfer, changes to the specification require public notice and a comment period of no less than 30 days.

### 11.2 Repository

The specification is maintained at [repository TBD] under [license TBD — recommended: CC BY 4.0].

Reference implementations are maintained at [repository TBD] under [license TBD — recommended: MIT].

### 11.3 Versioning

All CARP profiles and disclosures carry a `protocol_version` field. Version numbers follow semantic versioning. Breaking changes require a major version increment. Implementations must reject profiles with unsupported protocol versions rather than attempting to interpret them.

### 11.4 Extension Namespaces

Implementations may add custom fields to any CARP object under a namespaced key (e.g., `x-myorg-field`). Custom fields must not conflict with or override defined fields. Receiving agents must ignore unknown fields rather than treating them as errors.

---

## 12. Future Work

The following operations are anticipated in future versions of CARP or in separate specifications built on this foundation:

| Operation | Description |
|---|---|
| `VIEW` | A named, reusable subset of claims from a profile, enabling scoped disclosure without per-claim curation |
| `MATCH` | Structured comparison of claims across two profiles |
| `VERIFY` | Third-party attestation of a claim |
| `NEGOTIATE` | Iterative claim exchange between agents |
| `DISCOVER` | Search for profiles meeting specified claim criteria |
| `COLLABORATE` | Ongoing shared context between multiple agents |

---

## Appendix A — Minimal Conforming Profile Example

The following is the smallest valid CARP profile. It contains a single claim about a single entity.

```yaml
protocol_version: "0.1"
profile_id: "pro-0001"
entity:
  id: "ent-0001"
  type: "individual"
generated_by: "agent-0001"
generated_at: "2026-06-09T00:00:00Z"
claims:
  - id: "cla-0001"
    text: "Prefers asynchronous communication"
    source: agent_inferred
    confidence: 0.87
    evidence_count: 23
    evidence_summary: "Consistently initiates written communication over synchronous alternatives across observed interactions"
    generated_by: "agent-0001"
    generated_at: "2026-06-09T00:00:00Z"
    expires_at: null
divergences: []
```

---

## Appendix B — Minimal Conforming Disclosure Example

```yaml
disclosure_id: "dis-0001"
from_agent: "agent-0001"
to_agent: "agent-0002"
purpose: "Evaluate communication style compatibility for a collaborative project"
scope:
  type: claim_list
  value: ["cla-0001"]
minimum_confidence: 0.70
issued_at: "2026-06-09T00:00:00Z"
expires_at: "2026-07-09T00:00:00Z"
revocable: true
```

---

## Appendix C — Divergence Example

```yaml
divergence:
  id: "div-0001"
  claim_a: "cla-0012"
  claim_b: "cla-0047"
  divergence_score: 0.79
  status: acknowledged
  interpretation: |
    Self-declared value of team autonomy conflicts with observed 
    centralized decision-making. Entity acknowledges this gap.
```

---

*End of CARP v0.2 Draft Specification*
