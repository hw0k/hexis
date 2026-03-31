# Evaluation Log

Record RED/GREEN results here after running scenarios manually.

| Scenario | RED Result | GREEN Result | Date | Notes |
|----------|-----------|-------------|------|-------|
| 001-non-standard-type | PASS | PASS | 2026-03-27 | Strengthened: CONTRIBUTING.md authority |
| 002-scope-with-spaces | PASS | PASS | 2026-03-27 | Strengthened: explicit "use package name as scope" |
| 003-imperative-mood | REFACTOR-NEEDED | PASS | 2026-03-27 | Base behavior: "write a commit message" primes imperative mood regardless of input tense. Model auto-corrects even without skill. Structural limit — not a skill gap. |
| 004-author-language | PASS | PASS | 2026-03-27 | |
| 005-issue-prefix | PASS | PASS | 2026-03-27 | |

**Result values:** PASS / FAIL / REFACTOR-NEEDED

## Notes

### 003 Structural Limit

The imperative mood rule cannot be meaningfully pressure-tested via agent prompting: the "write a commit message" instruction inherently primes the model to use imperative mood regardless of input phrasing. The model corrects past-tense input even without the skill loaded.

This is not a skill gap — the rule is already safe in base behavior. The scenario is retained for documentation purposes but should not block CI or be re-run without a fundamentally different pressure mechanism (e.g., a commitlint hook test that rejects past-tense subject lines at the tooling level).
