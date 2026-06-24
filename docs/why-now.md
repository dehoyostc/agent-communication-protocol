# Why ACP, Why Now

## The gap this document addresses

AI systems can now reason, search, summarize, generate, plan, and act. The intelligence problem is not solved, but it is advancing rapidly. What is not advancing at the same pace is the infrastructure that allows AI agents to represent humans and organizations to each other — safely, consistently, with preserved privacy and explicit authorization boundaries.

This document argues that this gap is real, that it will become increasingly consequential as AI agents grow more autonomous, and that addressing it requires purpose-built infrastructure rather than an extension of existing tools.

---

## 1. Why existing language models are not sufficient

The most common objection to ACP is also the most reasonable one: modern language models are already capable of summarizing a person, analyzing a job description, and reasoning about compatibility. Why does a protocol need to exist at all?

The objection conflates two different problems.

The first problem is intelligence — the ability to reason about information, draw inferences, and generate useful outputs. Language models solve this problem, and they are getting better at it quickly.

The second problem is representation and exchange — the ability to define a shared, interoperable format in which agents communicate about entities, with explicit provenance, confidence levels, authorization boundaries, and privacy constraints. This is not an intelligence problem. It is an infrastructure problem.

Consider the analogy to email. A language model can help you write an email. It cannot define SMTP. These are different layers of the stack. SMTP does not care how intelligent the email author is. It defines how messages are formatted, transmitted, and routed so that systems built by different organizations, running different software, can communicate reliably.

ACP is attempting to define an equivalent layer for agent-to-agent communication about entities. The intelligence that generates a profile, evaluates a claim, or produces a compatibility signal lives in the model layer. The format in which those outputs are structured, the rules governing what can be disclosed and to whom, and the metadata that makes claims legible across systems — that lives in the protocol layer.

A language model left to its own devices will represent a person however seems most natural given its training and the prompt it received. Two different models representing the same person will produce incompatible outputs. Neither output will carry explicit confidence scores, provenance labels, or authorization constraints. Neither model will have a principled basis for refusing to disclose information that should not be shared.

The problem is not that models are unintelligent. The problem is that intelligence without structure does not produce interoperability, and interoperability is what the emerging multi-agent ecosystem requires.

---

## 2. Why MCP is not sufficient, and why that is not a criticism

The Model Context Protocol (MCP) solves a real and important problem: it allows AI agents to connect to external tools and data sources through a standardized interface. An agent that can query a database, read a document, or call an API through MCP is significantly more capable than one that cannot.

ACP addresses a different problem, and the distinction is worth being precise about.

MCP answers the question: *how does an agent access a tool or resource?*

ACP answers the question: *how does an agent represent an entity to another agent, and what is it authorized to disclose?*

An agent using MCP to access LinkedIn can retrieve a person's public profile. What MCP does not define is how that agent should represent what it knows about the person — including information that goes well beyond the public profile — to another agent acting on behalf of an employer, while preserving the person's privacy, honoring their disclosure preferences, and making the epistemic status of each claim explicit.

A concrete illustration: imagine an agent that has worked with a person daily for two years. It has observed their communication patterns, the environments in which they do their best work, the kinds of problems that energize them, and the organizational dynamics that have historically caused them to disengage. None of this appears on LinkedIn. None of it is accessible via MCP. And even if it were, the question of what the agent is authorized to share with a prospective employer's agent — and in what form, with what confidence labels, and under what disclosure constraints — is entirely outside MCP's scope.

MCP and ACP are complementary. An agent might use MCP to gather information about a person or organization from external sources, and ACP to represent and exchange that information with another agent in a structured, privacy-preserving way.

---

## 3. What changes when agents mediate interactions

For most of the internet's history, the interaction pattern has been:

```
Human → Website → Human
```

A person visits a website, fills out a form, reads a page, or sends a message. The website is a passive medium. It does not have opinions about the person. It does not have internal knowledge that it is choosing to withhold. It does not act on the person's behalf.

Increasingly, the interaction pattern is becoming:

```
Human → Agent → Agent → Human
```

A person's agent acts on their behalf. An organization's agent acts on its behalf. The two agents interact, exchange information, make assessments, and surface results to the humans they represent.

This transition creates requirements that did not exist in the previous model.

In a human-to-website interaction, the website receives exactly what the person types into the form. There is no ambiguity about the provenance of the information — the person provided it. There is no question about what the website knows beyond what was submitted — nothing.

In an agent-to-agent interaction, both sides may possess extensive contextual knowledge derived from observation over time. The provenance of that knowledge is varied — some of it was directly provided, some was inferred, some was observed behaviorally, some was derived from outcomes. The confidence in different claims varies significantly. And crucially, neither agent should share everything it knows with the other.

