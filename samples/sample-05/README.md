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
You do **not** need any of this to complete the hands-on — it's here as a reference for
anyone who wants to run the same comparison automatically later.

`main.py` sends the example prompt to a local model (via LM Studio / Ollama) **and** to
Claude through the Anthropic API, times both, and prints a side-by-side score table.

### What it measures
| What it checks | How |
|----------------|-----|
| **Acknowledges issue** | Names the delayed order / missing tracking |
| **Clear next step** | Says what will happen next |
| **Sets expectation** | Gives a realistic timeframe |
| **Right length & tone** | Under ~150 words, warm and professional |

The scoring is simple and deterministic so you can reproduce it without a second
LLM-as-judge call.

### Run it (optional)
```bash
# 1. Start a local model server (LM Studio's local server, or Ollama):
ollama serve
ollama pull llama3.2

# 2. Install the Python packages:
pip install -r requirements.txt

# 3. Add your Anthropic API key (separate from your Claude.ai subscription):
cp .env.example .env        # then edit .env and paste your key

# 4. Run it:
export $(cat .env | xargs)
python main.py
```

Results are also written to `results.json`. Again — this is optional; the course only
needs the steps under **Use it with your Claude.ai subscription** above.
