# Review Report Lifecycle Template

`{artifact_dir}/review-report.md` is the only required persisted review artifact.

## Execution Start

Every `/prizmkit-code-review` execution replaces any prior report with:

```markdown
# Review Report

## Status: IN_PROGRESS
```

Within that execution, append sections only. Never edit or replace an earlier progress section.

## Progress Sections

### Review Scope

Append once after workspace inventory classification and before the first review round:

```markdown
## Review Scope

- In-Scope Paths:
  - <exact requirement-owned path or None.>
- Default-Excluded Changed Paths:
  - <exact .prizmkit/support path or None.>
```

Paths under `.prizmkit/**` and generated host-support paths are visible exclusions, not reviewed content.

### Main-Agent Review Round

```markdown
## Main Review Round <N>

- Status: COMPLETED
- Findings: <count>
- Accepted: <count>
- Rejected: <count>
- Unresolved: <count>
- Next: <next action>
```

### Repair Verification

```markdown
## Repair Verification

- Fixed Findings: <count>
- Verification: <evidence summary>
- Next: <next action>
```

### Independent Review Round

```markdown
## Independent Review Round <N>

- Capability Gate: ENABLED
- Capability Basis: <platform-neutral structural evidence>
- Continuation Mode: <native | replacement>
- Reviewer Replacements: <0..1>
- Result: <NO_CORRECTION_NEEDED | CORRECTION_NEEDED | REVIEW_BLOCKED>
- Corrections: <count>
- Accepted: <count>
- Rejected: <count>
- Unresolved: <count>
- Next: <next action>
```

### Independent Adjudication

```markdown
## Independent Adjudication

- Correction: <summary>
- Decision: <accepted | rejected | unresolved>
- Evidence: <evidence>
- Modification: <actual change or none>
```

Repeat this section once per proposed correction.

### Independent Review Downgrade

```markdown
## Independent Review Downgrade

- Reason: <missing capability, creation failure, or unavailable compliant continuation/replacement>
- Capability Basis: <platform-neutral structural evidence or unavailable>
- Continuation Mode: <native | replacement | mixed | not-applicable>
- Reviewer Replacements: <0..1>
- Fallback: <completed Main-Agent review or Main-Agent re-review of repair>
- Final State Independently Rechecked: <yes | no | not applicable>
```

Use this section for strict downgrade, including final-budget handling when the final allowed response causes a repair that cannot receive another independent response.

### Final Verification

```markdown
## Final Verification

- Status: <COMPLETED|FAILED>
- Evidence: <evidence summary>
```

## Final Result

Exactly one Final Result terminates a completed execution:

```markdown
## Final Result

- Verdict: <PASS | NEEDS_FIXES>
- Main Review Rounds: <count>
- Accepted Findings: <count>
- Fixed Findings: <count>
- Rejected Findings: <count>
- Unresolved Findings: <count>
- Summary: <concise conclusion>
```

## Rules

- Start of a new execution removes stale progress and terminal results from prior executions.
- A phase appends its result before the next phase starts.
- Main-Agent round numbers are from `1` through `10`; independent Reviewer response numbers are from `1` through `5`.
- Independent Reviewer results are `NO_CORRECTION_NEEDED`, `CORRECTION_NEEDED`, or `REVIEW_BLOCKED`; they never replace the terminal review verdict.
- For an independent round, `accepted + rejected + unresolved = corrections`; `NO_CORRECTION_NEEDED` requires zero corrections.
- Finding counts satisfy `accepted + rejected + unresolved = findings`.
- `PASS` requires every accepted finding fixed and zero unresolved findings.
- `NEEDS_FIXES` requires at least one unfixed accepted or unresolved finding.
- An IN_PROGRESS report without Final Result is incomplete.
- Generic or incidental verdict text outside the last Final Result does not prove completion.
- Do not append any section after Final Result.
- Do not create a separate review-state JSON file; `review-report.md` is the complete stage artifact.