Current AI systems were designed for humans talking to software. They were not designed for agents talking to agents. The concepts of authorization scope, purpose binding, provenance labeling, confidence weighting, and selective disclosure are not native to these systems. They are added, when they are added at all, through application-level logic that is not standardized, not interoperable, and not auditable.

As agents become more capable and more autonomous, the consequences of this gap grow larger. An agent that discloses more than it should can cause real harm to the person it represents. An agent that discloses less than it should can cause the interactions it mediates to fail in ways that are opaque to all parties. An agent that discloses information without provenance metadata can cause downstream systems to make decisions on claims they cannot evaluate.

These are not hypothetical concerns. They are structural properties of a world in which agents act on behalf of people, and they will manifest in proportion to how capable and autonomous those agents become.

---

## 4. Why privacy becomes more important, not less

A reasonable intuition is that AI agents will make privacy less relevant by making information more fluid and accessible. The opposite is more likely to be true.

The more an agent knows about a person, the more important it becomes to have principled constraints on what it discloses and to whom. This is not primarily a legal or regulatory point, though legal and regulatory requirements will follow. It is a structural point about how information-dense representation creates information-dense risk.

Consider a personal AI agent that has observed a person's professional behavior for three years. It knows not only what roles they have held and what skills they claim, but which environments have produced their best work, which management styles have caused them to disengage, what compensation they consider a survival floor and why, what personal challenges they are navigating, and how their self-perception diverges from their observable behavior.

This is vastly richer than any resume, LinkedIn profile, or reference letter. It is also vastly more sensitive. The question of what this agent is authorized to share with a prospective employer's agent — and under what constraints, for what purpose, with what expiry — is not a question that can be answered by asking the agent to "be careful."

The same dynamic applies across domains. A healthcare agent that knows a patient's full medical history, treatment preferences, medication sensitivities, and behavioral health context is more useful precisely because it knows more. But the disclosure rules for that agent interacting with an insurance agent, a specialist agent, or a family member's agent must be explicit, granular, and auditable in ways that current systems do not support.

An investment agent that knows an individual's full financial picture — income, obligations, risk tolerance, behavioral patterns in volatile markets, life circumstances affecting financial decisions — faces the same challenge when interacting with an advisor agent or an institutional agent.

The pattern is consistent: the more capable the agent, the richer its knowledge, the higher the stakes of uncontrolled disclosure. Privacy-preserving compatibility discovery is not a feature to be bolted onto agents. It is a foundational requirement of a world in which agents know enough to be genuinely useful.

---

## 5. A motivating scenario

Suppose a person — call them the candidate — has been using an AI assistant for two years. The assistant has developed a detailed model of how this person works: the environments in which they produce their best output, the management styles that cause them to disengage, their primary motivators and frustrations, their communication preferences, and the gap between how they describe themselves and how they actually behave.

Now suppose a company has an internal AI system that has similarly developed a model of the organization: what kinds of people have historically thrived there, what the role actually demands versus what the job description says, the meeting load, the decision-making structure, the cultural dynamics that are visible to someone embedded in the organization but invisible in any public artifact.

These two agents could, in principle, exchange information in a way that produces a compatibility signal far richer than any comparison of resume to job description. The candidate agent knows things about the person that no interviewer would learn in four rounds of interviews. The company agent knows things about the environment that no job posting would reveal.

But this exchange cannot happen safely without a protocol that defines what each agent is authorized to disclose, in what form, for what purpose, with what confidence metadata, and under what constraints. Without such a protocol, the exchange either does not happen at all, or it happens in an unstructured way that exposes information neither party intended to share.

The candidate agent should not disclose the person's health context, their financial situation, their reasons for leaving previous roles, or their private assessments of past managers. The company agent should not disclose internal conflict, employee performance data, unreleased strategic plans, or the compensation ceiling the hiring manager is willing to reach.

The compatibility signal — the useful output of this interaction — does not require any of this private information. It emerges from the intersection of what each agent is authorized to share: the operating patterns that predict success and failure on both sides, the structural requirements of the role and environment, the constraints that are hard limits versus soft preferences.

This is the problem ACP is designed to address. Not the intelligence required to generate a compatibility signal. The infrastructure required to exchange information safely, with explicit authorization boundaries, in a format that is consistent across agents built by different organizations using different underlying models.

---

## 6. Why the solution must be an open protocol

The preceding sections establish that a gap exists. A reasonable response is: why can't a single AI company close it? OpenAI, Anthropic, Google, and Microsoft each have the engineering capacity to define an internal representation format for agents, build authorization and disclosure logic on top of it, and ship it as a feature of their own platforms.

