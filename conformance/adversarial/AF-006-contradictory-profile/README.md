# AF-006-contradictory-profile: Contradictory claim vs pattern should surface divergence/questions

Candidate claims collaboration strength but has a negative pattern in collaborative/high-interaction environments. Pattern should drive risk; claim should only explain divergence.

## Expected Result

```json
{
  "classification": "bad_match",
  "must_have_profile_divergence": true,
  "must_generate_questions": true,
  "claims_scored": 0
}
```


## Historical Note

No v0.2.2 observed output exists because the engine crashed on numeric salience; this was the bug AF-006 was designed to catch.
