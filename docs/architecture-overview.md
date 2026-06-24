# ACP Architecture Overview

The Agent Communication Protocol (ACP) is a layered architecture. Each layer has a distinct responsibility. Layers depend on the layers beneath them but remain independent of the layers above them.

This document defines the seven layers, their responsibilities, their current specification status, and how they relate to each other.

---

## The Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  L7  APPLICATION LAYER                                          │
│       Hiring · matching · investing · mentorship · collaboration │
│       Not part of ACP. Built on top of it.                      │
├─────────────────────────────────────────────────────────────────┤
│  L6  NEGOTIATION LAYER                                          │
│       MATCH · COMPARE · NEGOTIATE · COLLABORATE · DISCOVER      │
│       Future scope. Planned for ACP v0.2+.                      │
├─────────────────────────────────────────────────────────────────┤
│  L5  EXCHANGE LAYER                                             │
│       DISCLOSE · VERIFY · purpose binding · expiry · revocation │
│       Partially defined in CARP v0.1. Expanded in future specs. │
├─────────────────────────────────────────────────────────────────┤
│  L4  REPRESENTATION LAYER  ◄── CARP                            │
│       Claim · Profile · Divergence · provenance · confidence    │
│       Defined in CARP v0.1. This is the core of ACP.           │
├─────────────────────────────────────────────────────────────────┤
│  L3  TRUST & AUTHORIZATION LAYER                                │
│       Permissions · consent · delegation · agent authority      │
│       Not yet defined. Critical for safe agent operation.       │
├─────────────────────────────────────────────────────────────────┤
│  L2  AUTHENTICATION LAYER                                       │
│       Agent identity · entity binding · session integrity       │
│       Not yet defined. Likely built on DIDs + VCs.             │
├─────────────────────────────────────────────────────────────────┤
│  L1  TRANSPORT LAYER                                            │
│       Agent-to-agent messaging · routing · delivery             │
│       Delegated to existing protocols (HTTPS, MCP, etc.)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### L1 — Transport

**Responsibility:** Moving messages between agents reliably.

**What this layer answers:** How does a message from Agent A reach Agent B? What delivery guarantees exist?

**Current status:** ACP delegates this layer to existing protocols. Conforming implementations may use HTTPS, WebSockets, or emerging agent-to-agent messaging protocols such as MCP (Model Context Protocol). ACP does not define a new transport.

**Dependencies:** None.

---

### L2 — Authentication

**Responsibility:** Establishing that an agent is who it claims to be, and that it genuinely represents the entity it claims to represent.

**What this layer answers:** Is this agent legitimate? Does it have a verifiable binding to the entity on whose behalf it is acting?

**Current status:** Not yet defined. A future ACP specification will address this layer. The likely approach is Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs), both W3C standards. Agent identity must be separable from platform identity — an agent's identity should survive migration between AI systems.

**Dependencies:** L1 (Transport).

**Why this matters:** A CARP profile disclosed by an agent that cannot prove it represents a given entity is meaningless. Authentication is what makes the representation trustworthy.

---

### L3 — Trust and Authorization

**Responsibility:** Defining what an agent is permitted to do on behalf of an entity, and under what conditions.

**What this layer answers:** Is this agent authorized to disclose these claims? Can it initiate a negotiation? Can it accept terms? Who has oversight of its actions?

**Current status:** Not yet defined. This is where human oversight of AI agents lives architecturally. A well-designed authorization layer should make it structurally impossible for an agent to exceed its mandate — disclosing more than permitted, accepting terms without confirmation, or acting on behalf of an entity in ways the entity did not authorize.

**Dependencies:** L1, L2.

**Key design challenge:** Authorization must be granular (this agent may disclose professional claims but not personal ones), delegable (the entity may grant temporary elevated permissions), and auditable (every authorized action should be traceable to an explicit grant).

---

### L4 — Representation (CARP)

**Responsibility:** Defining how agents describe entities — individuals, teams, and organizations — in a structured, honest, and epistemically transparent way.

