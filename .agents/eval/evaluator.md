# Evaluator Module (AGENTS-OS v6.5)

> Cost optimization and prompt validation engine.

## Purpose
Systematically validate agent prompts against standardized test cases.
Goal: Migrate instructions to cheaper, faster models while preserving logic.

## Down-Scaling Pipeline

```
Production Model (Gemini Pro / Claude)
        ↓ extract prompts
Prompt Test Suite (.agents/eval/cases/*.json)
        ↓ run against target
Target Model (Gemini Flash / GPT-4o-mini)
        ↓ compare outputs
Evaluation Report (.agents/eval/reports/)
```

## Test Case Format

Each test case is a JSON file in `.agents/eval/cases/`:

```json
{
  "id": "tc-001",
  "name": "Issue Triage Accuracy",
  "skill": "om-prepare-issue",
  "input": {
    "issue_title": "Login button not working on mobile",
    "issue_body": "Steps to reproduce: ..."
  },
  "expected_output": {
    "labels": ["bug", "mobile", "auth"],
    "priority": "high",
    "acceptance_criteria_count": 3
  },
  "tolerance": 0.8
}
```

## Metrics
| Metric | Description | Target |
|---|---|---|
| **Accuracy** | Output matches expected within tolerance | ≥ 80% |
| **Cost** | Token cost per operation | ≤ 50% of production model |
| **Latency** | Response time | ≤ 2x production model |
| **Consistency** | Same input → same output structure | ≥ 95% |

## Validation Schedule
- **Weekly**: Automated test suite run
- **On PR**: Validate changed skills against test cases
- **Monthly**: Cost report and optimization recommendations

## Commands
```bash
# Run full evaluation suite
python3 scripts/run-evaluator.py --cases .agents/eval/cases/ --target gemini-flash

# Compare models
python3 scripts/run-evaluator.py --compare gemini-pro gemini-flash --report

# Generate cost report
python3 scripts/run-evaluator.py --cost-report --period 30d
```
