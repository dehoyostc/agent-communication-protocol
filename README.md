# Agent Communication Protocol (ACP)

**ACP** is an open protocol for structured, privacy-preserving communication between AI agents acting on behalf of people and organizations.

**CARP** (Confidence-Aware Representation Protocol) is the representation layer within ACP — defining how agents describe entities through confidence-weighted, provenance-labeled claims rather than flat assertions.

---

## The problem

AI agents can now reason, search, plan, and act. What they cannot do — safely, consistently, across systems — is represent the humans and organizations they serve to each other.

Today, when two AI agents need to exchange information about a person or organization, there is no shared format, no authorization layer, no principled way to say: *here is what I know, here is how confident I am, here is what I am permitted to share, and here is where the evidence contradicts itself.*

The result is unstructured disclosure, incompatible representations, and no privacy guarantees.

ACP is an attempt to define the infrastructure layer that makes honest, structured, privacy-preserving agent-to-agent communication possible.

---

## What this repository contains

| Directory | Contents |
|---|---|
| `specs/` | CARP v0.2 specification |
| `docs/` | Architecture overview, design principles, rationale, ontology |
| `schemas/` | JSON schemas for all CARP v0.2 objects |
| `engine/` | Reference implementation (Python, v0.2.3-alpha) |
| `conformance/` | Conformance suite, fixtures, and 13 adversarial tests |
| `examples/` | Example exchange outputs across named fixture pairs |
| `demos/` | Interactive HTML demos of agent exchange and profile recovery |

## Roadmap

| Status | Item |
|---|---|
| ✓ | CARP representation specification (v0.2) |
| ✓ | JSON schemas for all core objects |
| ✓ | Reference implementation (Python) |
| ✓ | Conformance suite with named fixture pairs |
| ✓ | Adversarial test suite (AF-001 through AF-013) |
| Next | Discovery layer (DISCOVER operation) |
| Next | Trust & authorization layer (L3) |
| Next | Negotiation protocol (L6 — MATCH, COMPARE, NEGOTIATE) |
| Next | Multi-agent interoperability across independent implementations |

---

## Core concepts

**Claim** — the atomic unit. A single confidence-weighted, provenance-labeled statement about an entity. Not a fact. An assertion with explicit uncertainty.

**Profile** — a collection of claims about a single entity, including divergences where evidence conflicts.

**Divergence** — a first-class object representing a meaningful conflict between two claims. Not an error. Signal.

**Disclosure** — a controlled, purpose-bound, time-limited release of a scoped subset of claims. All disclosures require declared purpose and expiry.

The protocol is designed around **epistemic transparency rather than certainty**.

---

## Quick start

Run the reference implementation and verify that all conformance and adversarial tests pass.

```bash
pip install -r requirements.txt
python engine/run_conformance.py
python engine/run_adversarial.py
```

---

## Architecture

ACP is the overall protocol stack. CARP is the representation layer within that stack. The full layer definitions:

```
L7  Application (hiring, matching, investing — built on ACP, not part of it)
L6  Negotiation (MATCH, COMPARE, NEGOTIATE — planned)
L5  Exchange    (DISCLOSE, VERIFY — partial in v0.2)
L4  Representation ◄── CARP (this repo)
L3  Trust & Authorization (planned)
L2  Authentication (planned — likely DIDs + VCs)
L1  Transport (delegated to HTTPS, MCP, etc.)
```

See `docs/architecture-overview.md` for the full layer definitions.

---

## Status

**Alpha (v0.2.3).** The representation layer (L4), schemas, reference engine, conformance suite, and adversarial tests are implemented. Negotiation (L6) and trust (L3) layers remain future work.

See `RELEASE_NOTES.md` for what is and is not working in the current release.

---

## Design principles

> **Reality Over Narrative**
>
> Representation should optimize for evidence and uncertainty, not persuasion.

Existing representation systems are optimized for narrative — resumes, job descriptions, LinkedIn profiles. CARP is built on the opposite premise: confidence over certainty, divergence as signal, transparency over persuasion.

See `docs/CARP-design-principles.md` for the full constitutional document.

---

## Governance

ACP is intended to be an open standard with no single controlling entity.

The specification is maintained under CC BY 4.0. Reference implementations are MIT licensed. Feedback via issues. As the project matures toward wider adoption, governance will transfer to an independent body.

---

## Why now

The infrastructure question — how do AI agents represent the entities they serve, and how do they exchange that representation safely — is being answered today by default, through ad hoc application logic that is not interoperable, not auditable, and not designed to handle the privacy and authorization requirements the problem demands.

ACP is an attempt to define that standard before the ecosystem calcifies around incompatible conventions.

See `docs/why-now.md` for the full argument.