**What this layer answers:** How should one agent describe a human being or organization to another agent? What does a claim look like? How is confidence expressed? How are contradictions surfaced?

**Current status:** Defined in [CARP v0.1](../specs/CARP-v0.1.md). This is the most developed layer in ACP.

**Core primitives:**
- **Claim** — a single confidence-weighted, provenance-labeled statement about an entity
- **Profile** — a collection of claims about a single entity
- **Divergence** — a conflict between two claims, treated as signal rather than error
- **Disclosure** — a controlled, purpose-bound, time-limited release of claims

**Dependencies:** L1, L2, L3 (a disclosure without authorization is a privacy violation).

**Design principle:** The representation layer does not attempt to determine whether claims are true. It communicates what is believed, how that belief was formed, and how confident the agent is. *The protocol is designed around epistemic transparency rather than certainty.*

---

### L5 — Exchange

**Responsibility:** Governing the mechanics of how agents request, share, and negotiate over representations.

**What this layer answers:** How does an agent initiate a disclosure? How does it request specific claims? How does it handle partial disclosures, expired disclosures, and revocations?

**Current status:** The DISCLOSE operation is defined in CARP v0.1. The VERIFY operation (third-party attestation of a claim) is anticipated but not yet specified. Future ACP versions will define the full exchange protocol including multi-turn exchanges where both agents disclose simultaneously.

**Dependencies:** L1–L4.

---

### L6 — Negotiation

**Responsibility:** Enabling agents to act on representations — comparing compatibility, exploring options, and negotiating outcomes on behalf of their entities.

**What this layer answers:** How do two agents determine compatibility between the entities they represent? How do they communicate proposed terms? How do they handle disagreement?

**Current status:** Not yet defined. Anticipated operations: MATCH, COMPARE, NEGOTIATE, COLLABORATE, DISCOVER. Planned for ACP v0.2+.

**Dependencies:** L1–L5.

**Design constraint:** Negotiation operations must remain advisory. Agents should surface options and assessments to humans; binding agreements require explicit human authorization at L3.

---

### L7 — Application

**Responsibility:** Domain-specific use cases built on top of ACP.

**Examples:** Employment matching, investment partnership evaluation, co-founder compatibility, mentorship pairing, consulting engagement, research collaboration.

**Current status:** Outside the scope of ACP. Application developers build on ACP; they do not modify it. The protocol intentionally contains no domain-specific vocabulary (no "job," "candidate," "employer," "investor," or "mentor" anywhere in the core spec).

**Design principle:** Any application that requires honest, confidence-weighted, provenance-aware representation of entities can build on ACP. The protocol should never be modified to accommodate a specific application's assumptions.

---

## Specification Status Summary

| Layer | Name | Status | Spec |
|---|---|---|---|
| L7 | Application | Out of scope | — |
| L6 | Negotiation | Not yet defined | Planned: ACP v0.2 |
| L5 | Exchange | Partial | CARP v0.1 (DISCLOSE) |
| L4 | Representation | Defined | [CARP v0.1](../specs/CARP-v0.1.md) |
| L3 | Trust & Authorization | Not yet defined | Planned: ACP v0.2 |
| L2 | Authentication | Not yet defined | Planned: ACP v0.2 |
| L1 | Transport | Delegated | Existing protocols |

---

## What ACP Is Not

ACP is not a product, a platform, or a marketplace. It is infrastructure — the shared language that makes honest agent-to-agent communication possible across any AI system, any domain, and any application.

ACP does not assume that agents are built on any particular AI model. A conforming ACP agent may be powered by any AI system capable of generating CARP-conforming representations and executing ACP-conforming exchange operations.

ACP does not define how agents generate their understanding of the entities they represent. The internal processes of an AI agent — how it builds its model of a person or organization — are outside the scope of this protocol. ACP only defines what a conforming output of that process looks like.

---

*For the full design philosophy, read the [CARP Design Principles](../principles/CARP-design-principles.md). For the rationale behind specific design decisions, read the [CARP Design Rationale](CARP-v0.1-rationale.md).*
