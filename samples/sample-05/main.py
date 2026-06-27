"""
HO1 Sample 05 — Marketing Copy Generator
Benchmarks Ollama vs Claude on writing a 3-sentence marketing hook,
scoring for persuasiveness, clarity, and call-to-action quality.
"""

import os
import time
import json
import requests
import anthropic
from tabulate import tabulate

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
CLAUDE_MODEL = "claude-haiku-3-5-20251001"

PROMPT = (
    "Write a 3-sentence marketing hook for: an AI scheduling tool that cuts "
    "meeting-booking time by 80%. Target: busy executives. "
    "End with a clear call to action."
)

CLAUDE_INPUT_COST_PER_1M = 0.80
CLAUDE_OUTPUT_COST_PER_1M = 4.00

# CTA trigger words that indicate a concrete call to action
CTA_PHRASES = [
    "sign up", "start free", "try", "book a demo", "get started",
    "request a demo", "learn more", "join", "claim", "schedule",
    "visit", "click", "download", "register", "today",
]

# Persuasion markers
PERSUASION_MARKERS = [
    "80%", "save", "reclaim", "cut", "slash", "eliminate",
    "never again", "imagine", "stop wasting", "focus on what matters",
    "transform", "effortless", "instant", "seamless",
]

# Executive-targeted language
EXEC_LANGUAGE = [
    "executive", "leader", "busy", "c-suite", "decision-maker",
    "your team", "your calendar", "hours back", "strategic",
    "productivity", "roi", "growth", "scale",
]


