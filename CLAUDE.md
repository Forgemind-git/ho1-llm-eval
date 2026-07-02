# CLAUDE.md — LLM Evaluation Report (HO1)

Guidance for **Claude Code / Claude Cowork** when helping a student work in this repo. The
student is usually a **beginner** — keep help clear, friendly, and efficient.

## About this project
Compare **two local models** head-to-head in **LM Studio** on the same task, and recommend
which one to run on-device. The metrics are **accuracy (a rubric), tokens/sec, model size
(GB) and RAM**.

**This hands-on is 100% offline — no API key, no cloud, no Claude in the eval loop.**
The primary way to do it is no-code: run the example prompt on both local models in LM
Studio, then score the results in `index.html`. The work lives under
`samples/sample-01 … sample-05`; each sample has its own `README.md` with a ready-to-use
example prompt. Start from those — they already work.

## How to help well
- **Plan before you build.** State a 1–3 line plan, then make the whole change in one pass.
- **Use the example prompt in the sample README** instead of writing a new one — it's tested.
- **Don't re-read or re-paste** files already shown in the conversation.
- **Keep replies short** — show only what changed, skip the preamble.
- **Reuse the sample files** — tweak them, don't rebuild from scratch.

## This repo, specifically
- It's the **LLM Evaluation Report** hands-on: a manual side-by-side comparison of **two
  local models**, scored in a browser scorecard, with a `RECOMMENDATION.md` deliverable.
- **No API key is needed — ever.** Any `main.py` is an OPTIONAL convenience that talks to
  LM Studio's own local server (still offline). Ignore it unless the student asks.
- When helping on the `starter` branch, don't restructure the repo or touch `main`.

See `SKILL.md` for the reusable **token-wise** skill that carries these same habits into Claude.ai.