The answer is that a proprietary solution to this problem is not a solution to this problem. It is a reproduction of the problem at a higher level of abstraction.

Consider what a proprietary approach produces. A user's personal agent is built on one platform. Their employer's HR agent is built on another. Their healthcare provider's agent runs on a third. Their financial advisor's firm uses a fourth. Each platform has defined its own internal representation format, its own disclosure rules, its own confidence metadata schema — or more likely, has not defined any of these things explicitly at all.

When these agents need to interact — and in an agent-first world, they will need to interact — they face the same interoperability problem that existed before email standards, before HTTP, before TCP/IP. Each organization built its own messaging system, its own document format, its own network protocol. Value was locked inside ecosystems. Communication across boundaries was difficult, expensive, and unreliable.

The internet became valuable not because one company built the best proprietary network, but because open standards made it possible for systems built by different organizations, using different architectures, to communicate reliably. The email you send from Gmail reaches an Outlook inbox because SMTP and IMAP are open standards, not because Google and Microsoft agreed to a bilateral data-sharing arrangement.

Agent ecosystems will follow the same dynamic. The value of a personal AI agent grows with the number of institutional agents it can interact with on its owner's behalf. The value of an organizational agent grows with the number of personal agents it can engage. That value is only realized if agents can communicate across organizational boundaries — which requires shared standards that no single organization controls.

There is a second reason proprietary solutions are insufficient, and it is specific to this problem domain. ACP is infrastructure for representing humans. The entity whose interests the protocol is designed to protect is the person being represented, not the platform doing the representing. A protocol owned by the platform that profits from agent interactions has a structural conflict of interest that is difficult to resolve through policy alone.

An open standard for agent-to-agent communication about humans can be designed with the person's interests as the primary constraint. A proprietary feature of a commercial platform will always be subject to the commercial incentives of the platform that owns it. This is not a criticism of any particular company. It is a structural observation about incentive alignment.

The argument for an open protocol is not ideological. It is the same argument that justified open standards for email, the web, and identity federation: the aggregate value of interoperability exceeds the value any single actor could capture by keeping the standard proprietary, and the entities whose interests are most at stake — in this case, the humans being represented — are better served by infrastructure they do not depend on any single organization to maintain.

---

## 7. Why now

In 2015, this problem did not exist in any practical sense. AI assistants were not capable of developing rich models of their users. The concept of an agent acting autonomously on a person's behalf was largely theoretical.

In 2020, the problem was emerging but not yet pressing. Language models had become capable enough to be genuinely useful, but agentic behavior — the ability to take sequences of actions, call external tools, maintain context over time, and act autonomously on behalf of a user — was limited.

In 2025 and beyond, the situation has changed materially. Agents are now capable of sustained autonomous action. Multi-agent frameworks are in active production use. Personal AI assistants are accumulating months and years of interaction history with individual users. Organizational AI systems are being embedded into operations, HR, product development, and strategy.

The infrastructure question — how do these agents represent the entities they serve, and how do they exchange that representation with other agents — is no longer hypothetical. It is being answered, by default, through ad hoc application logic that is not interoperable, not auditable, and not designed to handle the privacy and authorization requirements that the problem demands.

The absence of a standard in a nascent ecosystem is normal. Standards emerge when the cost of their absence becomes visible. That cost is not yet obvious to most practitioners, because the most capable multi-agent interactions are still being built by single organizations that control both agents and can therefore set informal conventions without a formal protocol.

As the ecosystem matures — as personal agents built by different organizations need to interact with institutional agents built by others, as individuals expect their agent to represent them across contexts they do not control, as regulatory pressure around AI and privacy increases — the absence of a standard will become increasingly costly.

ACP is an attempt to define that standard before the ecosystem calcifies around incompatible conventions. Whether this particular proposal becomes the foundation for a widely adopted standard is uncertain. What is less uncertain is that some version of this problem will need to be solved, and that the decisions made early in the development of agent-to-agent communication infrastructure will be difficult to reverse.

---

## What ACP does not claim

ACP does not claim to solve the intelligence problem. It does not claim to be a complete specification of all the infrastructure that agent-to-agent communication will eventually require. It does not claim that its current design is optimal or that its primitives will not need significant revision.

It claims that a gap exists between the intelligence capabilities of current AI systems and the infrastructure required to deploy those systems safely in multi-agent contexts involving sensitive information about real people and organizations. It claims that this gap is structural — not addressable by making models smarter — and that addressing it requires purpose-built, interoperable, open infrastructure.

The goal of this document is not to convince the reader that ACP is the answer. It is to make the case that the question is real.

---

*ACP v0.1 · [github.com/TBD/agent-communication-protocol](https://github.com)*
