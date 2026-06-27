# CARP v0.2 Rationale

## Status

Draft rationale.

This document explains why CARP v0.2 differs from CARP v0.1. It is a historical and conceptual design record, not a formal specification.

---

## 1. Why v0.1 Needed Revision

CARP v0.1 established the essential commitments: representation over identity, confidence over certainty, provenance-aware claims, divergence as signal, disclosure over collection, and entity ownership.

Those commitments remain intact.

However, v0.1 compressed too many different kinds of information into the Claim object. During simulation and prototype work, the Claim became responsible for representing traits, preferences, constraints, outcome patterns, document-extracted statements, self-perceptions, environmental requirements, compensation floors, and divergences.

This overloaded the Claim type and made downstream reasoning ambiguous. CARP v0.2 keeps the philosophy of v0.1 but corrects the object model.

---

## 2. Why Constraints Became First-Class Objects

The strongest evidence for separating Constraints came from the River ↔ Arclight false-positive scenario.

Discovery surfaced River and Arclight as a strong potential match because their coarse Discovery Signals overlapped. During exchange, River’s compensation floor exceeded Arclight’s compensation ceiling.

This was not a weak compatibility signal. It was a hard boundary.

In v0.1, compensation was modeled as a Claim. That allowed the system to treat compensation incompatibility as one tension among many, which produced a misleading output: strong match, but compensation may be challenging.

The correct output is: hard Constraint violation. Exchange blocked or disqualified.

This is why Constraints became first-class objects. Constraints are evaluated before Claims. They are not weighed the same way Claims are.

---

## 3. Why Environment Requirements Matter

The Marcus scenario revealed a second Constraint category.

Marcus did not merely prefer collaborative environments. His negative Pattern showed that isolated, low-collaboration environments produced disengagement and underperformance.

This is different from a soft preference. It is an environment requirement.

The broader rationale is:

> Some environmental conditions are not optimization factors. They are viability conditions.

---

## 4. Why Patterns Became First-Class Objects

Early CARP simulations matched traits. That approach was too shallow.

The more successful simulations reasoned over outcome patterns:

```text
entity + environment → outcome
person + operating mode → performance
organization + employee profile → retention
team + communication style → collaboration quality
```

This proved more predictive than static trait matching.

Trait: autonomous.

Pattern: produces strongest outcomes in high-autonomy, low-oversight environments where ownership is real.

The Pattern is more useful because it is relational and predictive. CARP v0.2 therefore introduces Pattern as a first-class object.

---

## 5. Why Claims Remain Necessary

Although Patterns are more predictive, Claims remain necessary. Claims are communicable assertions. They are often the unit agents exchange, summarize, review, and disclose.

A Pattern may ground a Claim, but a Claim does not always require a Pattern.

Examples:

- “Has four years of buy-side experience.”
- “Self-describes as collaborative.”
- “Prefers remote work.”
- “Has built three design systems.”

Some are direct statements. Some are historical facts. Some are skill claims. They do not all require a Pattern.

This is why CARP v0.2 uses grounding relationships rather than a strict Evidence → Observation → Pattern → Claim hierarchy.

---

## 6. Why Evidence Became Explicit

The CARP Workspace introduced document-derived representation.

This created a new epistemic situation. An agent may be highly confident that it extracted a statement correctly from a document while remaining uncertain that the statement reflects reality.

A resume may say: led redesign of onboarding flow. The extraction may be accurate, but the truth of the claim remains uncertain unless supported by other evidence.

CARP v0.1 had no clean way to separate extraction confidence, claim confidence, document authorship, temporal scope, and third-party support.

Evidence objects solve this by making the source artifact explicit without turning document types into provenance labels.

---

## 7. Why Confidence Was Split

CARP v0.1 used a single confidence score. Prototype work showed that a single number collapses multiple questions.

Two of the most important are:

1. How well supported is this object right now?
2. How likely is it to remain true over time?

These are not the same. A compensation floor may have high evidential weight because the entity stated it directly, but lower stability because financial circumstances change. A long-observed work pattern may have slightly lower evidential weight than a direct statement but much higher stability.

