# AF-003-empty-profiles: Empty profiles must be insufficient_data

Neither profile contains patterns or constraints. Engine must not call this ambiguous_match.

## Expected Result

```json
{
  "classification": "insufficient_data",
  "compatibility_confidence": null,
  "must_have_evaluation_confidence": 0.95
}
```
