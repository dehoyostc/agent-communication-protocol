# CARP v0.2 Open Questions

## Status

Working list.

This document captures unresolved design questions surfaced during CARP prototype work. These questions should remain explicit until resolved by further design, stress testing, or implementation.

---

## 1. Pattern Disclosure Authorization

Patterns may be more sensitive than Claims.

A Claim might say: performs best in autonomous environments.

A Pattern might reveal: negative outcomes occur in high-oversight environments, especially when public critique and meeting density exceed certain thresholds.

Open questions:

- Are Patterns disclosable by default?
- Should Patterns require stronger authorization than Claims?
- Should agents disclose Pattern summaries rather than Pattern objects?
- Can Patterns be used internally for compatibility while disclosing only Claims?

---

## 2. Discovery Signal Generation

Discovery Signals are currently treated as derived projections rather than ontology objects.

Open questions:

- Are Discovery Signals generated from Patterns, Claims, Constraints, or all Profile objects?
- Who authorizes a Discovery Signal?
- Are Discovery Signals public, semi-public, peer-to-peer, or purpose-bound?
- Can Discovery Signals be revoked?
- Do Discovery Signals expire?
- Should Discovery Signal generation rules be standardized?

Current working assumption:

> Discovery Signals are lossy, purpose-bound projections that exist to justify permissioned exchange, not to establish compatibility.

---

## 3. Environment Requirements

The Marcus stress test revealed the need for environment requirements.

Open questions:

- Should `environment_requirement` be a Constraint type?
- Or should it be Pattern severity metadata?
- How severe must a negative Pattern be before it becomes a Constraint?
- Who decides whether a Pattern rises to Constraint severity?
- Can an environment requirement be inferred without entity confirmation?

---

## 4. Divergence Salience

Priya surfaced multiple mid-range Divergences. The model could represent them, but did not know which mattered most for the exchange.

Open questions:

- Does salience belong on Divergence?
- Does salience belong on Disclosure?
- Does salience belong on Compatibility Evaluation?
- Should salience be set by the disclosing agent, receiving agent, or exchange engine?
- Is salience always purpose-relative?

Current working assumption:

> Salience is purpose-relative and should not be treated as an intrinsic property of a Divergence.

---

## 5. Cross-Agent Divergence

CARP v0.2 currently focuses on divergences within a single Profile. But agents may disagree about the same entity.

Open questions:

- How should cross-agent divergences be represented?
- Does this require a new object type?
- Who owns the divergence?
- Can a receiving agent create a Divergence about a disclosed Profile?
- How are disagreements reconciled or preserved?

---

## 6. Confidence Calibration Across Agents

A score of 0.87 from one agent may not mean the same thing as 0.87 from another.

Open questions:

- Should CARP standardize confidence calibration?
- Should confidence remain agent-relative?
- Should agents disclose calibration metadata?
- Should receiving agents normalize confidence scores?
- Can confidence be compared across agents at all?

Current working assumption:

> Confidence scores should be treated as agent-relative unless calibration standards are defined.

---

## 7. Claim Stability

CARP v0.2 separates evidential weight from claim stability.

Open questions:

- How should stability be estimated?
- Does stability require historical evidence?
- Can self-declared Claims have high stability?
- Should stability decay automatically over time?
- Does stability belong on Claims, Patterns, or both?

---

## 8. Mixed-Valence Patterns

Priya revealed Patterns that are genuinely mixed.

Open questions:

- Should mixed Patterns include conditioning variables?
- Should mixed Patterns be decomposed into multiple narrower Patterns?
- When does decomposition become required?
- Does CARP v0.2 need Pattern subtypes?

---

## 9. Profile Scope and Ambiguous Silence

If a Profile contains no management-related Claims, what does that mean?

Possibilities:

- management was assessed and no signal was found
- management was not assessed
- management is known but withheld
- management is outside the disclosure scope

Open questions:

- How detailed must `assessed_categories` be?
- Should profiles distinguish unassessed from withheld?
- Should withheld categories be visible to receiving agents?
- Can silence itself be a protocol signal?

Current working assumption:

> Profiles must distinguish between unassessed categories and withheld categories.

---

## 10. Evidence Disclosure

Evidence objects may expose sensitive underlying documents.

Open questions:

- Should Evidence ever be disclosed?
- Should only Evidence metadata be disclosed?
- Should receiving agents be able to request Evidence?
- How does entity consent apply to Evidence created by third parties?
- Can Evidence be redacted while preserving traceability?

---

## 11. Observation Privacy

Observations are the raw material of CARP but are usually private.

Open questions:

- Are Observations ever transmitted?
- Can Observations be summarized safely?
- Can a receiving agent audit a Claim without seeing Observations?
- Should Observations have privacy tiers?
- How are Observation counts verified?

Current working assumption:

> Observations should remain private by default. Claims and Patterns transmit distilled understanding rather than raw context.

---

## 12. Constraint Negotiation

Constraints may be hard or soft.

Open questions:

- How does a soft Constraint participate in negotiation?
- Should Constraints include negotiation anchors?
- Should hard Constraints ever be challengeable?
- What happens if a Constraint changes during exchange?
- Does negotiation belong entirely outside CARP?

---

## 13. Object Revision History

CARP objects may change over time.

Open questions:

- Should revision history be required?
- Should each revision create a new object ID?
- How are expired Claims retained?
- Can receiving agents ask what changed between Profiles?
- How does revision interact with disclosure expiry?

---

## 14. Workspace vs Longitudinal Agent Profiles

A document-based Workspace and a long-term personal agent produce epistemically different Profiles.

Open questions:

- Should Profile schemas differ by agent relationship?
- Should document-extracted profiles carry warnings?
- How should receiving agents weight document-based Profiles?
- Can Workspace-generated Claims be upgraded after longitudinal observation?
- Should agent relationship affect conformance rules?

---

## 15. Discovery vs Exchange Boundary

Discovery uses coarse public or semi-public signals. Exchange uses permissioned information.

Open questions:

- What exactly crosses the boundary between Discovery and Exchange?
- Can Discovery Signals include Constraints?
- Should Discovery reveal why a pair surfaced?
- How lossy should Discovery be?
- How many false positives are acceptable?

Current working assumption:

> Discovery should optimize for not missing plausible compatibility while leaving final evaluation to Exchange.

---

## 16. Spec Boundary

CARP defines both the representation layer (L4) and the full protocol stack. Open boundary questions between the representation layer and the exchange/negotiation layers (L5–6) are documented below.

Open questions:

- Which lifecycle rules belong in the CARP representation spec vs. the CARP exchange spec?
- Does Disclosure belong in the CARP representation spec or the exchange layer spec?
- Does Constraint-first ordering belong in CARP Profile metadata or the exchange layer spec?
- Does Discovery Signal generation belong to the exchange/negotiation layers (L5–6), not the representation layer?
- Where does Negotiation begin?

---

## 17. Priority Questions Before CARP v0.2 Spec

Before writing a conformance specification, the project should resolve or explicitly defer:

1. Are Patterns transmittable?
2. Is `environment_requirement` a Constraint type?
3. Where does Divergence salience live?
4. Is Discovery Signal part of the exchange layer only, not the representation layer?
5. How should Profiles distinguish unassessed vs withheld?
6. What minimum lifecycle metadata is required?
7. How should confidence calibration be framed?

These questions do not block continued prototyping, but they should be resolved before calling CARP v0.2 a formal specification.
