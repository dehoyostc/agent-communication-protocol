# CARP v0.3 — Knowledge Layers
### Foundational Architecture Document

---

## Abstract

This document establishes Knowledge Layers as a foundational architectural concept within CARP. It defines two orthogonal dimensions of knowledge contained in the Belief Graph, introduces Meta-Representational Knowledge as a distinct and essential category, formalizes Cognitive Dynamics as its first domain, and defines the CARP Projection as the mechanism through which the Belief Graph is externalized. These concepts extend CARP's existing framework without replacing it. Every architectural addition described here is derivable from the existing CARP Axioms.

---

## Status of This Document

**Version:** 0.3 (draft)
**Status:** Foundational — intended to be read before schema definitions
**Relationship to prior versions:** Extends CARP v0.2. Does not alter existing object definitions, lifecycle rules, or conformance requirements. Introduces two new concepts (Knowledge Layers, CARP Projection) and one new domain (Cognitive Dynamics).

---

## 1. Introduction

CARP was originally designed to represent what is known about an entity — its skills, preferences, values, constraints, and identity — through confidence-aware, evidence-backed claims.

During architectural development, a second category of knowledge emerged that cannot be adequately represented as facts, preferences, or skills. This category describes not what is known about an entity, but how that entity engages with knowledge itself: how it receives information, evaluates evidence, revises internal models, communicates uncertainty, and makes decisions.

These two categories are not sequential. They are not hierarchical. They are orthogonal dimensions of the same internal model, populated simultaneously from the same evidence stream.

This document formalizes that distinction, establishes the architectural relationship between the two dimensions, and introduces Cognitive Dynamics as the first standardized domain of the second.

---

## 2. The Belief Graph

The Belief Graph is an agent's internal confidence-aware knowledge model. It is not a profile, a database, or a static artifact. It continuously evolves as new evidence arrives, is maintained by the Reconciliation Engine, and is never directly transmitted to another agent.

The Belief Graph contains two orthogonal knowledge dimensions:

- **Representational Knowledge** — what is currently believed about the entity
- **Meta-Representational Knowledge** — how the entity processes, evaluates, and revises knowledge

These dimensions are orthogonal in the precise sense: neither is derived from the other, neither depends on the other being complete, and both are populated continuously from the same shared evidence stream. A third dimension, if established in a future version of this specification, would be added alongside these two without altering the definition of the Belief Graph itself.

The same observation may contribute evidence to one dimension, the other, or both. CARP places no requirement that every observation populate every knowledge dimension.

```
┌─────────────────────────────────────────────────────┐
│                    BELIEF GRAPH                     │
│                                                     │
│  ┌───────────────────────┐  ┌───────────────────┐  │
│  │  Representational     │  │  Meta-            │  │
│  │  Knowledge            │  │  Representational │  │
│  │                       │  │  Knowledge        │  │
│  │  • Identity           │  │                   │  │
│  │  • Skills             │  │  • Cognitive      │  │
│  │  • Preferences        │  │    Dynamics       │  │
│  │  • Values             │  │  • (future        │  │
│  │  • Constraints        │  │    domains)       │  │
│  │  • Relationships      │  │                   │  │
│  │  • Patterns           │  │                   │  │
│  └───────────────────────┘  └───────────────────┘  │
│                                                     │
│           ↑ Shared Evidence Stream ↑               │
│         (Revision Events are a particularly        │
│          informative subset for Meta-RK)           │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
                 CARP Projections
                         │
                         ↓
                   CARP Exchanges
```

---

## 3. Representational Knowledge

Representational Knowledge describes the observable state of an entity. It answers the question: *what is currently believed about this entity?*

Representational Knowledge includes claims about:

- **Identity** — who or what the entity is
- **Skills** — what the entity is capable of
- **Preferences** — what the entity chooses when unconstrained
- **Values** — what the entity treats as important
- **Constraints** — what limits the entity's options
- **Relationships** — how the entity connects to other entities
- **Patterns** — recurring behavioral regularities
- **History** — what the entity has done and experienced

