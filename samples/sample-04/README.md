# HO1 Sample 04 — Document Redaction

## What you'll build
A side-by-side test of two **local** models on privacy redaction. You give the **same** sensitive record to both models in LM Studio, then count how many personal-data items each one masked (and whether it kept the medical details), and compare their speed and RAM use.

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
You are a privacy redaction tool. Rewrite the text below, replacing every piece of personally identifiable information with a label in square brackets: [NAME], [DATE_OF_BIRTH], [ADDRESS], [PHONE], [EMAIL], [ID_NUMBER]. Keep all medical and clinical details exactly as written — do NOT redact symptoms, diagnoses, or medication names.

Text:
"Patient Maria Gonzalez, DOB 03/07/1984, lives at 42 Elm Street, Leeds. Phone 07700 900123, email maria.g@example.com. NHS number 945 220 1864. Diagnosed with type 2 diabetes; prescribed metformin 500mg twice daily."
```

6 PII items must be masked: **name, date of birth, address, phone, email, NHS number**. The medical details (**type 2 diabetes**, **metformin**) must stay.

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
| All PII masked | No / Yes |
| Medical details preserved | No / Yes |
| False positives (over-redaction) | 3+ / 1-2 / 0 |

## Make it your own
- Paste a real (test) record from your own system to see how it copes.
- Rename labels to match your policy — e.g. [PATIENT_ID] instead of [ID_NUMBER].
- Tighten the 'keep the medical details' instruction if a model over-redacts.

## Optional — reproduce it with a script (advanced)
You do **not** need this for the course. If you later want the numbers filled in
automatically, `main.py` runs the same prompt on **both local models** through LM Studio's
local server and prints a tokens/sec + accuracy table. It is still **100% offline — no API
key, no cloud.** See the comments at the top of `main.py`.
