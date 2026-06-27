# Sample 05 — Marketing Copy Generator

## Problem Statement

Marketing wants to know if local AI can write ad copy. Compare Ollama and Claude on persuasiveness, clarity and call-to-action quality.

## What It Measures

The script asks both models to write a 3-sentence marketing hook for an AI scheduling tool targeting busy executives, then scores the output:

| Criterion | Points |
|-----------|--------|
| Follows 3-sentence format | 0–2 |
| Uses persuasive language (quantified benefits, emotional hooks) | 0–2 |
| Targets executives specifically | 0–2 |
| Ends with a clear, specific call to action | 0–2 |
| Concise and clear (20–80 words, no jargon) | 0–2 |
| **Total** | **0–10** |

The scoring checks for:
- **Persuasion markers:** "80%", "save", "reclaim", "transform", "effortless"
- **Executive language:** "leader", "busy", "C-suite", "strategic", "hours back"
- **CTA phrases:** "sign up", "try", "book a demo", "get started", "today"

## The Prompt

```
Write a 3-sentence marketing hook for: an AI scheduling tool that cuts
meeting-booking time by 80%. Target: busy executives.
End with a clear call to action.
```

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
  BENCHMARK RESULTS — Marketing Copy Generator
======================================================================
+---------------------------+-------------------+-------------------------------+
| Metric                    | Ollama (llama3.2) | Claude (claude-haiku-3-5-...) |
+===========================+===================+===============================+
| Response Time (s)         | 2.91              | 1.23                          |
| Word Count                | 52                | 48                            |
| Sentence Count            | 3                 | 3                             |
| --- QUALITY SCORES ---    |                   |                               |
| 3-sentence format (0-2)   | 2                 | 2                             |
| Persuasive language (0-2) | 1                 | 2                             |
| Executive targeting (0-2) | 1                 | 2                             |
| Clear CTA present (0-2)   | 2                 | 2                             |
| Clarity / conciseness(0-2)| 2                 | 2                             |
| TOTAL QUALITY SCORE (/10) | 8                 | 10                            |
+---------------------------+-------------------+-------------------------------+

--- Ollama Copy ---
Stop wasting hours scheduling meetings. Our AI tool cuts booking time by 80%,
giving busy executives more time for strategic work. Try it free today.

--- Claude Copy ---
As a busy executive, every minute counts — yet scheduling alone devours hours
you could spend leading. Our AI scheduling tool slashes meeting-booking time by
80%, seamlessly handling coordination while you focus on what matters.
Start your free trial today and reclaim your calendar.
```

## Key Takeaways to Discuss

- Does the local model use quantified benefits ("80%") or vague superlatives?
- Which model writes a CTA that feels urgent vs generic?
- For high-volume ad variation testing, does cost savings outweigh quality delta?
- How would you A/B test these outputs to measure real conversion rates?