All Representational Knowledge claims conform to standard CARP requirements: they carry confidence scores, provenance labels, evidence counts, lifecycle metadata, and disclosure controls. Nothing in this document alters those requirements.

---

## 4. Meta-Representational Knowledge

Meta-Representational Knowledge describes how an entity engages with knowledge itself. It answers the question: *how does this entity receive, evaluate, revise, communicate, and incorporate information?*

This is a categorically different kind of knowledge from Representational Knowledge. A preference claim describes what an entity wants. A skill claim describes what an entity can do. A Meta-Representational claim describes the processes through which an entity forms, holds, and updates all of its other beliefs.

For this reason, Meta-Representational Knowledge is not simply another category of Representational Knowledge. It is a distinct dimension — one whose observations are informed by the same evidence stream but which describe a different aspect of the entity entirely.

### 4.1 What Meta-Representational Knowledge Is

Meta-Representational Knowledge consists of evidence-backed, probabilistic observations describing recurring patterns in how an entity processes information.

Examples include:

- how the entity weighs different types of evidence
- how the entity communicates uncertainty
- how readily the entity revises beliefs in response to new information
- what communication structures the entity responds to most effectively
- how the entity handles ambiguity
- what level of abstraction the entity prefers
- how the entity makes decisions under uncertainty

All of these are behavioral observations. They describe what can be seen, not what is inferred about hidden mental states.

### 4.2 What Meta-Representational Knowledge Is Not

Meta-Representational Knowledge is not:

- personality typing or psychological profiling
- psychiatric or diagnostic categorization
- intelligence measurement
- immutable trait attribution
- normative evaluation (better or worse reasoning)
- prediction of future behavior treated as deterministic

CARP does not model hidden mental states. It models observable behavioral patterns supported by evidence. The distinction is not merely rhetorical — it determines what evidence is admissible, what confidence scores are valid, and what disclosures are appropriate.

### 4.3 Entity Agnosticism

Meta-Representational Knowledge applies to every entity type CARP can represent.

**Individual:**
- updates beliefs when presented with more coherent explanatory models
- prefers written context before verbal conclusions
- maintains high confidence in claims with strong cross-domain convergence

**Organization:**
- makes decisions through consensus processes
- revises strategy rapidly following new market information
- requires dashboard summaries rather than narrative reports before committing

**AI Agent:**
- expresses uncertainty explicitly before asserting conclusions
- prefers chain-of-thought reasoning structures in exchanges
- revises confidence incrementally rather than discontinuously

**Government or Institution:**
- requires procedural evidence formats before policy revision
- operates through hierarchical approval chains
- revises positions slowly and with formal acknowledgment

**Project or Team:**
- iterates rapidly based on experimental outcomes
- makes milestone-driven decisions
- favors experimentation over extensive prior planning

The representational framework is identical across all entity types. The observations differ; the structure does not.

---

## 5. The Shared Evidence Stream

Both knowledge dimensions are populated from a single shared evidence stream. There are not separate input channels for Representational Knowledge and Meta-Representational Knowledge. The same observed interactions, outputs, decisions, and exchanges produce evidence for both simultaneously.

An observed decision, for example, may simultaneously contribute evidence to:
- a Representational claim about the entity's values or preferences
- a Meta-Representational claim about the entity's decision-making process

The Reconciliation Engine processes both from the same underlying observation set. Neither dimension waits for the other to be complete.

### 5.1 Revision Events

Within the shared evidence stream, **Revision Events** are a particularly informative subset for Meta-Representational Knowledge.

A Revision Event is an observable instance in which an entity demonstrates interaction with new information. Examples include:

- changing a previously held belief following new evidence
- refusing to change a belief despite contrary evidence
- requesting additional evidence or clarification before updating
- increasing or decreasing expressed confidence
- replacing one explanatory model with another
- explicitly acknowledging uncertainty before concluding

Revision Events are informative for Meta-Representational Knowledge because they expose the *process* through which information is evaluated — not merely the *outcome* of that evaluation. Repeated Revision Events across different contexts allow higher-confidence Meta-Representational observations to emerge.

