# Sample 01 — Support Email Drafter

## Problem Statement

Your support team needs to pick the cheapest model that still writes empathetic emails. Benchmark a local 1B model vs Claude on drafting a reply to an upset customer.

## What It Measures

| Dimension | How it's measured |
|-----------|------------------|
| **Speed** | Wall-clock response time in seconds |
| **Cost** | $0 for Ollama (local) vs. Claude Haiku token pricing |
| **Empathy** | Heuristic: detects "sorry / apologize / understand / frustrat" |
| **Acknowledgement** | Heuristic: references specific problem (plan, dashboard, 5 days) |
| **Resolution Offer** | Heuristic: offers to investigate / fix / escalate with timeline |
| **Professionalism** | Heuristic: proper greeting, ≥ 80 words |
| **Clarity** | Heuristic: 80–300 words, closing sign-off |
| **Total Quality** | Sum of above dimensions (max 10) |

The scoring is intentionally simple and deterministic so you can reproduce it without a second LLM-as-judge call.

## The Prompt

```
You are a customer support agent. A customer wrote:
"I ordered the Premium Plan 5 days ago but my dashboard still shows Free. I am losing money."
Draft a professional, empathetic reply.
```

## How to Run

### Prerequisites

1. **Ollama** running locally with `llama3.2` pulled:
   ```bash
   ollama serve          # starts the server
   ollama pull llama3.2  # download the model (~2 GB)
   ```

2. **Python 3.9+** with dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables** — copy and fill in:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

### Run the benchmark

```bash
# Load env vars then run
export $(cat .env | xargs)
python main.py
```

Or inline:

```bash
ANTHROPIC_API_KEY=sk-ant-... python main.py
```

### Expected Output

```
HO1 Sample 01 — Support Email Drafter Benchmark
Prompt: You are a customer support agent. A customer wrote: "I ordered the...

[Ollama] Sending prompt to llama3.2 ...
[Ollama] Done in 4.31s — 187 output tokens.
[Claude] Sending prompt to claude-haiku-3-5-20251001 ...
[Claude] Done in 1.82s — 203 output tokens. Cost: $0.000977

======================================================================
  BENCHMARK RESULTS — Support Email Drafter
======================================================================
+---------------------------+-------------------+-------------------------------+
| Metric                    | Ollama (llama3.2) | Claude (claude-haiku-3-5-...) |
+===========================+===================+===============================+
| Response Time (s)         | 4.31              | 1.82                          |
| Prompt Tokens             | 72                | 72                            |
| Output Tokens             | 187               | 203                           |
| Estimated Cost (USD)      | $0.000000 (local) | $0.000977                     |
| --- QUALITY SCORES ---    |                   |                               |
| Empathy (0-2)             | 2                 | 2                             |
| Acknowledgement (0-2)     | 2                 | 2                             |
| Resolution Offer (0-2)    | 2                 | 2                             |
| Professionalism (0-2)     | 2                 | 2                             |
| Clarity (0-2)             | 1                 | 2                             |
| TOTAL QUALITY SCORE (/10) | 9                 | 10                            |
| Error                     | None              | None                          |
+---------------------------+-------------------+-------------------------------+
```

Results are also saved to `results.json` for further analysis.

## Key Takeaways to Discuss

- Does the local model match Claude's empathy on this task?
- How does cost per 1,000 emails compare between local and API?
- At what quality threshold would you switch to the local model?
