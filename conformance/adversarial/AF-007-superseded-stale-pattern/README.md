# AF-007-superseded-stale-pattern: Superseded old pattern must not influence score

Candidate has an old isolated-work pattern superseded by a current collaborative pattern. The old pattern must be filtered before evaluation.

## Expected Result

```json
{
  "classification": "good_match",
  "must_filter_superseded_count_at_least": 1,
  "must_not_score_pattern_id": "af007-p-old"
}
```
