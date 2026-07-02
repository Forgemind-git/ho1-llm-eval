# HO1 Sample 05 — Email Drafting

## What you'll build
A side-by-side test of two **local** models drafting a first reply. You give the **same** customer email to both models in LM Studio, then rate each draft on tone and accuracy, note tokens/sec and size, and decide which local model gives the best quality for the compute it needs.

## Run it in LM Studio (two local models)
**100% offline. No API key, no cloud, no Claude.** Everything runs on your own machine.

1. Open **LM Studio** and download **two** local models to compare — e.g. **Llama 3.2 1B** and **Qwen 2.5 3B** (or two quant levels of one model).
2. Load **Model A**, paste the example prompt below into its chat, and run it. Copy the reply. Note the **tokens/sec** LM Studio shows and the model's **size (GB)** and **RAM** use.
3. Load **Model B** and do exactly the same with the **same** prompt.
4. Open **`index.html`** from this folder in your browser. Paste both replies in, score each with the rubric, and type in the tokens/sec, size and RAM you noted.
5. The page builds a comparison table and lets you download it. Then fill in **`RECOMMENDATION.md`** naming which local model to run and why.

## The example prompt
Copy this exactly into **both** models so the comparison is fair:

```
You are a customer support agent for an online electronics store. Read the customer's email below and draft a warm, professional reply that acknowledges the problem, gives a clear next step, and sets a realistic expectation. Keep it under 150 words.

Customer email:
"Hi, I ordered a wireless keyboard (order #ORD-5582) last Tuesday and it still hasn't arrived. The tracking page hasn't updated in three days. I need it for work — can you tell me where it is and when I'll get it?"
```

A good reply acknowledges the delayed order, gives a clear next step (check/expedite the shipment), sets a realistic expectation, and stays under ~150 words.

## What you measure
| Metric | Where it comes from |
|--------|---------------------|
| **Accuracy** | Your rubric below (score each model's answer) |
| **Tokens/sec** | Shown by LM Studio under each reply |
| **Model size (GB)** | The model's file size in LM Studio |
| **RAM** | Memory the model uses when loaded (LM Studio / your system monitor) |

## Scoring rubric (accuracy)
| Criterion | Scale |
|-----------|-------|
| Correct solution proposed | No / Yes |
| Tone matches brand | 1 / 2 / 3 / 4 / 5 |
| Length appropriate | No / Yes |

## Make it your own
- Swap in a real (anonymised) customer email you get often.
- Paste a couple of your best past replies first so the model copies your voice.
- Add a rule like 'always offer a discount code if delivery is late'.

## Optional — reproduce it with a script (advanced)
You do **not** need this for the course. If you later want the numbers filled in
automatically, `main.py` runs the same prompt on **both local models** through LM Studio's
local server and prints a tokens/sec + accuracy table. It is still **100% offline — no API
key, no cloud.** See the comments at the top of `main.py`.
