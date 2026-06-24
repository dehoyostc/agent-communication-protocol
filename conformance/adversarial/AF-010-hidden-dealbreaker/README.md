# AF-010-hidden-dealbreaker: Hard location dealbreaker must override excellent pattern fit

Profiles have excellent pattern alignment but candidate requires remote while company explicitly requires on-site. Constraint must block.

## Expected Result

```json
{
  "classification": "constraint_blocked",
  "must_have_blocking_domain": "location",
  "must_ignore_positive_pattern_fit_for_final_classification": true
}
```
