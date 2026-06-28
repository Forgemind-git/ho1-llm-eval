# HO1 Sample 3 — Meeting Notes

## What you'll build
A side-by-side test of meeting-summary quality. You give the **same** meeting transcript to a free local model (in LM Studio) and to **Claude.ai**, then score which one produced the clearer summary and the most usable list of action items with owners.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login.

1. Open **LM Studio** and load any small model (e.g. Llama 3.2). Paste the example prompt below into its chat. Copy the reply.
2. Open **Claude.ai** (your subscription). Paste the **same** prompt. Copy Claude's reply.
3. Open **`index.html`** from this folder in your browser. Paste both replies in and score each using the rubric.
4. Compare the action items each model found against the transcript and mark what's right.

## The example prompt
Copy this exactly into both LM Studio and Claude.ai:

```
You are a meeting assistant. Read the transcript below and produce:
1. A 2-3 sentence summary.
2. A bulleted list of the decisions made.
3. An action-item table with the columns: Owner | Task | Due date.

Transcript:
"Sarah (PM): The dashboard needs to ship by the end of March. Dev (Lead): That's about four weeks of work, but I need the design specs first. Ana (Design): I can have the mockups ready by Friday. Dev: Great — I'll also need the API docs. Sarah: I'll chase the backend team for those by end of day today. Let's lock the launch date as March 28."
```

## Scoring rubric
| Criterion | Scale |
|-----------|-------|
| All action items captured | yes / no |
| Owners assigned correctly | yes / no |
| Summary length appropriate | 1–5 |
| Key decisions included | yes / no |

## Make it your own
- Paste a transcript from one of your own calls (Zoom/Teams export the text).
- Ask for the action items as a checklist you can paste straight into your task tool.
- Add a 'Risks / blockers' section to the prompt if your meetings need it.

## Optional — automate it with the API (advanced)
You do **not** need any of this to complete the hands-on — it's here as a reference for
anyone who wants to run the same comparison automatically later.

`main.py` sends the example prompt to a local model (via LM Studio / Ollama) **and** to
Claude through the Anthropic API, times both, and prints a side-by-side score table.

### What it measures
| What it checks | How |
|----------------|-----|
| **Summary present** | 2-3 sentence overview at the top |
| **Action items captured** | Every task that was assigned is listed |
| **Owners correct** | Right person against each task |
| **Decisions listed** | The launch date / key decisions are noted |

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
