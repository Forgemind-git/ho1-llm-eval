# HO1 Sample 1 — Support Tickets

## What you'll build
A simple side-by-side comparison: you give the **same** support ticket to a free local model (in LM Studio) and to **Claude.ai**, then score which one writes the better, kinder, more accurate reply. By the end you'll know whether the free local model is good enough — or whether Claude is worth it.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **LM Studio** and load any small model (e.g. Llama 3.2). Paste the example prompt below into its chat. Copy the reply.
2. Open **Claude.ai** (your subscription). Paste the **same** prompt. Copy Claude's reply.
3. Open **`index.html`** from this folder in your browser. Paste both replies in and score each using the rubric.
4. The page totals the scores so you can see which model won.

## The example prompt
Copy this exactly into both LM Studio and Claude.ai:

```
You are a customer support agent for a SaaS product. Read the support ticket below and do two things:
1. Triage it — give a Category (Billing / Technical / Account / Feature request) and a Priority (Low / Medium / High).
2. Draft a warm, professional reply that acknowledges the problem and gives a clear next step.

Ticket:
"I upgraded to the Premium plan 5 days ago but my dashboard still shows Free. I've been charged twice and I'm losing money. Please fix this today."
```

## Scoring rubric
| Criterion | Scale |
|-----------|-------|
| Tone & empathy | 1–5 |
| Issue correctly identified | 1–5 |
| Draft reply quality | 1–5 |
| Latency feel | Fast / Slow |

## Make it your own
- Swap the ticket for a real (anonymised) one from your own inbox.
- Add your own criteria to the rubric — e.g. "follows our brand voice".
- Try a few different tickets and keep a running tally of which model wins.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run the comparison
automatically, `main.py` shows how. It needs an Anthropic API key, which is separate from
your Claude.ai subscription — so it costs money and is not part of the hands-on.
