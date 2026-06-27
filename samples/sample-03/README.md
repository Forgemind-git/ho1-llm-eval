# Sample 03 — Structured Data Extraction

## Problem Statement

Ops needs to extract JSON from freeform text reliably. Compare a local model and Claude on accuracy of field extraction.

## What It Measures

The script asks both models to extract 4 fields from a customer support message and scores against known ground-truth values:

| Field | Ground Truth |
|-------|-------------|
| `customer_name` | Maria |
| `order_id` | ORD-2847 |
| `issue` | three items missing |
| `urgency_level` | high (client event tomorrow morning) |

### Scoring Rubric (max 10 points)

| Criterion | Points |
|-----------|--------|
| Produces valid, parseable JSON | 0–2 |
| `customer_name` matches "Maria" | 0–2 |
| `order_id` matches "ORD-2847" | 0–2 |
| `issue` contains "missing" and "items" | 0–2 |
| `urgency_level` is "high" (correct inference) | 0–2 |

The urgency field requires **inference** — the text says "client event tomorrow morning" not "urgent". This tests how well each model reasons about implicit signals.

## The Prompt

```
Extract these fields as JSON: customer_name, order_id, issue, urgency_level (low/medium/high).
Text: "Hi, I am Maria. Order #ORD-2847 arrived yesterday but three items are missing.
I have a client event tomorrow morning."
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
HO1 Sample 03 — Structured Data Extraction Benchmark
...

--- Ground Truth ---
{
  "customer_name": "Maria",
  "order_id": "ORD-2847",
  "issue": "three items missing from order",
  "urgency_level": "high"
}

--- Ollama Parsed JSON ---
{
  "customer_name": "Maria",
  "order_id": "ORD-2847",
  "issue": "Three items missing",
  "urgency_level": "high"
}

--- Claude Parsed JSON ---
{
  "customer_name": "Maria",
  "order_id": "ORD-2847",
  "issue": "Three items missing from order",
  "urgency_level": "high"
}
```

## Key Takeaways to Discuss

- Does the local model produce valid JSON reliably, or does it add prose around it?
- Which model correctly infers `urgency_level = high` from context clues?
- For high-volume ETL pipelines, what accuracy threshold is acceptable?
- How would you validate extraction at scale without manual review?
