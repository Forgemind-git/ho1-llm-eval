# HO1 Sample 03 — Meeting Notes

## What you'll build
A side-by-side test of two **local** models on meeting notes. You give the **same** transcript to both models in LM Studio, then score which produced the more usable action-item list with the right owners — and weigh that against the tokens/sec each one managed.

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
You are a meeting assistant. Read the transcript below and return an action-item list. Use exactly this format, one item per line:
- Owner | Task | Due date

Transcript:
"Sarah (PM): The dashboard needs to ship by the end of March. Dev (Lead): That's about four weeks of work, but I need the design specs first. Ana (Design): I can have the mockups ready by Friday. Dev: Great — I'll also need the API docs. Sarah: I'll chase the backend team for those by end of day today. Let's lock the launch date as March 28."
```

Owners that must appear: **Ana** (mockups, Friday), **Sarah** (chase API docs, today), **Dev** (build dashboard, March 28).

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
| All action items captured | No / Yes |
| Owners correct | No / Yes |
| Format usable | 1 / 2 / 3 / 4 / 5 |

## Make it your own
- Paste a transcript from one of your own calls (Zoom/Teams can export the text).
- Ask for the items as a checklist you can paste straight into your task tool.
- Add a 'Risks / blockers' line to the format if your meetings need it.

## Optional — reproduce it with a script (advanced)
You do **not** need this to complete the hands-on — it is a convenience for anyone who
wants the numbers filled in automatically. It is still **100% offline: no API key, no cloud.**

`main.py` sends the example prompt to **both local models** through LM Studio's local
server and prints a tokens/sec + accuracy table.

### What it measures
| What it checks | How |
|----------------|-----|
| **Accuracy** | A simple, deterministic rubric for this task (see `main.py`) |
| **Tokens/sec** | Output tokens ÷ response time |
| **Response time** | Wall-clock time for each model |

Model **size (GB)** and **RAM** are read from the LM Studio UI — the script prints a
reminder to add them to `index.html`.

### Run it (optional)
```bash
# 1. In LM Studio, download your two models, then open the Developer tab and click Start Server.
# 2. Install the one Python package:
pip install -r requirements.txt
# 3. Point the script at your two models:
cp .env.example .env        # edit MODEL_A / MODEL_B to the exact IDs shown in LM Studio
# 4. Run it:
python main.py
```
Results are also written to `results.json`. Again — this is optional; the course only
needs the no-code steps under **Run it in LM Studio** above.
