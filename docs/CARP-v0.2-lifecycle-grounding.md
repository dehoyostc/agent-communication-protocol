# CARP v0.2 Object Lifecycle and Grounding Model

## Status

Draft design document.

This document defines how CARP objects come into existence, how they are grounded, how they change, and how they participate in disclosure.

CARP does not only define object types. It also needs to define the lifecycle of representational knowledge.

---

## 1. Why Lifecycle Matters

CARP represents living entities: people, teams, organizations, projects, and relationships. These change over time.

A representation that was accurate six months ago may now be stale. A self-declared preference may be revised. A Pattern may strengthen or weaken. A Divergence may be resolved. A Constraint may expire.

Without lifecycle rules, CARP risks turning living models into static profiles.

---

## 2. Core Lifecycle States

Every CARP object may pass through some or all of the following states:

```text
Created
Grounded
Reviewed
Approved
Disclosed
Expired
Revoked
Revised
Archived
```

Not every object uses every state.

---

## 3. Created

An object is created when an agent generates it or an entity declares it. Creation does not automatically make an object valid for disclosure.

Examples:

- Workspace extracts a Claim from a document.
- Personal agent identifies a Pattern from observations.
- Entity states a hard Constraint.
- Agent detects a Divergence.

---

## 4. Grounded

An object is grounded when it declares what supports it. Grounding may include Evidence references, Observation references, Pattern references, entity statements, third-party statements, or system records.

Grounding may be absent only when explicitly declared.

Grounding is not the same as verification.

---

## 5. Reviewed

An object is reviewed when the represented entity or an authorized agent inspects it for accuracy, sensitivity, and disclosure suitability.

Review is especially important for document-extracted Claims, inferred Patterns, sensitive Constraints, Divergences, and guarded disclosures.

Review does not require agreement. An entity may acknowledge a Divergence without resolving it.

---

## 6. Approved

An object is approved when it is accepted into a Profile or authorized for a specific disclosure scope.

Approval may be internal only, disclosable, guarded, private, or purpose-specific.

Approval should not be assumed globally. An object approved for one purpose may remain prohibited for another.

---

## 7. Disclosed

An object is disclosed when it is transmitted, summarized, or referenced to another agent under an explicit purpose.

Disclosure may include:

- full object
- redacted object
- guarded summary
- object existence only
- refusal reason without content

Example:

```text
Full private Pattern:
Negative outcomes in high-meeting environments due to anxiety triggers and prior public conflict.

Guarded disclosure:
Performance and engagement decline in high-meeting, performative environments.

Withheld:
health context, named individuals, specific incidents.
```

---

## 8. Expired

An object expires when its validity window ends. Expiration does not mean the object never existed. It means the object should no longer be used as current unless renewed or re-evaluated.

Expiration may apply to Claims, Constraints, Evidence, Patterns, Disclosures, and Profiles.

---

## 9. Revoked

Revocation is an explicit withdrawal of authorization. Revocation may apply to a disclosure, an object’s disclosability, an agent’s authority to represent an object, or a Profile scope.

Revocation does not erase history. It limits future authorized use.

---

## 10. Revised

An object is revised when its contents or metadata change. Revision should create a new version rather than silently overwrite the old one.

Examples:

- Claim stability decreases.
- Pattern evidential weight increases.
- Constraint value changes.
- Divergence status changes from unresolved to acknowledged.

Recommended fields:

```yaml
version: integer
supersedes: object_id | null
revision_reason: string
revised_at: timestamp
```

---

## 11. Archived

An object is archived when it is retained for audit or historical context but should not participate in current compatibility reasoning.

Archived objects may still matter for longitudinal analysis, temporal drift, audit trails, and historical reconstruction.

---

# 12. Grounding Model

CARP v0.2 uses explicit grounding relationships. Each object should be able to answer:

> Why does this object exist?

Grounding types:

```yaml
grounding_type:
  - entity_statement
  - evidence_refs
  - observation_refs
  - pattern_ref
  - third_party_statement
  - system_record
  - inferred_relationship
```

---

## 13. Object-Specific Lifecycle Notes

### Evidence

Evidence may be created, acquired, extracted, restricted, revoked, or archived. Evidence may be too sensitive to disclose even when derived Claims are disclosable.

### Observation

Observations are usually private. They may be referenced but not transmitted. Observation histories may support Patterns without exposing raw behavioral data.

### Pattern

Patterns may strengthen, weaken, split, or decay. Patterns may require re-evaluation when new Observations contradict them. Patterns may be more sensitive than Claims because they reveal predictive behavioral structure.

### Claim

Claims may be revised, expired, contradicted, or superseded. Claims are usually easier to disclose than underlying Observations.

### Constraint

Constraints may change, but not because evidence changes in the same way Claims do. A changed Constraint reflects a changed boundary condition or negotiation state.

### Divergence

Divergences may be unresolved, acknowledged, transitional, aspirational, or resolved. A resolved Divergence should not be deleted. It should be updated.

### Profile

Profiles are generated for a scope and purpose. Profiles should not be assumed permanent. Profiles may be regenerated from current objects at any time.

---

# 14. Disclosure Lifecycle

A Disclosure is not the same as an object. A Disclosure is an event or authorization record involving objects.

Recommended disclosure lifecycle:

```text
Requested
Evaluated
Authorized
Partially Authorized
Refused
Disclosed
Expired
Revoked
Audited
```

The ontology does not define full exchange mechanics, but CARP objects must carry enough lifecycle metadata for exchange systems to honor disclosure rules.

---

# 15. Key Principle

CARP object lifecycle exists to prevent stale, overconfident, or unauthorized representations from being treated as current truth.

The model should make it structurally easy to ask:

- What is this?
- Where did it come from?
- Who generated it?
- What grounds it?
- How current is it?
- Can it be disclosed?
- Has it changed?
- Has it expired?
- Has disclosure been revoked?

If a CARP object cannot answer those questions, the representation is incomplete.
