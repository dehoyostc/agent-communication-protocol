# AF-004-empty-assessed-categories: Empty assessed_categories must generate scope warnings

A document-like profile declares assessed_categories: []. This must be treated as unassessed critical scope, not as clean absence.

## Expected Result

```json
{
  "classification": "insufficient_data",
  "must_have_scope_warning_count_at_least": 3,
  "must_include_scope_gap_reason": "not_declared_assessed"
}
```
