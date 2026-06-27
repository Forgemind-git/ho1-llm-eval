"""
HO1 Sample 03 — Structured Data Extraction
Sends freeform customer text to Ollama and Claude, then compares JSON extraction
accuracy against known ground-truth field values.
"""

import os
import time
import json
import re
import requests
import anthropic
from tabulate import tabulate

# --- Configuration ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
CLAUDE_MODEL = "claude-haiku-3-5-20251001"

PROMPT = (
    'Extract these fields as JSON: customer_name, order_id, issue, urgency_level (low/medium/high). '
    'Text: "Hi, I am Maria. Order #ORD-2847 arrived yesterday but three items are missing. '
    'I have a client event tomorrow morning."'
)

# Ground truth values for accuracy scoring
GROUND_TRUTH = {
    "customer_name": "maria",
    "order_id": "ord-2847",
    "issue": ["missing", "items"],  # must contain these words
    "urgency_level": "high",        # tomorrow morning = high urgency
}

# Claude Haiku 3.5 pricing (USD per 1M tokens)
CLAUDE_INPUT_COST_PER_1M = 0.80
CLAUDE_OUTPUT_COST_PER_1M = 4.00


def call_ollama(prompt: str) -> dict:
    """Send prompt to Ollama and return response with timing."""
    print(f"[Ollama] Sending extraction prompt to {OLLAMA_MODEL} ...")
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
    print(f"[Claude] Sending extraction prompt to {CLAUDE_MODEL} ...")
    if not ANTHROPIC_API_KEY:
        msg = "ANTHROPIC_API_KEY env var is not set."
        print(f"[Claude] ERROR: {msg}")
        return {"text": "", "elapsed": 0.0, "prompt_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "error": msg}

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


def extract_json_from_text(text: str) -> dict:
    """
    Attempt to parse JSON from a model response.
    Handles markdown code blocks and raw JSON.
    Returns empty dict on failure.
    """
    if not text:
        return {}

    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?", "", text).strip().strip("`")

    # Find the first { ... } block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Try parsing the full cleaned text
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


def score_extraction(text: str) -> dict:
    """
    Score a structured extraction response.

    Criteria:
      - Valid JSON produced: 0 or 2
      - customer_name correct: 0 or 2
      - order_id correct: 0 or 2
      - issue contains relevant keywords: 0 or 2
      - urgency_level correct (high): 0 or 2
    Max: 10

    Returns score breakdown and the parsed dict.
    """
    if not text:
        return {
            "total": 0, "valid_json": 0, "customer_name": 0,
            "order_id": 0, "issue": 0, "urgency_level": 0, "parsed": {},
        }

    parsed = extract_json_from_text(text)
    valid_json = 2 if parsed else 0

    # Normalize all values to lowercase strings for comparison
    def norm(v):
        return str(v).lower().strip() if v else ""

    customer_name_score = 0
    if norm(parsed.get("customer_name")) == GROUND_TRUTH["customer_name"]:
        customer_name_score = 2

    order_id_score = 0
    if norm(parsed.get("order_id")) == GROUND_TRUTH["order_id"]:
        order_id_score = 2

    issue_score = 0
    issue_val = norm(parsed.get("issue"))
    if all(kw in issue_val for kw in GROUND_TRUTH["issue"]):
        issue_score = 2
    elif any(kw in issue_val for kw in GROUND_TRUTH["issue"]):
        issue_score = 1

    urgency_score = 0
    if norm(parsed.get("urgency_level")) == GROUND_TRUTH["urgency_level"]:
        urgency_score = 2

    total = valid_json + customer_name_score + order_id_score + issue_score + urgency_score
    return {
        "total": total,
        "valid_json": valid_json,
        "customer_name": customer_name_score,
        "order_id": order_id_score,
        "issue": issue_score,
        "urgency_level": urgency_score,
        "parsed": parsed,
    }


def print_comparison(ollama_result: dict, claude_result: dict,
                     ollama_score: dict, claude_score: dict) -> None:
    """Print a side-by-side comparison table."""
    print("\n" + "=" * 70)
    print("  BENCHMARK RESULTS — Structured Data Extraction")
    print("=" * 70)

    table = [
        ["Metric", f"Ollama ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"],
        ["Response Time (s)", f"{ollama_result['elapsed']:.2f}", f"{claude_result['elapsed']:.2f}"],
        ["Prompt Tokens", ollama_result["prompt_tokens"], claude_result["prompt_tokens"]],
        ["Output Tokens", ollama_result["output_tokens"], claude_result["output_tokens"]],
        ["Estimated Cost (USD)", "$0.000000 (local)", f"${claude_result['cost_usd']:.6f}"],
        ["--- ACCURACY SCORES ---", "", ""],
        ["Valid JSON output (0-2)", ollama_score["valid_json"], claude_score["valid_json"]],
        ["customer_name correct (0-2)", ollama_score["customer_name"], claude_score["customer_name"]],
        ["order_id correct (0-2)", ollama_score["order_id"], claude_score["order_id"]],
        ["issue description (0-2)", ollama_score["issue"], claude_score["issue"]],
        ["urgency_level = high (0-2)", ollama_score["urgency_level"], claude_score["urgency_level"]],
        ["TOTAL ACCURACY SCORE (/10)", ollama_score["total"], claude_score["total"]],
        ["Error", ollama_result["error"] or "None", claude_result["error"] or "None"],
    ]

    print(tabulate(table[1:], headers=table[0], tablefmt="grid"))

    print("\n--- Ground Truth ---")
    print(json.dumps({
        "customer_name": "Maria",
        "order_id": "ORD-2847",
        "issue": "three items missing from order",
        "urgency_level": "high",
    }, indent=2))

    print("\n--- Ollama Parsed JSON ---")
    print(json.dumps(ollama_score["parsed"], indent=2) if ollama_score["parsed"] else "(no valid JSON)")
    print("\n--- Claude Parsed JSON ---")
    print(json.dumps(claude_score["parsed"], indent=2) if claude_score["parsed"] else "(no valid JSON)")

    print("\n--- Ollama Raw Response ---")
    print(ollama_result["text"] or "(no response)")
    print("\n--- Claude Raw Response ---")
    print(claude_result["text"] or "(no response)")


def main():
    print("HO1 Sample 03 — Structured Data Extraction Benchmark")
    print(f"Prompt: Extract JSON fields from a customer message...")
    print()

    ollama_result = call_ollama(PROMPT)
    claude_result = call_claude(PROMPT)

    ollama_score = score_extraction(ollama_result["text"])
    claude_score = score_extraction(claude_result["text"])

    print_comparison(ollama_result, claude_result, ollama_score, claude_score)

    results = {
        "sample": "03-data-extraction",
        "prompt": PROMPT,
        "ground_truth": {
            "customer_name": "Maria",
            "order_id": "ORD-2847",
            "issue": "three items missing",
            "urgency_level": "high",
        },
        "ollama": {
            "model": OLLAMA_MODEL,
            **{k: v for k, v in ollama_result.items() if k != "text"},
            "raw_response": ollama_result["text"],
            "quality_score": {k: v for k, v in ollama_score.items() if k != "parsed"},
            "parsed_json": ollama_score["parsed"],
        },
        "claude": {
            "model": CLAUDE_MODEL,
            **{k: v for k, v in claude_result.items() if k != "text"},
            "raw_response": claude_result["text"],
            "quality_score": {k: v for k, v in claude_score.items() if k != "parsed"},
            "parsed_json": claude_score["parsed"],
        },
    }

    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
