# HO1 Sample 01 — Support Tickets

## What you'll build
A side-by-side test of two **local** models. You give the **same** support ticket to both models in LM Studio, then score whether each got the category and urgency right, note each model’s tokens/sec and size, and decide which one to run on the team laptop.

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
You are a customer support triage assistant. Read the ticket below and reply in exactly this format:
Category: <Billing | Technical | Account | Feature request>
Urgency: <Low | Medium | High>
Reply: <a warm 2-3 sentence reply that acknowledges the problem and gives a clear next step>

Ticket:
"I upgraded to the Premium plan 5 days ago but my dashboard still shows Free. I've been charged twice and I'm losing money. Please fix this today."
```

Correct answer: **Category = Billing**, **Urgency = High**.

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
| Category correct | No / Yes |
| Urgency correct | No / Yes |
| Reply quality | 1 / 2 / 3 / 4 / 5 |

## Make it your own
- Swap the ticket for a real (anonymised) one from your own inbox and run all 20.
- Add your own category labels to match how your team files tickets.
- Try two quant levels of the same model (e.g. Q4 vs Q8) to see the size/quality trade-off.

## Optional — reproduce it with a script (advanced)
You do **not** need this for the course. If you later want the numbers filled in
automatically, `main.py` runs the same prompt on **both local models** through LM Studio's
local server and prints a tokens/sec + accuracy table. It is still **100% offline — no API
key, no cloud.** See the comments at the top of `main.py`.
