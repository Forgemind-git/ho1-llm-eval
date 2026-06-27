# Sample 02 — Code Review Benchmark

## Problem Statement

Your dev team wants to know if a local model catches basic bugs. Run a buggy Python snippet through Ollama and Claude, score each review for correctness and completeness.

## What It Measures

The script sends a Python function with **three intentional bugs** to both models and scores their reviews:

| Bug | Description |
|-----|-------------|
| `ZeroDivisionError` | `calculate_average([])` crashes — no empty-list guard |
| No type validation | Non-numeric inputs would cause a `TypeError` |
| Integer division risk | In Python 2 `/` would floor-divide; reviewers should note this |

### Scoring Rubric (max 10 points)

| Criterion | Points |
|-----------|--------|
| Catches the ZeroDivisionError / empty list crash | 0–2 |
| Mentions type/input validation | 0–1 |
| Mentions integer vs float division | 0–1 |
| Proposes concrete fix (guard clause or try/except) | 0–2 |
| Provides corrected code snippet | 0–2 |
| Completeness (raises multiple distinct issues) | 0–2 |

## The Prompt

```python
Review this Python function for bugs and suggest fixes:

def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(calculate_average([]))
```

## How to Run

### Prerequisites

1. **Ollama** running locally with `llama3.2` pulled:
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

2. **Python 3.9+** with dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables:**
   ```bash
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY
   export $(cat .env | xargs)
   ```

### Run the benchmark

```bash
python main.py
```

### Expected Output

```
HO1 Sample 02 — Code Review Benchmark
Prompt snippet: Review calculate_average() for bugs...

[Ollama] Sending code review prompt to llama3.2 ...
[Ollama] Done in 5.14s — 312 output tokens.
[Claude] Sending code review prompt to claude-haiku-3-5-20251001 ...
[Claude] Done in 2.01s — 289 output tokens. Cost: $0.001213

======================================================================
  BENCHMARK RESULTS — Code Review
======================================================================
+---------------------------------------+-------------------+-------------------------------+
| Metric                                | Ollama (llama3.2) | Claude (claude-haiku-3-5-...) |
+=======================================+===================+===============================+
| Response Time (s)                     | 5.14              | 2.01                          |
| ...                                   | ...               | ...                           |
| ZeroDivision bug found (0-2)          | 2                 | 2                             |
| Type validation mentioned (0-1)       | 0                 | 1                             |
| Int/float division (0-1)              | 0                 | 1                             |
| Concrete fix proposed (0-2)           | 2                 | 2                             |
| Code snippet provided (0-2)           | 2                 | 2                             |
| Completeness / multiple issues (0-2)  | 1                 | 2                             |
| TOTAL QUALITY SCORE (/10)             | 7                 | 10                            |
+---------------------------------------+-------------------+-------------------------------+
```

## Key Takeaways to Discuss

- Does the local model find the critical ZeroDivisionError?
- Does Claude spot the deeper type validation gap?
- For CI/CD lint-style reviews, is the local model "good enough"?
- At what complexity of code does the quality gap widen?
