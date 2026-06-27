"""
HO1 Sample 02 — Code Review Benchmark
Sends a buggy Python snippet to Ollama and Claude, then scores each review
for correctness and completeness of bug detection.
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

PROMPT = """\
Review this Python function for bugs and suggest fixes:

def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(calculate_average([]))"""

# Claude Haiku 3.5 pricing (USD per 1M tokens)
CLAUDE_INPUT_COST_PER_1M = 0.80
CLAUDE_OUTPUT_COST_PER_1M = 4.00

# Known bugs in the snippet — used for scoring
KNOWN_BUGS = {
    "zero_division": [
        "zerodivision", "zero division", "zero-division",
        "divisionbyzero", "division by zero",
        "empty list", "empty input", "len(numbers) == 0",
        "len(numbers) is 0", "if not numbers",
    ],
    "no_type_check": [
        "type", "non-numeric", "string", "validate", "isinstance",
        "typeerror", "type error",
    ],
    "integer_division": [
        "float", "integer division", "int division", "truncat",
        "true division", "// vs /",
    ],
}

SUGGESTED_FIXES = {
    "guard_clause": ["if not numbers", "if len(numbers) == 0", "return 0", "return none", "raise"],
    "try_except": ["try", "except", "valueerror", "typeerror"],
}


def call_ollama(prompt: str) -> dict:
    """Send prompt to Ollama and return response with timing."""
    print(f"[Ollama] Sending code review prompt to {OLLAMA_MODEL} ...")
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
        return {
            "text": text,
            "elapsed": elapsed,
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "cost_usd": 0.0,
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
    print(f"[Claude] Sending code review prompt to {CLAUDE_MODEL} ...")
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
    Score a code review response for bug detection and fix quality.

    Criteria:
      - Catches ZeroDivisionError (empty list): 0-2
      - Mentions type/input validation: 0-1
      - Mentions integer vs float division: 0-1
      - Proposes a concrete guard clause or try/except fix: 0-2
      - Provides corrected code snippet: 0-2
      - Overall completeness (multiple distinct issues raised): 0-2
    Max: 10
    """
    if not text:
        return {
            "total": 0, "zero_division": 0, "type_check": 0,
            "int_division": 0, "fix_proposed": 0, "code_snippet": 0, "completeness": 0,
        }

    lower = text.lower()

    # ZeroDivisionError detection (most important bug)
    zero_division = 0
    if any(kw in lower for kw in KNOWN_BUGS["zero_division"]):
        zero_division = 2

    # Type checking mention
    type_check = 0
    if any(kw in lower for kw in KNOWN_BUGS["no_type_check"]):
        type_check = 1

    # Integer/float division mention
    int_division = 0
    if any(kw in lower for kw in KNOWN_BUGS["integer_division"]):
        int_division = 1

    # Concrete fix proposed
    fix_proposed = 0
    if any(kw in lower for kw in SUGGESTED_FIXES["guard_clause"]):
        fix_proposed += 1
    if any(kw in lower for kw in SUGGESTED_FIXES["try_except"]):
        fix_proposed += 1
    fix_proposed = min(fix_proposed, 2)

    # Code snippet in response
    code_snippet = 0
    if "def " in text and "return" in text:
        code_snippet = 2
    elif "```" in text or "    " in text:
        code_snippet = 1

    # Completeness: at least 2 separate issues mentioned
    issues_found = sum([
        zero_division > 0,
        type_check > 0,
        int_division > 0,
    ])
    completeness = min(issues_found, 2)

    total = zero_division + type_check + int_division + fix_proposed + code_snippet + completeness
    return {
        "total": total,
        "zero_division": zero_division,
        "type_check": type_check,
        "int_division": int_division,
        "fix_proposed": fix_proposed,
        "code_snippet": code_snippet,
        "completeness": completeness,
    }


def print_comparison(ollama_result: dict, claude_result: dict,
                     ollama_score: dict, claude_score: dict) -> None:
    """Print a side-by-side comparison table."""
    print("\n" + "=" * 70)
    print("  BENCHMARK RESULTS — Code Review")
    print("=" * 70)

    table = [
        ["Metric", f"Ollama ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"],
        ["Response Time (s)", f"{ollama_result['elapsed']:.2f}", f"{claude_result['elapsed']:.2f}"],
        ["Prompt Tokens", ollama_result["prompt_tokens"], claude_result["prompt_tokens"]],
        ["Output Tokens", ollama_result["output_tokens"], claude_result["output_tokens"]],
        ["Estimated Cost (USD)", "$0.000000 (local)", f"${claude_result['cost_usd']:.6f}"],
        ["--- QUALITY SCORES ---", "", ""],
        ["ZeroDivision bug found (0-2)", ollama_score["zero_division"], claude_score["zero_division"]],
        ["Type validation mentioned (0-1)", ollama_score["type_check"], claude_score["type_check"]],
        ["Int/float division (0-1)", ollama_score["int_division"], claude_score["int_division"]],
        ["Concrete fix proposed (0-2)", ollama_score["fix_proposed"], claude_score["fix_proposed"]],
        ["Code snippet provided (0-2)", ollama_score["code_snippet"], claude_score["code_snippet"]],
        ["Completeness / multiple issues (0-2)", ollama_score["completeness"], claude_score["completeness"]],
        ["TOTAL QUALITY SCORE (/10)", ollama_score["total"], claude_score["total"]],
        ["Error", ollama_result["error"] or "None", claude_result["error"] or "None"],
    ]

    print(tabulate(table[1:], headers=table[0], tablefmt="grid"))

    print("\n--- Ollama Response ---")
    print(ollama_result["text"] or "(no response)")
    print("\n--- Claude Response ---")
    print(claude_result["text"] or "(no response)")


def main():
    print("HO1 Sample 02 — Code Review Benchmark")
    print(f"Prompt snippet: Review calculate_average() for bugs...")
    print()

    ollama_result = call_ollama(PROMPT)
    claude_result = call_claude(PROMPT)

    ollama_score = score_response(ollama_result["text"])
    claude_score = score_response(claude_result["text"])

    print_comparison(ollama_result, claude_result, ollama_score, claude_score)

    results = {
        "sample": "02-code-review",
        "prompt": PROMPT,
        "known_bugs": KNOWN_BUGS,
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
