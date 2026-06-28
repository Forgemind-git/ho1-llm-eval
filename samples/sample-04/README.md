# HO1 Sample 4 — Document Redaction

## Your task

Your clinic must keep patient data on-premises. Run 20 sensitive documents through a local model and Claude for PII redaction, then score recall and precision of what was redacted.

## What to do

1. Copy the test prompt below into **LM Studio** (local model) — note the output
2. Copy the same prompt into **Claude.ai** — note the output
3. Score both using the rubric below
4. Open index.html in your browser to fill in your scores interactively

## Test prompt

```
[TODO: write your test prompt here — what will you give to both models?]
```

## Scoring rubric

| Criterion | Scale |
|-----------|-------|
| All names redacted | yes / no |
| All dates redacted | yes / no |
| Medical terms preserved (not over-redacted) | yes / no |
| False positives count | 0 / 1–2 / 3+ |
