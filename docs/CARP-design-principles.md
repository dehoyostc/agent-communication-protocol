# CARP Design Principles

*This is not the protocol specification. This is not the design rationale. This is the constitutional document for CARP — the principles that guided its original design and should guide every future decision about its evolution.*

*A contributor reading this document ten years from now should understand the spirit of CARP even if the protocol itself has changed dramatically. These principles are not rules. They are values. They exist to preserve the philosophical core of the protocol through the inevitable pressures of adoption, commercialization, and extension.*

---

## The Master Principle: Reality Over Narrative

Every principle in this document is a specific expression of one deeper commitment: **prefer reality, even when reality is messy.**

Existing representation systems are optimized for narrative. A resume is a story. A job description is a story. A LinkedIn profile is a story. Stories are coherent, selective, and persuasive. They hide contradictions, suppress uncertainty, and present a polished surface in place of an accurate one.

CARP is built on the opposite premise. Confidence over certainty — because reality is uncertain. Divergence as signal — because reality is contradictory. Transparency over persuasion — because reality is more useful than narrative. Representation over identity — because reality is about how entities actually operate, not how they are credentialed.

All of the principles below are manifestations of this commitment. When they appear to conflict, the question to ask is: which path leads closer to reality?

CARP representations are not truths. They are current best models — provisional, confidence-weighted understandings that should be revised as new observations emerge. An agent that generated a profile six months ago should be capable of generating a different profile today. That is not a failure of consistency. It is evidence that the system is working.

---

## I. Representation Over Identity

**What it means:** CARP describes how entities operate, not who they are. It is not an identity protocol. It does not issue credentials, verify legal identity, or establish authenticity in the traditional sense. It represents understanding — the patterns, tendencies, motivations, and characteristics that define how a person or organization actually functions in the world.

**Why it matters:** Identity systems answer the question: *Is this person who they say they are?* CARP answers a different question: *Who is this person?* These are not the same question. The first is about authentication. The second is about understanding. Conflating them would reduce CARP to another credentialing system — useful, but not foundational.

**How it should guide future decisions:** When a proposed extension asks CARP to verify, authenticate, or certify, it is probably asking the wrong protocol. When it asks CARP to represent more richly, more honestly, or more completely, it is probably asking the right one.

---

## II. Confidence Over Certainty

**What it means:** Every claim in CARP carries a confidence score because no claim is simply true or false. Knowledge exists on a spectrum. Observations are incomplete. Self-assessments are partially wrong. Agents have limited information. CARP does not pretend otherwise.

**Why it matters:** The systems CARP is designed to replace — resumes, job descriptions, profiles — present information as if it were simply true. This false certainty is not neutral. It misleads. It causes good matches to be missed and bad matches to be made. Confidence-weighting is not a technical feature. It is a commitment to honesty about the limits of what any agent can know.

**How it should guide future decisions:** Any extension that strips confidence metadata from claims, normalizes scores across agents without calibration, or introduces binary qualified/unqualified outputs is moving away from this principle. The goal is not to appear more certain. The goal is to be more accurate about uncertainty.

---

## III. Transparency Over Persuasion

**What it means:** CARP is not a presentation layer. It is not designed to help entities put their best foot forward. It is designed to help entities represent themselves accurately — including their contradictions, their gaps, and their unknowns. The purpose of a CARP profile is not to persuade. It is to inform.

**Why it matters:** Every existing representation format is optimized for persuasion. Resumes highlight strengths and omit weaknesses. Job descriptions advertise culture rather than describe it. Mission statements express aspiration rather than reality. The result is a system where both parties enter relationships based on curated impressions rather than honest understanding. CARP exists to correct this.

**How it should guide future decisions:** When a proposed feature makes profiles more impressive, it should be scrutinized. When it makes profiles more accurate — even at the cost of appearing less favorable — it should be welcomed. Divergence is a feature, not a flaw. Acknowledged gaps are more trustworthy than polished surfaces.

---

## IV. Disclosure Over Collection

**What it means:** CARP does not collect profiles. It does not store them. It does not aggregate them. It enables agents to generate representations on demand and share specific, scoped, time-limited subsets of those representations for declared purposes. The default state of a CARP profile is private. Sharing is the exception, not the rule.

**Why it matters:** Every system that collects profiles eventually becomes a surveillance infrastructure. The data that was shared to find a job becomes the data used to price insurance, set credit limits, or evaluate fitness for opportunities the entity never consented to. CARP's architecture is designed to make this kind of accumulation structurally difficult, not merely contractually prohibited.

**How it should guide future decisions:** Any extension that introduces persistent profile storage, cross-purpose data reuse, or centralized profile aggregation — however well-intentioned — should be treated with extreme caution. The question is not whether the intent is benign. The question is whether the architecture could be abused once it exists.

---

## V. Divergence Is Signal

**What it means:** Contradictions between what an entity believes about itself and what its behavior demonstrates are not errors to be hidden or resolved. They are among the most valuable information the protocol can surface. CARP treats divergence as a first-class object — something to be disclosed, labeled, and interpreted, not suppressed.

**Why it matters:** The interesting truth about a person or organization often lives in the gap between self-perception and observed behavior. A leader who believes they delegate but whose team reports every decision flowing upward is not lying — they are unaware. That unawareness is meaningful. So is the gap. A protocol that hides this divergence in the name of presenting a coherent picture is a protocol that enables self-deception at scale.

