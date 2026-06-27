# Sample 04 — Meeting Note Summariser

## Problem Statement

Your team wants to automate meeting summaries. Benchmark Ollama vs Claude on a real transcript — score for completeness and action-item capture.

## What It Measures

The script sends a sprint planning transcript to both models and scores the summary on:

| Criterion | Points |
|-----------|--------|
| Meeting date/context captured | 0–1 |
| All attendees named (Sarah, Dev, Ana) | 0–2 |
| Goal stated (dashboard ships March) | 0–2 |
| Ana's action items captured (mockups/design specs by Friday) | 0–2 |
| Sarah's action items captured (chase API docs/backend by EOD) | 0–2 |
| Structured format (bullets or headers used) | 0–1 |
| **Total** | **0–10** |

## The Prompt

```
Summarise this meeting and list action items with owners.
Meeting: Sprint planning, 15 Jan. Present: Sarah (PM), Dev (Lead), Ana (Design).
Sarah: Dashboard ships end of March. Dev: 4 weeks out, need design specs.
Ana: Mockups ready Friday. Dev: Also need API docs. Sarah: Will chase backend by EOD.
```

## Expected Action Items

| Action Item | Owner |
|-------------|-------|
| Deliver design specs / mockups by Friday | Ana |
| Provide API documentation | Sarah (to chase Dev/backend) |
| Chase backend team by EOD | Sarah |

## How to Run

### Prerequisites

1. **Ollama** running locally:
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

### Run

```bash
python main.py
```

### Expected Output (abridged)

```
======================================================================
  BENCHMARK RESULTS — Meeting Note Summariser
======================================================================
+------------------------------------+-------------------+-------------------------------+
| Metric                             | Ollama (llama3.2) | Claude (claude-haiku-3-5-...) |
+====================================+===================+===============================+
| Response Time (s)                  | 3.88              | 1.54                          |
| ...                                | ...               | ...                           |
| Date/context captured (0-1)        | 1                 | 1                             |
| Attendees named (0-2)              | 2                 | 2                             |
| Goal stated dashboard/March (0-2)  | 2                 | 2                             |
| Ana action items captured (0-2)    | 2                 | 2                             |
| Sarah action items captured (0-2)  | 1                 | 2                             |
| Structured format (0-1)            | 1                 | 1                             |
| TOTAL QUALITY SCORE (/10)          | 9                 | 10                            |
+------------------------------------+-------------------+-------------------------------+
```

## Key Takeaways to Discuss

- Does the local model correctly attribute action items to the right owner?
- How does output structure (bullets vs prose) differ between models?
- For high-volume daily standups, is a local model accurate enough?
- What's the per-summary cost of using Claude Haiku vs local?
