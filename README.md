# HO1 — LLM Evaluation Report

> Hands-on portfolio project · **Week 1** · **Solo** · module M4. Part of the **ForgeMind AI — AI Productivity Essentials** course.

## Goal

**Done when:** A reproducible eval of **two local models**, head-to-head, with a data-backed recommendation.

## What to ship

The eval sheet/script + a results table (**accuracy · tokens/sec · model size (GB) · RAM**) + a **`RECOMMENDATION.md`** naming which **local** model to run and why.

## What you measure

Run the **same** prompt on **two local models** in **LM Studio** and compare them on four things — all gathered **offline**, no API key, no cloud, no Claude:

| Metric | Where it comes from |
|--------|---------------------|
| **Accuracy** | Your own rubric — score each model's answer |
| **Tokens/sec** | Shown by LM Studio under each reply |
| **Model size (GB)** | The model's file size in LM Studio |
| **RAM** | Memory the model uses when loaded |

## Pick a problem statement

Choose **one** of these real use-cases — or bring your own (get it approved first):

1. "Your support team handles ~150 tickets a week and you want an offline model that runs on the team laptop. Take 20 real anonymised tickets and run each through two local models in LM Studio (e.g. Llama 3.2 1B vs Qwen 2.5 3B), score whether the category and urgency are right, read off each model’s tokens/sec and size, then write a one-paragraph recommendation on which local model to run and why."

2. "You run accounts payable and want to key invoices on-device without sending them to the cloud. Grab 15 scanned supplier invoices, have two local models each pull the date, vendor and total, score every field against the truth, compare their speed (tokens/sec) and file size, and report which local model is accurate enough to trust and light enough for your laptop."

3. "As a project lead drowning in call recordings, you want notes that write themselves — offline. Feed 10 long meeting transcripts to two local models (say a 1B and a 3B), ask each for a clean action-item list with owners, then judge which produced usable items and report the quality-versus-speed trade-off you measured in LM Studio."

4. "Your clinic must keep patient data on the premises, so everything stays offline. Run 20 sensitive documents through two local models to mask names, addresses and IDs, count how many PII items each one missed, compare their speed and RAM use, and conclude which on-device model is reliable enough to ship."

5. "You handle a flood of repetitive customer emails and want a local model to draft the first reply. Take 15 common queries, have two local models each draft a response, rate tone and accuracy on a simple rubric, note each model’s tokens/sec and size, and recommend which local model gives the best quality for the compute it needs."

## How to run it (100% offline)

1. Install **LM Studio** and download **two** local models to compare — e.g. **Llama 3.2 1B** vs **Qwen 2.5 3B**, or two quant levels of one model.
2. Open the chosen sample folder and copy its **example prompt**.
3. Run that prompt on **Model A**, then on **Model B**, in LM Studio's chat. For each, note the **tokens/sec**, **size (GB)** and **RAM**.
4. Open the sample's **`index.html`** in your browser. Paste both replies, score them with the rubric, and enter the metrics. Download the results table.
5. Fill in the sample's **`RECOMMENDATION.md`** naming the local model you'd run and why.

No API key. No cloud. Everything runs on your own machine.

## How to use this repo

1. Click **Use this template** to create your own copy.
2. Build your chosen project in your copy (start from a sample — the prompts are ready to use).
3. Replace this section of the README with: what you built, which two models you compared, and your recommendation.

---

*HO1 · Solo · ForgeMind AI Course · module M4 (Week 1)*

## 🖥️ This hands-on is 100% offline

Everything here runs **on your own machine** with **LM Studio** — no API key, no cloud, no Claude in the loop. A few habits keep it smooth:

- **Use the example prompt** in each sample's README — it's already written and tested. Run the *same* prompt on both models so the comparison is fair.
- **Change one thing at a time.** Compare two models, or two quant levels — not both at once — so you know what caused the difference.
- **Small models are surprisingly capable.** The whole point is to find out whether a 1B or 3B model is *good enough* to run on-device.
- **Using Claude Code or Cowork to help you build?** This repo's `CLAUDE.md` and `SKILL.md` keep that help efficient and beginner-friendly.
