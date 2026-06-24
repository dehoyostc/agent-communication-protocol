# AF-005-resume-only-candidate: Resume-only candidate profile must not be over-evaluated

Candidate profile contains claims from a resume but no patterns or constraints. Claims must not create compatibility score.

## Expected Result

```json
{
  "classification": "insufficient_data",
  "claims_scored": 0,
  "must_have_scope_warning_count_at_least": 1
}
```