**How it should guide future decisions:** Extensions that make it easier to surface and categorize divergences are aligned with this principle. Extensions that allow divergences to be suppressed, resolved without acknowledgment, or hidden behind aggregate scores are not. The goal is not harmony. The goal is accuracy.

---

## VI. Entity Ownership Over Platform Control

**What it means:** Entities own their representations. Agents generate profiles on behalf of entities and at their direction. No platform, no implementing organization, and no standards body owns a person's profile. The protocol exists to serve the entity being represented, not the systems that process their representation.

**Why it matters:** Every professional network ever built has eventually discovered that user profiles are a more valuable asset than user relationships. The temptation to monetize, restrict, or leverage accumulated profile data is not hypothetical — it is the default outcome of centralized profile ownership. CARP is designed so that this outcome is architecturally unavailable, not merely contractually forbidden.

**How it should guide future decisions:** When a proposed extension shifts control of profile generation, storage, or access from the entity to a platform, it is moving away from this principle. The test is simple: can the entity leave any implementing platform and take their representation with them? If not, the platform owns the profile. CARP should never enable that outcome.

---

## VII. Infrastructure Over Application

**What it means:** CARP is a protocol, not a product. It defines how agents represent entities and exchange those representations. It does not define what should be done with those representations. Matching, scoring, hiring, investing, collaborating — these are applications. CARP is the layer beneath them.

**Why it matters:** A protocol that encodes the assumptions of its first application becomes permanently limited to that application. HTTP did not encode the assumptions of the first website. TCP/IP did not encode the assumptions of the first email system. Their generality is why they became infrastructure rather than historical curiosities. CARP must maintain the same discipline.

**How it should guide future decisions:** When a proposed extension solves a specific application problem elegantly, ask whether it does so by encoding application-specific assumptions into the protocol layer. If yes, the extension belongs in an application built on top of CARP, not in CARP itself. The protocol should become more expressive over time, not more specific.

---

## VIII. Epistemic Humility as Architecture

**What it means:** CARP is not merely humble in tone. It is humble in structure. The provenance system, the confidence scores, the divergence objects, the evidence counts — these are not decorative metadata. They are architectural acknowledgments that knowledge is uncertain, observations are incomplete, and agents are fallible. The protocol encodes these limitations rather than hiding them.

**Why it matters:** Systems that pretend to know more than they do cause harm in proportion to their confidence. A hiring algorithm that presents a match score without uncertainty bounds is more dangerous than one that expresses its uncertainty honestly — not because the underlying model is worse, but because the false precision prevents appropriate human judgment. CARP is designed to support human judgment, not replace it.

**How it should guide future decisions:** Any extension that produces outputs without uncertainty quantification, presents aggregate scores without component transparency, or obscures the provenance of its conclusions is moving away from this principle. The goal is not to appear authoritative. The goal is to be useful — which requires being honest about the limits of what the protocol knows.

---

## IX. Open Governance as Obligation

**What it means:** CARP is an open standard. No single entity controls it. This is not a feature of the initial release. It is a permanent commitment. The authors of CARP v0.1 do not own CARP. They authored a specification and committed to transferring its governance to an independent body. Future contributors inherit that commitment.

**Why it matters:** A protocol about honest representation cannot be owned by a party with commercial interests in how entities are represented. The conflict of interest is structural and irresolvable. Open governance is not idealism. It is the only architecture under which CARP can remain trustworthy over time.

**How it should guide future decisions:** Governance decisions should always increase the independence of the protocol from any single commercial interest, including the organizations most invested in its success. Concentration of contributor influence, intellectual property claims over extensions, and proprietary conformance certifications are all warning signs. The protocol belongs to everyone who implements it honestly.

---

## The Test

When a future contributor proposes a feature, an extension, or a change to the protocol, these questions should be applied before the technical merits are evaluated. A proposal that fails multiple questions should be rejected or substantially redesigned, regardless of its technical elegance.

**On honesty:**
- Does this make representations more accurate, or does it make them more impressive?
- Does this surface uncertainty, or does it obscure it?
- Does this make divergences easier to express, or does it allow them to be hidden?

**On ownership:**
- Does this preserve the entity's control over their own representation?
- Could an entity leave any implementing platform and take their representation with them?
- Does this create a new dependency on a central authority?

**On scope:**
- Does this belong in the protocol, or in an application built on top of it?
- Does this encode the assumptions of a specific domain or use case?
- Would this limit CARP's applicability to domains its authors did not anticipate?

**On architecture:**
- Does this introduce centralization that could become capture?
- Does this create data aggregation that could become surveillance?
- Does this produce outputs without uncertainty quantification?

**On governance:**
- Does this concentrate control in any single implementing organization?
- Is this compatible with open, independent governance?
- Would this change be accepted if proposed by an organization with no commercial interest in the outcome?

---

*A proposal that increases transparency, preserves entity ownership, encodes uncertainty honestly, avoids centralization, and belongs in the protocol layer rather than an application layer is almost certainly aligned with the spirit of CARP.*

*A proposal that does the opposite — however technically elegant, however commercially attractive, however well-intentioned — is not.*

*The protocol is designed around epistemic transparency rather than certainty. Every future decision should be made in that spirit.*

---

*End of CARP Design Principles*
