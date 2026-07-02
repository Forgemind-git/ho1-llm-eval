# HO1 Sample 02 — Invoice Extraction

## What you'll build
A side-by-side test of two **local** models reading a supplier invoice. You paste the **same** invoice into both models in LM Studio, then score whether each got the vendor, date and total right, and compare their tokens/sec and file size.

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
You are an accounts-payable assistant. Read the invoice text below and return ONLY a JSON object with these fields:
- vendor (string)
- invoice_date (in YYYY-MM-DD format)
- total_amount (a number, no currency symbol)

Invoice:
"NORTHWIND SUPPLIES LTD
Invoice #INV-20418   Date: 14 March 2026
Bill to: Riverside Cafe
2x Espresso Beans 1kg @ 18.50
5x Oat Milk 1L @ 2.20
1x Delivery @ 6.00
Total due: GBP 54.00"
```

Correct answer: **vendor = NORTHWIND SUPPLIES LTD**, **invoice_date = 2026-03-14**, **total_amount = 54.00**.

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
| Vendor correct | No / Yes |
| Date correct (YYYY-MM-DD) | No / Yes |
| Total correct | No / Yes |

## Make it your own
- Swap in a real (anonymised) invoice from one of your own suppliers.
- Add fields you actually need — e.g. tax amount, PO number, due date.
- Ask for CSV instead of JSON if that pastes more easily into your spreadsheet.

## Optional — reproduce it with a script (advanced)
You do **not** need this for the course. If you later want the numbers filled in
automatically, `main.py` runs the same prompt on **both local models** through LM Studio's
local server and prints a tokens/sec + accuracy table. It is still **100% offline — no API
key, no cloud.** See the comments at the top of `main.py`.