def call_ollama(prompt):
    print(f"[Ollama] Sending marketing copy prompt to {OLLAMA_MODEL} ...")
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        elapsed = time.time() - start
        text = data.get("response", "")
        prompt_tokens = data.get("prompt_eval_count", 0)
        output_tokens = data.get("eval_count", 0)
        print(f"[Ollama] Done in {elapsed:.2f}s — {output_tokens} output tokens.")
        return {"text": text, "elapsed": elapsed, "prompt_tokens": prompt_tokens,
                "output_tokens": output_tokens, "cost_usd": 0.0, "error": None}
    except requests.exceptions.ConnectionError:
        elapsed = time.time() - start
        msg = f"Cannot connect to Ollama at {OLLAMA_BASE_URL}. Is it running?"
        print(f"[Ollama] ERROR: {msg}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "error": msg}
    except Exception as exc:
        elapsed = time.time() - start
        print(f"[Ollama] ERROR: {exc}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def call_claude(prompt):
    print(f"[Claude] Sending marketing copy prompt to {CLAUDE_MODEL} ...")
    if not ANTHROPIC_API_KEY:
        msg = "ANTHROPIC_API_KEY env var is not set."
        print(f"[Claude] ERROR: {msg}")
        return {"text": "", "elapsed": 0.0, "prompt_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "error": msg}
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    start = time.time()
    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed = time.time() - start
        text = message.content[0].text
        prompt_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        cost = (prompt_tokens / 1_000_000 * CLAUDE_INPUT_COST_PER_1M) + \
               (output_tokens / 1_000_000 * CLAUDE_OUTPUT_COST_PER_1M)
        print(f"[Claude] Done in {elapsed:.2f}s — {output_tokens} output tokens. Cost: ${cost:.6f}")
        return {"text": text, "elapsed": elapsed, "prompt_tokens": prompt_tokens,
                "output_tokens": output_tokens, "cost_usd": cost, "error": None}
    except Exception as exc:
        elapsed = time.time() - start
        print(f"[Claude] ERROR: {exc}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def count_sentences(text):
    """Count approximate sentences by splitting on . ! ?"""
    import re
    sentences = re.split(r'[.!?]+', text.strip())
    return len([s for s in sentences if s.strip()])


def score_response(text):
    """
    Score marketing copy for persuasiveness, clarity, and CTA quality.

    Criteria (max 10):
      three_sentences (0-2): produces approximately 3 sentences
      persuasion (0-2): uses persuasive language / quantified benefit
      exec_targeting (0-2): targets executives / busy leaders
      has_cta (0-2): ends with a clear call to action
      clarity (0-2): concise (20-80 words), no excessive jargon
    """
    if not text:
        return {"total": 0, "three_sentences": 0, "persuasion": 0,
                "exec_targeting": 0, "has_cta": 0, "clarity": 0}

    lower = text.lower()
    word_count = len(text.split())

    sentence_count = count_sentences(text)
    three_sentences = 0
    if 2 <= sentence_count <= 4:
        three_sentences = 2
    elif sentence_count == 5:
        three_sentences = 1

    persuasion = 0
    persuasion_hits = sum(1 for p in PERSUASION_MARKERS if p.lower() in lower)
    if persuasion_hits >= 2:
        persuasion = 2
    elif persuasion_hits == 1:
        persuasion = 1

    exec_targeting = 0
    exec_hits = sum(1 for e in EXEC_LANGUAGE if e.lower() in lower)
    if exec_hits >= 2:
        exec_targeting = 2
    elif exec_hits == 1:
        exec_targeting = 1

    has_cta = 0
    cta_hits = sum(1 for c in CTA_PHRASES if c.lower() in lower)
    if cta_hits >= 1:
        # Stronger score if CTA appears in the last sentence
        last_sentence = text.strip().split(".")[-2] if "." in text else text
        if any(c.lower() in last_sentence.lower() for c in CTA_PHRASES):
            has_cta = 2
        else:
            has_cta = 1

    clarity = 0
    if 20 <= word_count <= 80:
        clarity = 2
    elif 15 <= word_count <= 100:
        clarity = 1

    total = three_sentences + persuasion + exec_targeting + has_cta + clarity
    return {"total": total, "three_sentences": three_sentences, "persuasion": persuasion,
            "exec_targeting": exec_targeting, "has_cta": has_cta, "clarity": clarity,
            "word_count": word_count, "sentence_count": sentence_count}


def print_comparison(ollama_result, claude_result, ollama_score, claude_score):
    print("\n" + "=" * 70)
    print("  BENCHMARK RESULTS — Marketing Copy Generator")
    print("=" * 70)
    table = [
        ["Metric", f"Ollama ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"],
        ["Response Time (s)", f"{ollama_result['elapsed']:.2f}", f"{claude_result['elapsed']:.2f}"],
        ["Prompt Tokens", ollama_result["prompt_tokens"], claude_result["prompt_tokens"]],
        ["Output Tokens", ollama_result["output_tokens"], claude_result["output_tokens"]],
        ["Estimated Cost (USD)", "$0.000000 (local)", f"${claude_result['cost_usd']:.6f}"],
        ["Word Count", ollama_score.get("word_count", "N/A"), claude_score.get("word_count", "N/A")],
        ["Sentence Count", ollama_score.get("sentence_count", "N/A"), claude_score.get("sentence_count", "N/A")],
        ["--- QUALITY SCORES ---", "", ""],
        ["3-sentence format (0-2)", ollama_score["three_sentences"], claude_score["three_sentences"]],
        ["Persuasive language (0-2)", ollama_score["persuasion"], claude_score["persuasion"]],
        ["Executive targeting (0-2)", ollama_score["exec_targeting"], claude_score["exec_targeting"]],
        ["Clear CTA present (0-2)", ollama_score["has_cta"], claude_score["has_cta"]],
        ["Clarity / conciseness (0-2)", ollama_score["clarity"], claude_score["clarity"]],
        ["TOTAL QUALITY SCORE (/10)", ollama_score["total"], claude_score["total"]],
        ["Error", ollama_result["error"] or "None", claude_result["error"] or "None"],
    ]
    print(tabulate(table[1:], headers=table[0], tablefmt="grid"))
    print("\n--- Ollama Copy ---")
    print(ollama_result["text"] or "(no response)")
    print("\n--- Claude Copy ---")
    print(claude_result["text"] or "(no response)")


def main():
    print("HO1 Sample 05 — Marketing Copy Generator Benchmark")
    print("Prompt: 3-sentence hook for AI scheduling tool, target: busy executives...")
    print()
    ollama_result = call_ollama(PROMPT)
    claude_result = call_claude(PROMPT)
    ollama_score = score_response(ollama_result["text"])
    claude_score = score_response(claude_result["text"])
    print_comparison(ollama_result, claude_result, ollama_score, claude_score)
    results = {
        "sample": "05-marketing-copy",
        "prompt": PROMPT,
        "ollama": {"model": OLLAMA_MODEL, **ollama_result, "quality_score": ollama_score},
        "claude": {"model": CLAUDE_MODEL, **claude_result, "quality_score": claude_score},
    }
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