Revision Events also contribute to Representational Knowledge. The same event that reveals how an entity updates beliefs may also reveal what the entity now believes. The two are not exclusive.

---

## 6. Cognitive Dynamics

Cognitive Dynamics is the first standardized domain of Meta-Representational Knowledge within CARP.

### 6.1 Definition

Cognitive Dynamics consists of evidence-backed, probabilistic observations describing how an entity receives, evaluates, updates, communicates, and incorporates information internally — distinct from the external actions that follow from those processes, which belong to the Agency layer.

### 6.2 Example Observations

The following illustrate the kind of observations Cognitive Dynamics captures. All are evidence-backed, confidence-weighted, and continuously revisable:

- *Prefers framework before conclusions* — consistently requests structural context before engaging with specific claims
- *Readily revises beliefs when presented with higher explanatory models* — demonstrated across multiple observed Revision Events
- *Communicates uncertainty explicitly* — consistently qualifies conclusions with confidence language
- *Favors conceptual coherence over isolated evidence* — weights cross-domain convergence heavily in belief formation
- *Seeks consensus before major decisions* — observable pattern across high-stakes decision contexts
- *High ambiguity tolerance* — maintains effective function in low-information contexts

### 6.3 Conformance Requirements

All Cognitive Dynamics observations must satisfy standard CARP claim requirements:

- confidence score supported by evidence count
- explicit provenance label
- lifecycle metadata (generated_at, reviewed_at, expires_at where applicable)
- disclosure controls
- associated divergences where conflicting observations exist

No special evidentiary standard applies to Meta-Representational claims. They are CARP claims. They are governed by CARP's existing conformance rules.

### 6.4 The Self-Description Divergence

An entity's self-described reasoning process and its observed reasoning behavior may diverge. This is not an error condition. It is a first-class signal.

An entity that describes itself as highly open to feedback but whose Revision Events consistently show resistance to external evidence carries a divergence between a self-declared Meta-Representational claim and a behaviorally-evident one. CARP preserves both, with supporting evidence, exactly as it would preserve any other divergence.

This divergence is often more informative than either claim in isolation. Receiving agents should treat it as a positive signal about the epistemic richness of the profile — not as a reliability concern.

---

## 7. CARP Projection

A **CARP Projection** is a serialized, permissioned, context-specific view of a subset of the Belief Graph, generated on demand for a specific exchange purpose.

A CARP Projection is:

- **Generated** — produced at exchange time, not retrieved from storage
- **Scoped** — contains a purposefully selected subset of the Belief Graph
- **Purposeful** — created for a declared exchange context
- **Not the Belief Graph** — a projection does not expose the internal model; it expresses a view of it

The Belief Graph may contain rich Meta-Representational observations about an entity. A CARP Projection for an employment compatibility exchange might include a subset of those observations relevant to working-style compatibility. A projection for a healthcare coordination exchange might include a different subset. Neither projection is the Belief Graph. Both are valid, independently scoped expressions of it.

This distinction has privacy, architectural, and philosophical implications:

**Privacy:** An agent never exposes its full internal model. Each exchange receives only what is authorized for that purpose.

**Architecture:** The Belief Graph can evolve continuously without invalidating prior projections. Each projection reflects the state of the graph at generation time.

**Philosophy:** There is no canonical "profile" of an entity. There are only context-specific projections. This is not a limitation — it is the correct model. An entity's representation to a potential employer is not the same as their representation to a healthcare provider, not because they are being deceptive, but because different contexts require different projections of the same underlying knowledge model.

### 7.1 There Is No Canonical Profile

Traditional representation systems assume an entity possesses a single authoritative profile — a document or record that, if retrieved, constitutes "who this entity is."

CARP does not share that assumption.

An entity possesses an internal knowledge model. Every external representation is a context-specific projection of that model. No projection is "the profile." Each is a faithful expression of the same underlying knowledge model for a particular purpose, at a particular moment, under a particular authorization.

