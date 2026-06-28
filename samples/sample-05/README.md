# HO1 Sample 5 — Email Drafting

## What you'll build
A side-by-side test of first-draft email quality. You give the **same** customer email to a free local model (in LM Studio) and to **Claude.ai**, then score which one drafted the reply you'd be happiest to send with the fewest edits.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **LM Studio** and load any small model (e.g. Llama 3.2). Paste the example prompt below into its chat. Copy the reply.
2. Open **Claude.ai** (your subscription). Paste the **same** prompt. Copy Claude's reply.
3. Open **`index.html`** from this folder in your browser. Paste both replies in and score each using the rubric.
4. Decide which draft needs the least editing before you'd actually send it.

## The example prompt
Copy this exactly into both LM Studio and Claude.ai:

```
You are a customer support agent for an online electronics store. Read the customer's email below and draft a warm, professional reply that acknowledges the problem, gives a clear next step, and sets a realistic expectation. Keep it under 150 words.

Customer email:
"Hi, I ordered a wireless keyboard (order #ORD-5582) last Tuesday and it still hasn't arrived. The tracking page hasn't updated in three days. I need it for work — can you tell me where it is and when I'll get it?"
```

## Scoring rubric
| Criterion | Scale |
|-----------|-------|
| Correct solution proposed | yes / no |
| Tone matches brand | 1–5 |
| Reply length appropriate | 1–5 |
| Needs major edits | yes / no |

## Make it your own
- Swap in a real (anonymised) customer email you get often.
- Paste a couple of your best past replies first so the model copies your voice.
- Add a rule like 'always offer a discount code if delivery is late'.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run the comparison
automatically, `main.py` shows how. It needs an Anthropic API key, which is separate from
your Claude.ai subscription — so it costs money and is not part of the hands-on.
