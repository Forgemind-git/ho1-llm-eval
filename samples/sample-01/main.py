"""
HO1 Sample 01 — Support Email Drafter
Benchmarks a local Ollama model vs Claude on drafting empathetic customer support emails.
"""

import os
import time
import json
import requests
import anthropic
from tabulate import tabulate

# --- Configuration ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
CLAUDE_MODEL = "claude-haiku-3-5-20251001"

PROMPT = (
    'You are a customer support agent. A customer wrote: '
    '"I ordered the Premium Plan 5 days ago but my dashboard still shows Free. '
    'I am losing money." '
    "Draft a professional, empathetic reply."
)

# Rough token cost for Claude Haiku 3.5 (per 1M tokens, USD)
CLAUDE_INPUT_COST_PER_1M = 0.80
CLAUDE_OUTPUT_COST_PER_1M = 4.00


def call_ollama(prompt: str) -> dict:
    """Send prompt to Ollama and return response with timing."""
    print(f"[Ollama] Sending prompt to {OLLAMA_MODEL} ...")
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        elapsed = time.time() - start
        text = data.get("response", "")
        # Ollama returns eval_count (tokens generated) and prompt_eval_count
        prompt_tokens = data.get("prompt_eval_count", 0)
        output_tokens = data.get("eval_count", 0)
        print(f"[Ollama] Done in {elapsed:.2f}s — {output_tokens} output tokens.")
        return {
            "text": text,
            "elapsed": elapsed,
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "cost_usd": 0.0,  # local model, no API cost
            "error": None,
        }
    except requests.exceptions.ConnectionError:
        elapsed = time.time() - start
        msg = f"Cannot connect to Ollama at {OLLAMA_BASE_URL}. Is it running?"
        print(f"[Ollama] ERROR: {msg}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "error": msg}
    except Exception as exc:
        elapsed = time.time() - start
        print(f"[Ollama] ERROR: {exc}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def call_claude(prompt: str) -> dict:
    """Send prompt to Claude and return response with timing."""
    print(f"[Claude] Sending prompt to {CLAUDE_MODEL} ...")
    if not ANTHROPIC_API_KEY:
        msg = "ANTHROPIC_API_KEY env var is not set."
        print(f"[Claude] ERROR: {msg}")
        return {"text": "", "elapsed": 0.0, "prompt_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "error": msg}

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    start = time.time()
    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed = time.time() - start
        text = message.content[0].text
        prompt_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        cost = (prompt_tokens / 1_000_000 * CLAUDE_INPUT_COST_PER_1M) + \
               (output_tokens / 1_000_000 * CLAUDE_OUTPUT_COST_PER_1M)
        print(f"[Claude] Done in {elapsed:.2f}s — {output_tokens} output tokens. Cost: ${cost:.6f}")
        return {
            "text": text,
            "elapsed": elapsed,
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
            "error": None,
        }
    except Exception as exc:
        elapsed = time.time() - start
        print(f"[Claude] ERROR: {exc}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def score_response(text: str) -> dict:
    """
    Heuristic scoring for a support email reply.
    Criteria:
      - Empathy (mentions sorry / apologize / understand): 0-2
      - Acknowledgement (references the specific problem): 0-2
      - Resolution offer (mentions fix / team / investigate / escalate): 0-2
      - Professionalism (length >= 80 words, proper greeting): 0-2
      - Clarity (no jargon, readable length < 300 words): 0-2
    Max score: 10
    """
    if not text:
        return {"total": 0, "empathy": 0, "acknowledgement": 0, "resolution": 0, "professionalism": 0, "clarity": 0}

    lower = text.lower()
    word_count = len(text.split())

    empathy = 0
    if any(w in lower for w in ["sorry", "apologize", "apologies", "understand", "frustrat"]):
        empathy += 1
    if any(w in lower for w in ["sincerely", "truly", "deeply", "we value"]):
        empathy += 1

    acknowledgement = 0
    if any(w in lower for w in ["premium", "dashboard", "free", "plan"]):
        acknowledgement += 1
    if any(w in lower for w in ["5 days", "five days", "order", "account"]):
        acknowledgement += 1

    resolution = 0
    if any(w in lower for w in ["investigate", "look into", "fix", "resolve", "escalate", "team"]):
        resolution += 1
    if any(w in lower for w in ["24 hours", "48 hours", "shortly", "as soon as", "immediately", "priority"]):
        resolution += 1

    professionalism = 0
    if word_count >= 80:
        professionalism += 1
    if any(w in lower for w in ["dear", "hello", "hi", "greetings"]):
        professionalism += 1

    clarity = 0
    if 80 <= word_count <= 300:
        clarity += 1
    if any(w in lower for w in ["sincerely", "regards", "best", "thank you"]):
        clarity += 1

    total = empathy + acknowledgement + resolution + professionalism + clarity
    return {
        "total": total,
        "empathy": empathy,
        "acknowledgement": acknowledgement,
        "resolution": resolution,
        "professionalism": professionalism,
        "clarity": clarity,
    }


def print_comparison(ollama_result: dict, claude_result: dict,
                     ollama_score: dict, claude_score: dict) -> None:
    """Print a side-by-side comparison table."""
    print("\n" + "=" * 70)
    print("  BENCHMARK RESULTS — Support Email Drafter")
    print("=" * 70)

    table = [
        ["Metric", f"Ollama ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"],
        ["Response Time (s)", f"{ollama_result['elapsed']:.2f}", f"{claude_result['elapsed']:.2f}"],
        ["Prompt Tokens", ollama_result["prompt_tokens"], claude_result["prompt_tokens"]],
        ["Output Tokens", ollama_result["output_tokens"], claude_result["output_tokens"]],
        ["Estimated Cost (USD)", "$0.000000 (local)", f"${claude_result['cost_usd']:.6f}"],
        ["--- QUALITY SCORES ---", "", ""],
        ["Empathy (0-2)", ollama_score["empathy"], claude_score["empathy"]],
        ["Acknowledgement (0-2)", ollama_score["acknowledgement"], claude_score["acknowledgement"]],
        ["Resolution Offer (0-2)", ollama_score["resolution"], claude_score["resolution"]],
        ["Professionalism (0-2)", ollama_score["professionalism"], claude_score["professionalism"]],
        ["Clarity (0-2)", ollama_score["clarity"], claude_score["clarity"]],
        ["TOTAL QUALITY SCORE (/10)", ollama_score["total"], claude_score["total"]],
        ["Error", ollama_result["error"] or "None", claude_result["error"] or "None"],
    ]

    print(tabulate(table[1:], headers=table[0], tablefmt="grid"))

    print("\n--- Ollama Response ---")
    print(ollama_result["text"] or "(no response)")
    print("\n--- Claude Response ---")
    print(claude_result["text"] or "(no response)")


def main():
    print("HO1 Sample 01 — Support Email Drafter Benchmark")
    print(f"Prompt: {PROMPT[:80]}...")
    print()

    ollama_result = call_ollama(PROMPT)
    claude_result = call_claude(PROMPT)

    ollama_score = score_response(ollama_result["text"])
    claude_score = score_response(claude_result["text"])

    print_comparison(ollama_result, claude_result, ollama_score, claude_score)

    results = {
        "sample": "01-customer-support-email",
        "prompt": PROMPT,
        "ollama": {
            "model": OLLAMA_MODEL,
            **ollama_result,
            "quality_score": ollama_score,
        },
        "claude": {
            "model": CLAUDE_MODEL,
            **claude_result,
            "quality_score": claude_score,
        },
    }

    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
