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
You do **not** need any of this to complete the hands-on — it's here as a reference for
anyone who wants to run the same comparison automatically later.

`main.py` sends the example prompt to a local model (via LM Studio / Ollama) **and** to
Claude through the Anthropic API, times both, and prints a side-by-side score table.

### What it measures
| What it checks | How |
|----------------|-----|
| **Valid JSON** | Output parses as JSON with no extra text |
| **All fields present** | vendor, invoice_date, total_amount, line_items |
| **Date normalised** | Free-text date turned into YYYY-MM-DD |
| **Line items correct** | Right count, quantities and prices |

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