CARP v0.2 therefore separates evidential support from stability.

---

## 8. Why Agent Relationship Was Added

CARP v0.1 implicitly assumed an agent that deeply knew the entity. That matched the original Jerry vision.

The Workspace introduced a different kind of agent: one that may know the entity only through a document.

These situations are epistemically different. A Profile generated by a two-year personal agent and a Profile generated by a thirty-second document extractor should not be interpreted the same way, even if they contain superficially similar Claims.

Agent Relationship describes how long the agent has represented the entity, what kind of knowledge the agent has, what observation modes were available, and whether the profile is longitudinal, transactional, document-based, or hybrid.

This context belongs at the Profile level because it affects interpretation of every object in the Profile.

---

## 9. Why Divergence Was Expanded

Divergences were one of the strongest parts of CARP v0.1. Prototype work made them even more important.

The most valuable human questions often came from Divergences.

Examples:

- “You describe yourself as collaborative, but your strongest outcomes occur independently. What does collaboration mean to you?”
- “The organization describes itself as low-ego, but the role includes high-visibility board presentations. How should that be interpreted?”
- “You claim to handle ambiguity well, but the data suggests this depends on the type of ambiguity.”

These are not errors. They are high-value signals. CARP v0.2 therefore types Divergences and allows Divergences between different object types, including Claim ↔ Pattern.

---

## 10. Why Salience Is Still Unsettled

The Priya scenario surfaced multiple mid-range Divergences. Each was real. None was obviously disqualifying.

The question became: which Divergence matters most for this exchange?

This is not intrinsic to the Divergence. It depends on purpose. The same Divergence may be critical in one exchange and irrelevant in another.

CARP v0.2 therefore treats salience as purpose-relative and currently unresolved. Possible locations include Divergence, Disclosure, Compatibility Evaluation, or Human Question generation.

---

## 11. Why Discovery Signals Are Not Ontology Objects

Discovery Signals emerged during the Discovery prototype. They are intentionally lossy projections used to surface possible matches without exposing private context.

A Discovery Signal may be generated from Patterns, Claims, Constraints, and Profile context. But it is not itself underlying knowledge. It is a compiled representation for a specific purpose.

If Discovery Signals are treated as Profile objects, they risk becoming another form of public profile. That would undermine CARP’s privacy-preserving architecture.

CARP v0.2 therefore treats Discovery Signals as derived artifacts outside the core ontology.

---

## 12. What the False Positive Proved

The River ↔ Arclight false positive was one of the most important tests.

Discovery said: strong possible match. Exchange said: disqualified.

This is not a failure. It is correct behavior. Discovery is supposed to be lossy. Exchange exists to resolve what Discovery cannot safely know.

This test proved the need for distinct layers:

```text
Discovery Signal
→ Potential Match
→ Permissioned Exchange
→ Constraint Check
→ Compatibility Analysis
→ Human Questions
```

It also proved that Constraints must be processed before Claims.

---

## 13. What the Workspace Proved

The Workspace tested whether CARP can be generated from unstructured source material. It revealed that the representation problem begins before exchange.

The hard question is not only what should an agent disclose, but how did the agent come to believe this in the first place?

The Workspace made traceability essential. Every extracted Claim needs a visible connection to its source passage or grounding. This pushed CARP from a claim schema toward a richer object model.

---

## 14. What the Ontology Stress Test Proved

The Sam, Marcus, Priya, and River stress test showed that the v0.2 ontology mostly holds across strong match, bad match, ambiguous match, and false positive.

It also revealed three necessary additions or unresolved issues:

1. Environment requirements that rise to Constraint severity
2. Divergence salience relative to exchange purpose
3. Constraint-first exchange ordering

The test did not destroy the ontology. It refined it.

---

## 15. Core Rationale

CARP v0.2 exists because representation is richer than claims.

The project learned this by building. Discovery exposed lossy compatibility signals. Exchange exposed disclosure boundaries. False positives exposed Constraints. Compatibility exposed Patterns. Workspace exposed Evidence and grounding. Stress testing exposed Divergence complexity.

CARP v0.2 does not make agents certain. It makes their uncertainty legible.
