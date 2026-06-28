# HO1 Sample 4 — Document Redaction

## What you'll build
A side-by-side test of privacy redaction. You give the **same** sensitive document to a free local model (in LM Studio) and to **Claude.ai**, then score which one removed every piece of personal information without wrecking the medical details you need to keep.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **LM Studio** and load any small model (e.g. Llama 3.2). Paste the example prompt below into its chat. Copy the reply.
2. Open **Claude.ai** (your subscription). Paste the **same** prompt. Copy Claude's reply.
3. Open **`index.html`** from this folder in your browser. Paste both replies in and score each using the rubric.
4. Check that names, dates and IDs are gone but the medical facts are untouched.

## The example prompt
Copy this exactly into both LM Studio and Claude.ai:

```
You are a privacy redaction tool. Rewrite the text below, replacing every piece of personally identifiable information with a label in square brackets: [NAME], [DATE_OF_BIRTH], [ADDRESS], [PHONE], [EMAIL], [ID_NUMBER]. Keep all medical and clinical details exactly as written — do NOT redact symptoms, diagnoses, or medication names.

Text:
"Patient Maria Gonzalez, DOB 03/07/1984, lives at 42 Elm Street, Leeds. Phone 07700 900123, email maria.g@example.com. NHS number 945 220 1864. Diagnosed with type 2 diabetes; prescribed metformin 500mg twice daily."
```

## Scoring rubric
| Criterion | Scale |
|-----------|-------|
| All names redacted | yes / no |
| All dates / IDs redacted | yes / no |
| Medical terms preserved (not over-redacted) | yes / no |
| False positives count | 0 / 1-2 / 3+ |

## Make it your own
- Paste a real (test) record from your own system to see how it copes.
- Add or rename labels to match your policy — e.g. [PATIENT_ID] instead of [ID_NUMBER].
- Tighten the 'keep the medical details' instruction if it over-redacts.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run the comparison
automatically, `main.py` shows how. It needs an Anthropic API key, which is separate from
your Claude.ai subscription — so it costs money and is not part of the hands-on.
