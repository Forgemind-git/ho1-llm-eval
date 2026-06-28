# HO1 — LLM Evaluation Report

> Hands-on portfolio project · **Week 1** · **Solo** · module M4. Part of the **ForgeMind AI — AI Productivity Essentials** course.

## Goal

**Done when:** A reproducible eval with a data-backed recommendation

## What to ship

The eval script/sheet + a results table + a RECOMMENDATION.md naming the model to use and why.

## Pick a problem statement

Choose **one** of these real use-cases — or bring your own (get it approved first):

1. Your support team handles ~150 tickets a week and you are weighing a local model to cut API spend. Take 20 real anonymised tickets, run each through a local model and through Claude, score whether the category and urgency are right, log cost and response time, then write a one-paragraph recommendation on which to use.

2. You run accounts payable and key invoices by hand. Grab 15 scanned supplier invoices, have a local model and Claude each pull the date, vendor and total, score every field against the truth, and report which model is accurate enough to trust and how much cheaper it runs at your monthly volume.

3. As a project lead drowning in call recordings, you want notes that write themselves. Feed 10 long meeting transcripts to a local model and to Claude, ask each for a clean action-item list with owners, then judge which produced usable items faster and report the quality and speed gap you measured.

4. Your clinic must keep patient data on the premises, so cloud AI is off the table for redaction. Run 20 sensitive documents through a local model to mask names, addresses and IDs, count how many PII items it missed versus Claude, and conclude whether on-device redaction is reliable enough to ship.

5. You handle a flood of repetitive customer emails and want AI to draft the first reply. Take 15 common queries, have a local model and Claude each draft a response, rate tone and accuracy on a simple rubric, log cost per reply, and recommend which model gives the best quality for the price.

## How to use this repo

1. Click **Use this template** to create your own copy.
2. Build your chosen project in your copy.
3. Replace this section of the README with: what you built, the problem it solves, and how to run it.

---

*HO1 · Solo · ForgeMind AI Course · module M4 (Week 1)*


## 💡 Use your Claude.ai Pro plan wisely

The Pro plan has a usage limit that resets every few hours. A few habits make it stretch — and
keep a mistake from burning your whole session:

- **Use the example prompt** in each sample's README — it's already written and tested. Don't
  reinvent it.
- **One clear prompt** beats lots of vague back-and-forth. Say what you want, with an example, in
  a single message.
- **Start a new chat when you switch tasks.** Long chats re-read every earlier message and use up
  your limit faster.
- **Don't paste big files over and over.** Paste once, then refer back to it.
- **If something works, keep it.** Tweak it rather than regenerate from scratch.
- **Using Claude Code or Cowork?** This repo's `CLAUDE.md` makes Claude follow these same rules
  automatically, and `SKILL.md` is a reusable "token-wise" skill.

If you do hit the limit, it resets after a few hours — nothing you've saved is lost.
