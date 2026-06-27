# Release Notes

## v0.2.3-alpha (current)

**Status:** Alpha. Not production-ready. Interfaces and object definitions may change.

### What's in this release

- CARP v0.2 specification (`specs/CARP-v0.2.md`)
- Exchange engine v0.2.3 with full conformance suite runner
- 9 JSON schemas covering all core CARP objects
- 13 adversarial fixtures (AF-001 through AF-013)
- 5 conformance example outputs across named fixture pairs
- Profile recovery report demo (`demos/profile-recovery-report.html`)

### Engine changes in v0.2.3

- Added `MAX_POSITIVE_TAG_GROUP_DELTA` capping to prevent duplicate low-evidence pattern stuffing from inflating compatibility scores (resolves AF-009)
- Orphaned divergence reference detection (AF-011)
- Relationship depth spoofing resistance (AF-012)
- Clock manipulation and selective expiry detection (AF-013)
- Confidence now reflects pattern evidence quality and stability, not raw score

### Known issues

- AF-009 pattern-stuffing check: the capping logic is active and producing correct results in v0.2.3 (`ambiguous_match`). Prior v0.2.2 results in `observed_engine_v022_results.json` show the unfixed behavior for reference.
- Conformance suite schemas are v0.2.2; will be updated to v0.2.3 schemas in the next release.
- `NEGATION_TAGS` semantic opposition table is engine-local and should be promoted to a documented ontology before independent conformance claims.
- L2 (Authentication) and L3 (Trust & Authorization) layers are not yet defined. See `docs/architecture-overview.md`.

## v0.2.2-alpha

- Initial conformance suite with fixtures for Jordan/Vessel, Priya/Fieldstone, Sam/Arclight, Marcus/Vantage, River/Arclight
- Pattern comparison engine with tag-group scoring
- Constraint evaluation layer

## v0.1

- Initial CARP specification draft
- Basic claim, profile, divergence, and disclosure primitives
- CARP simulation demonstrating agent-to-agent exchange
