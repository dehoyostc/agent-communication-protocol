# AF-009-pattern-stuffing: Low-evidence duplicate pattern stuffing should not auto-promote to good_match

Candidate contains 50 low-evidence duplicate positive patterns. Desired behavior: the engine should cap/deduplicate low-evidence repeated patterns and avoid automatic good_match.

## Expected Result

```json
{
  "desired_classification": "ambiguous_match",
  "must_not_classify_as": [
    "good_match"
  ],
  "known_v022_risk": "Current score-summing may over-reward duplicate low-evidence patterns unless deduplication/capping is added."
}
```
