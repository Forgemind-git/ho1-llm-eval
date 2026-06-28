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
You do **not** need this for the course. If you later want to run the comparison
automatically, `main.py` shows how. It needs an Anthropic API key, which is separate from
your Claude.ai subscription — so it costs money and is not part of the hands-on.
