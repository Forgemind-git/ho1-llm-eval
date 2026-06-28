# HO1 Sample 2 — Invoice Extraction

## What you'll build
A side-by-side test of how well a free local model (in LM Studio) and **Claude.ai** can read a messy invoice and pull out the important fields as clean data. You paste the **same** invoice into both, then score which one got the vendor, date, total and line items right.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **LM Studio** and load any small model (e.g. Llama 3.2). Paste the example prompt below into its chat. Copy the reply.
2. Open **Claude.ai** (your subscription). Paste the **same** prompt. Copy Claude's reply.
3. Open **`index.html`** from this folder in your browser. Paste both replies in and score each using the rubric.
4. Check the JSON each model produced against the invoice and mark what's correct.

## The example prompt
Copy this exactly into both LM Studio and Claude.ai:

```
You are an accounts-payable assistant. Read the invoice text below and return ONLY a JSON object with these fields:
- vendor (string)
- invoice_date (in YYYY-MM-DD format)
- total_amount (a number, no currency symbol)
- line_items (an array of objects with description, quantity, unit_price)

Invoice:
"NORTHWIND SUPPLIES LTD
Invoice #INV-20418   Date: 14 March 2026
Bill to: Riverside Cafe
2x Espresso Beans 1kg @ 18.50
5x Oat Milk 1L @ 2.20
1x Delivery @ 6.00
Total due: GBP 54.00"
```

## Scoring rubric
| Criterion | Scale |
|-----------|-------|
| All 4 fields extracted (vendor, date, amount, line-items) | yes / no |
| Line items correct | 1–5 |
| Output format clean (valid JSON) | 1–5 |
| Hallucinations present | yes / no |

## Make it your own
- Swap in a real (anonymised) invoice from one of your own suppliers.
- Add fields you actually need — e.g. tax amount, PO number, due date.
- Ask for CSV instead of JSON if that's easier to paste into your spreadsheet.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run the comparison
automatically, `main.py` shows how. It needs an Anthropic API key, which is separate from
your Claude.ai subscription — so it costs money and is not part of the hands-on.
