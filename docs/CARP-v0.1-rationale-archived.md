# CARP v0.1 Design Rationale

*This document explains why CARP was designed the way it was. It is a companion to the formal specification. The specification tells you what a conforming implementation must do. This document tells you why those decisions were made — so that future contributors can understand the reasoning before proposing changes.*

---

## Why Claims?

The first question in any protocol design is: what is the atom?

We considered Profile. But a Profile is a container, not a primitive. You can't reason about a Profile — you can only hold one.

We considered Observation. But observations are raw data. They're private, they're voluminous, and they vary enormously across agents and implementations.

We arrived at Claim because it sits at the right level of abstraction. A Claim is what an agent knows about an entity, expressed as a single assertable statement with explicit uncertainty. It's small enough to compose, rich enough to be meaningful, and structured enough to be machine-readable.

Everything else in CARP is built from collections of Claims, relationships between Claims, or operations on Claims. If that abstraction is wrong, the entire protocol is wrong. We believe it's right.

One note on the word itself: "claim" was chosen deliberately. A claim is not a fact. It is an assertion made by a party with a perspective, a method, and a degree of certainty. That epistemological humility is embedded in the name. A future version of the specification may revisit this terminology, but the concept it represents — an assertion with explicit uncertainty — is non-negotiable.

---

## Why Confidence?

Because the alternative is false certainty.

Every existing representation format — resumes, profiles, job descriptions, reference letters — presents information as if it were simply true or false. Either you have the skill or you don't. Either the company values autonomy or it doesn't.

This is a lie of omission. All knowledge is uncertain. All observations are incomplete. All self-assessments are partially wrong.

CARP forces agents to be explicit about how certain they are. A confidence score of 0.87 is not precise — it is honest. It tells the receiving agent: *this is what I believe, and this is how strongly I believe it.*

One important constraint: confidence scores in CARP v0.1 are meaningful only within the output of a single originating agent. They are not comparable across agents. Claude's 0.82 and another system's 0.82 may reflect entirely different calibration methods. A future version of this specification may address confidence calibration standards. For now, treat confidence as a relative signal, not an absolute measure.

---

## Why Divergence as a First-Class Object?

This was the most debated design decision.

The easy path was to represent divergence implicitly — as two claims with conflicting content and let the receiving agent figure it out. We rejected this for one reason: it lets senders hide contradictions by simply not including one of the conflicting claims.

Divergence needed to be a first-class object because it needed to be undeniable.

When an agent discloses claims about an entity, it must also disclose any divergences associated with those claims. You cannot share the self-declared value while suppressing the observed behavior that contradicts it. That selective disclosure is exactly how existing systems mislead.

There is a deeper reason too. The most interesting information about a person or organization often lives in the gap between what they believe about themselves and what their behavior demonstrates. A company that sincerely believes it empowers people but whose decision structure is deeply centralized is not lying — it is aspirational. That aspiration is meaningful. So is the gap. Both deserve representation.

By making Divergence a first-class object with a status field, CARP allows entities to be honest about their contradictions without being penalized for them. An `aspirational` divergence is not a failure. It is a signal that the entity knows where they are and where they want to be.

---

## Why Disclosure?

Because sharing a profile is not the same as authorizing its use.

CARP separates the act of representation from the act of exchange. An agent can hold a rich profile about an entity indefinitely. That profile goes nowhere until a Disclosure operation is explicitly initiated.

Disclosure has four required constraints: a declared purpose, a specific scope of claims, a minimum confidence threshold, and an expiry. All four must be present. None can be waived.

This design reflects a core belief: data shared for one purpose should not be reusable for another. A Disclosure for evaluating communication compatibility does not authorize use of the same claims for any other purpose. When the disclosure expires, the obligation to honor its constraints expires with it — but the data must not be retained.

The purpose binding is not merely a privacy feature. It is an honesty feature. It forces the receiving agent to declare what it actually wants to know, rather than requesting everything and sorting it out later.

---

## Why Not Matching?

Because matching is an application, not a primitive.

Matching requires a definition of what constitutes a good match. That definition varies by domain, by context, by the values of the parties involved, and by factors that no protocol can anticipate. Employment matching is different from investment matching, which is different from co-founder matching, which is different from research collaboration matching.

If CARP defined matching, it would either define it so narrowly as to be useless in most domains, or so broadly as to be meaningless in all of them.

CARP defines what agents know about entities and how they share that knowledge. What they do with that knowledge — including matching — is a higher-order problem that should be solved by applications built on top of CARP, not by the protocol itself.

---

## Why Not Jobs?

Because the protocol that solves hiring is not the same protocol that solves everything else.

The initial motivation for CARP came from a problem in employment: the mismatch between how AI systems understand people and organizations, and the primitive artifacts — resumes, job descriptions — that those same people and organizations use to represent themselves.

But as the design progressed, it became clear that the underlying problem was not specific to hiring. It was about representation itself. How does an AI agent describe a human being to another AI agent, in a way that is honest, portable, and epistemically transparent?

That problem exists in every domain where humans interact with institutions through AI intermediaries. Employment is simply the first domain where the pain is acute enough that someone was motivated to solve it.

By refusing to mention jobs, candidates, or employment anywhere in the core specification, CARP remains available to every domain that needs it. Hiring applications will be built on CARP. So will other things we have not yet imagined.

---

## Why No Central Registry?

Because centralization creates capture.

A central registry of human profiles — however well-intentioned — is a surveillance infrastructure. It creates a single point of failure, a single point of control, and a single point of commercial exploitation. Every existing professional network has demonstrated what happens when profile data centralizes: it becomes a product, and the person it describes becomes the inventory.

CARP profiles are generated on demand and shared peer-to-peer through the Disclosure operation. No central authority is required to generate a profile, validate a claim, or execute a disclosure. No single entity can revoke access to the protocol.

This is not naïve decentralization for its own sake. It is a deliberate structural choice to ensure that the protocol cannot be captured by any single commercial interest — including the organizations that authored it.

---

## What CARP Is Not Trying to Be

CARP is not trying to determine truth. It is trying to communicate what is believed, how that belief was formed, and how certain the believer is.

CARP is not trying to replace human judgment. It is trying to give human judgment better inputs.

CARP is not a recruiting tool, a matchmaking platform, or an AI agent. It is the protocol layer on which those things can be built — honestly, transparently, and without hiding the uncertainty that has always been present but never before acknowledged.

---

## A Final Note

The sentence that guided every design decision in CARP v0.1 was this:

> *The protocol is designed around epistemic transparency rather than certainty.*

When in doubt about any future design decision, return to that sentence. If the proposed change increases certainty at the cost of transparency, it is probably wrong. If it increases transparency at the cost of apparent precision, it is probably right.

The world has enough systems that pretend to know more than they do.

CARP is not one of them.

---

*End of CARP v0.1 Design Rationale*