This has a practical consequence: two projections of the same entity, generated for different purposes on the same day, may contain different claims, different confidence levels, and different subsets of the available knowledge — and both may be entirely correct. Neither supersedes the other. Neither is more "real" than the other. They are projections.

This framing applies equally to both knowledge dimensions. A Representational projection and a Meta-Representational projection drawn from the same Belief Graph are each faithful to their purpose. The Belief Graph is the source of truth. The projections are its expressions.

Both knowledge dimensions — Representational and Meta-Representational — may be included in a CARP Projection, independently or together, depending on the exchange purpose and the entity's disclosure authorization.

---

## 8. Epistemic Compatibility

The addition of Meta-Representational Knowledge introduces a new compatibility dimension that existing compatibility models do not capture.

**Traditional compatibility** evaluates whether entities can work together based on:
- skill alignment
- preference compatibility
- constraint satisfaction
- goal overlap
- value convergence

**Epistemic compatibility** evaluates whether entities process information in mutually effective ways:
- compatible evidence standards (what convinces each entity)
- compatible abstraction preferences (what level of detail each engages with)
- compatible communication structures (how each entity best receives information)
- compatible uncertainty tolerance (how each entity handles incomplete information)
- compatible revision cadence (how quickly each entity updates its models)
- compatible explanation styles (how each entity structures and receives reasoning)
- compatible decision processes (how each entity moves from evidence to commitment)

Two entities may possess complementary skills and compatible values while being epistemically incompatible in ways that make sustained collaboration difficult. Conversely, entities with different backgrounds and experiences may collaborate exceptionally well because their information-processing dynamics align.

Epistemic compatibility is not a replacement for traditional compatibility evaluation. It is an additional dimension — one that becomes increasingly important as the depth and duration of collaboration increases.

---

## 9. Disclosure Considerations

Meta-Representational claims are subject to the same disclosure controls as all CARP claims. However, their nature warrants specific attention during disclosure design.

Meta-Representational observations describe how an entity reasons, not merely what it prefers or knows. This makes them epistemically more intimate than many Representational claims. An agent that knows an entity's skill profile knows what they can do. An agent that knows an entity's Cognitive Dynamics profile knows how they think.

Conforming implementations should:

- treat Meta-Representational claims as at least as sensitive as personal preference claims during disclosure scoping
- require explicit entity authorization before including Cognitive Dynamics observations in any CARP Projection
- honor the purpose-binding requirement with particular care for Meta-Representational disclosures — a Cognitive Dynamics observation disclosed for communication optimization is not authorized for use in evaluation or screening

These are not new rules. They are applications of existing CARP disclosure requirements to a category of claim whose sensitivity merits explicit acknowledgment.

---

## 10. Relationship to the CARP Axioms

The Knowledge Layers architecture does not require new axioms. Every concept introduced in this document is derivable from the axioms established in CARP v0.2.

**Axiom I — Represent Uncertainty Explicitly**
Meta-Representational claims carry confidence scores and evidence counts. Uncertainty about how an entity reasons is represented as explicitly as uncertainty about what an entity knows.

**Axiom II — Preserve Provenance**
Cognitive Dynamics observations carry provenance labels. A claim that an entity prefers framework before conclusions must indicate whether that observation is self-declared, agent-inferred, or behaviorally evident.

**Axiom III — Treat Divergence as Information**
The self-description divergence described in Section 6.4 is a direct application of this axiom to the Meta-Representational dimension. Divergence between how an entity describes its reasoning and how its Revision Events demonstrate it is signal, not error.

**Axiom IV — Agency Must Never Outrun Understanding**
Meta-Representational Knowledge deepens the understanding that precedes agency. An agent that understands not only what an entity prefers but how it processes information is better positioned to act faithfully on that entity's behalf.

**Axiom V — Standardize Accountability, Not Implementation**
This document defines what Meta-Representational Knowledge must demonstrate — confidence, provenance, revisability, disclosure controls. It does not prescribe how implementations derive Cognitive Dynamics observations. Different reconciliation engines may use different methods; the output requirements are identical.

