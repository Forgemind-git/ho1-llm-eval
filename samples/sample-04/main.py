"""
HO1 Sample 04 — Meeting Note Summariser
Benchmarks Ollama vs Claude on summarising a meeting transcript and
extracting action items with owners.
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
    "Summarise this meeting and list action items with owners.\n"
    "Meeting: Sprint planning, 15 Jan. Present: Sarah (PM), Dev (Lead), Ana (Design).\n"
    "Sarah: Dashboard ships end of March. Dev: 4 weeks out, need design specs. "
    "Ana: Mockups ready Friday. Dev: Also need API docs. Sarah: Will chase backend by EOD."
)

EXPECTED_ATTENDEES = ["sarah", "dev", "ana"]
EXPECTED_ACTION_ITEMS = [
    {"item": "design specs", "owner": "ana"},
    {"item": "mockup", "owner": "ana"},
    {"item": "api docs", "owner": "sarah"},
    {"item": "backend", "owner": "sarah"},
]

CLAUDE_INPUT_COST_PER_1M = 0.80
CLAUDE_OUTPUT_COST_PER_1M = 4.00


def call_ollama(prompt):
    print(f"[Ollama] Sending meeting summary prompt to {OLLAMA_MODEL} ...")
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
    print(f"[Claude] Sending meeting summary prompt to {CLAUDE_MODEL} ...")
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
        return {"text": text, "elapsed": elapsed, "prompt_tokens": prompt_tokens,
                "output_tokens": output_tokens, "cost_usd": cost, "error": None}
    except Exception as exc:
        elapsed = time.time() - start
        print(f"[Claude] ERROR: {exc}")
        return {"text": "", "elapsed": elapsed, "prompt_tokens": 0,
                "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def score_response(text):
    if not text:
        return {"total": 0, "date_context": 0, "attendees": 0,
                "goal": 0, "action_ana": 0, "action_sarah": 0, "structure": 0}

    lower = text.lower()
    date_context = 1 if any(d in lower for d in ["15 jan", "january 15", "jan 15", "sprint planning"]) else 0
    found_attendees = sum(1 for a in EXPECTED_ATTENDEES if a in lower)
    attendees = min(found_attendees, 2)
    goal = 2 if all(kw in lower for kw in ["dashboard", "march"]) else (
        1 if any(kw in lower for kw in ["dashboard", "march", "end of march"]) else 0
    )
    action_ana = 0
    if "ana" in lower and any(kw in lower for kw in ["mockup", "design spec", "friday"]):
        action_ana = 2
    elif any(kw in lower for kw in ["mockup", "design spec"]):
        action_ana = 1
    action_sarah = 0
    if "sarah" in lower and any(kw in lower for kw in ["api doc", "backend", "eod", "end of day"]):
        action_sarah = 2
    elif any(kw in lower for kw in ["api doc", "backend"]):
        action_sarah = 1
    structure = 1 if any(m in text for m in ["- ", "* ", "1.", "##", "**", "Action"]) else 0
    total = date_context + attendees + goal + action_ana + action_sarah + structure
    return {"total": total, "date_context": date_context, "attendees": attendees,
            "goal": goal, "action_ana": action_ana, "action_sarah": action_sarah,
            "structure": structure}


def print_comparison(ollama_result, claude_result, ollama_score, claude_score):
    print("\n" + "=" * 70)
    print("  BENCHMARK RESULTS — Meeting Note Summariser")
    print("=" * 70)
    table = [
        ["Metric", f"Ollama ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"],
        ["Response Time (s)", f"{ollama_result['elapsed']:.2f}", f"{claude_result['elapsed']:.2f}"],
        ["Prompt Tokens", ollama_result["prompt_tokens"], claude_result["prompt_tokens"]],
        ["Output Tokens", ollama_result["output_tokens"], claude_result["output_tokens"]],
        ["Estimated Cost (USD)", "$0.000000 (local)", f"${claude_result['cost_usd']:.6f}"],
        ["--- QUALITY SCORES ---", "", ""],
        ["Date/context captured (0-1)", ollama_score["date_context"], claude_score["date_context"]],
        ["Attendees named (0-2)", ollama_score["attendees"], claude_score["attendees"]],
        ["Goal stated dashboard/March (0-2)", ollama_score["goal"], claude_score["goal"]],
        ["Ana action items captured (0-2)", ollama_score["action_ana"], claude_score["action_ana"]],
        ["Sarah action items captured (0-2)", ollama_score["action_sarah"], claude_score["action_sarah"]],
        ["Structured format (0-1)", ollama_score["structure"], claude_score["structure"]],
        ["TOTAL QUALITY SCORE (/10)", ollama_score["total"], claude_score["total"]],
        ["Error", ollama_result["error"] or "None", claude_result["error"] or "None"],
    ]
    print(tabulate(table[1:], headers=table[0], tablefmt="grid"))
    print("\n--- Ollama Summary ---")
    print(ollama_result["text"] or "(no response)")
    print("\n--- Claude Summary ---")
    print(claude_result["text"] or "(no response)")


def main():
    print("HO1 Sample 04 — Meeting Note Summariser Benchmark")
    print("Prompt: Sprint planning transcript — summarise + list action items...")
    print()
    ollama_result = call_ollama(PROMPT)
    claude_result = call_claude(PROMPT)
    ollama_score = score_response(ollama_result["text"])
    claude_score = score_response(claude_result["text"])
    print_comparison(ollama_result, claude_result, ollama_score, claude_score)
    results = {
        "sample": "04-meeting-summarization",
        "prompt": PROMPT,
        "expected_action_items": EXPECTED_ACTION_ITEMS,
        "ollama": {"model": OLLAMA_MODEL, **ollama_result, "quality_score": ollama_score},
        "claude": {"model": CLAUDE_MODEL, **claude_result, "quality_score": claude_score},
    }
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