**Axiom VI — Represent Current Best Models**
Cognitive Dynamics observations are current best models of how an entity processes information. They are revised as new Revision Events accumulate. An observation with low evidence count carries lower confidence. An observation supported by dozens of Revision Events across diverse contexts carries higher confidence. The model evolves; it is never frozen.

---

## 11. Relationship to the CARP Exchange Layer

The CARP exchange layer (L5) governs how CARP Projections are exchanged between agents. The Knowledge Layers architecture interacts with the exchange layer in two ways.

**First:** Both knowledge dimensions may appear in CARP Projections, making them available for CARP exchanges. A CARP exchange may request, disclose, or negotiate over Representational claims, Meta-Representational claims, or both, depending on the declared purpose.

**Second:** An agent's Cognitive Dynamics model of a *counterpart* agent may inform how that agent conducts CARP negotiations. Understanding that a counterpart prefers structured evidence before conclusions, for example, allows an agent to adapt the format of its disclosures to be more effective. This is not a structural dependency — The exchange layer does not require Meta-Representational Knowledge to function — but it is a meaningful strategic application of the second knowledge dimension.

---

## 12. Future Extensibility

Cognitive Dynamics is the first standardized domain of Meta-Representational Knowledge. It is not the last.

Future domains might include:

- **Communication Dynamics** — observable patterns in how an entity structures and adapts its communication
- **Negotiation Dynamics** — observable patterns in how an entity approaches exchange, compromise, and agreement
- **Collaboration Dynamics** — observable patterns in how an entity functions within multi-agent or multi-person contexts

Each future domain would follow the same pattern: evidence-backed, probabilistic observations; standard CARP conformance requirements; entity-agnostic structure; representation as a subset of the Meta-Representational Knowledge dimension of the Belief Graph.

The Belief Graph definition does not change when new domains are added. The definition of the Meta-Representational dimension does not change. The architecture is designed to accommodate extension without restructuring.

---

## 13. Glossary

**Belief Graph** — An agent's internal confidence-aware knowledge model. Contains two orthogonal knowledge dimensions. Never directly transmitted. The source from which CARP Projections are generated.

**Representational Knowledge** — The dimension of the Belief Graph describing what is currently believed about an entity. Includes identity, skills, preferences, values, constraints, relationships, and patterns.

**Meta-Representational Knowledge** — The dimension of the Belief Graph describing how an entity processes, evaluates, and revises knowledge. Includes Cognitive Dynamics and future domains.

**Cognitive Dynamics** — The first standardized domain of Meta-Representational Knowledge. Evidence-backed, probabilistic observations describing how an entity receives, evaluates, updates, and communicates information internally.

**Revision Event** — An observable instance in which an entity demonstrates interaction with new information. The primary evidence primitive for Cognitive Dynamics observations.

**CARP Projection** — A serialized, permissioned, context-specific view of a subset of the Belief Graph, generated on demand for a specific exchange purpose. Not the Belief Graph itself.

**Epistemic Compatibility** — A compatibility dimension evaluating whether entities process information in mutually effective ways. Complementary to, not a replacement for, traditional compatibility evaluation.

**Shared Evidence Stream** — The single source from which both Representational and Meta-Representational knowledge dimensions are populated. Revision Events are a particularly informative subset for Meta-Representational Knowledge.

---

## 14. What This Document Does Not Define

The following are explicitly outside the scope of this document:

- The internal format of the Belief Graph or its implementation
- The algorithms or methods by which Cognitive Dynamics observations are derived
- Specific Cognitive Dynamics schemas or field definitions (to be defined in CARP v0.3 object definitions)
- Additional Meta-Representational domains beyond Cognitive Dynamics
- CARP exchange operations specific to Meta-Representational Knowledge
- Compatibility scoring algorithms that incorporate Cognitive Dynamics

These will be addressed in subsequent specifications or in implementing applications built on CARP.

---

*CARP v0.3 Draft — Knowledge Layers*
*This document is part of the CARP foundational architecture. It should be read alongside the CARP Axioms, Ontology, Lifecycle, and Object Definitions.*
