"""
HO1 Sample 04 — Document Redaction  (OPTIONAL automation)
============================================================
You do NOT need this file for the course.

The course uses your Claude.ai subscription — just follow the README:
run the example prompt in LM Studio and in Claude.ai, then score in index.html.
No API key needed for that path.

This script is only for learners who later want to run the same comparison
automatically. It calls a local model (LM Studio / Ollama) AND Claude via the
Anthropic API. The API key is SEPARATE from your Claude.ai subscription and costs
money — see the README section "Optional — automate it with the API (advanced)".
"""

import os
import time
import json
import requests

try:
    import anthropic
except ImportError:
    anthropic = None
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# --- Configuration ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

PROMPT = 'You are a privacy redaction tool. Rewrite the text below, replacing every piece of personally identifiable information with a label in square brackets: [NAME], [DATE_OF_BIRTH], [ADDRESS], [PHONE], [EMAIL], [ID_NUMBER]. Keep all medical and clinical details exactly as written — do NOT redact symptoms, diagnoses, or medication names.\n\nText:\n"Patient Maria Gonzalez, DOB 03/07/1984, lives at 42 Elm Street, Leeds. Phone 07700 900123, email maria.g@example.com. NHS number 945 220 1864. Diagnosed with type 2 diabetes; prescribed metformin 500mg twice daily."'

# Rough Claude Haiku pricing (USD per 1M tokens) — for the optional cost estimate only.
CLAUDE_INPUT_COST_PER_1M = 1.00
CLAUDE_OUTPUT_COST_PER_1M = 5.00


def call_ollama(prompt: str) -> dict:
    print(f"[Local] Sending prompt to {OLLAMA_MODEL} ...")
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        elapsed = time.time() - start
        print(f"[Local] Done in {elapsed:.2f}s.")
        return {"text": data.get("response", ""), "elapsed": elapsed,
                "output_tokens": data.get("eval_count", 0), "cost_usd": 0.0, "error": None}
    except requests.exceptions.ConnectionError:
        msg = f"Cannot reach a local model at {OLLAMA_BASE_URL}. Start LM Studio's local server or run 'ollama serve'."
        print(f"[Local] ERROR: {msg}")
        return {"text": "", "elapsed": 0.0, "output_tokens": 0, "cost_usd": 0.0, "error": msg}
    except Exception as exc:
        print(f"[Local] ERROR: {exc}")
        return {"text": "", "elapsed": 0.0, "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def call_claude(prompt: str) -> dict:
    print(f"[Claude] Sending prompt to {CLAUDE_MODEL} ...")
    if anthropic is None:
        return {"text": "", "elapsed": 0.0, "output_tokens": 0, "cost_usd": 0.0,
                "error": "anthropic package not installed (pip install -r requirements.txt)"}
    if not ANTHROPIC_API_KEY:
        msg = "ANTHROPIC_API_KEY is not set. This optional script needs an API key (separate from Claude.ai)."
        print(f"[Claude] {msg}")
        return {"text": "", "elapsed": 0.0, "output_tokens": 0, "cost_usd": 0.0, "error": msg}
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    start = time.time()
    try:
        message = client.messages.create(
            model=CLAUDE_MODEL, max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed = time.time() - start
        in_t = message.usage.input_tokens
        out_t = message.usage.output_tokens
        cost = in_t / 1_000_000 * CLAUDE_INPUT_COST_PER_1M + out_t / 1_000_000 * CLAUDE_OUTPUT_COST_PER_1M
        print(f"[Claude] Done in {elapsed:.2f}s. Cost: ${cost:.6f}")
        return {"text": message.content[0].text, "elapsed": elapsed,
                "output_tokens": out_t, "cost_usd": cost, "error": None}
    except Exception as exc:
        print(f"[Claude] ERROR: {exc}")
        return {"text": "", "elapsed": 0.0, "output_tokens": 0, "cost_usd": 0.0, "error": str(exc)}


def score_response(text: str) -> dict:
    """Simple, deterministic heuristics for the Document Redaction task (max 4)."""
    if not text:
        return {"names_removed": 0, "ids_removed": 0, "contacts_removed": 0, "medical_kept": 0, "total": 0}
    lower = text.lower()
    names = 1 if "gonzalez" not in lower and "[name]" in lower else 0
    ids = 1 if ("945" not in text) and ("[id" in lower or "[date" in lower) else 0
    contacts = 1 if ("example.com" not in lower and "900123" not in text) else 0
    medical = 1 if ("diabetes" in lower and "metformin" in lower) else 0
    return {"names_removed": names, "ids_removed": ids, "contacts_removed": contacts,
            "medical_kept": medical, "total": names+ids+contacts+medical}


def print_comparison(local_r, claude_r, local_s, claude_s):
    print("\n" + "=" * 64)
    print("  BENCHMARK RESULTS — Document Redaction")
    print("=" * 64)
    rows = [
        ["Response time (s)", f"{local_r['elapsed']:.2f}", f"{claude_r['elapsed']:.2f}"],
        ["Estimated cost (USD)", "$0.00 (local)", f"${claude_r['cost_usd']:.6f}"],
    ]
    for k in [k for k in local_s if k != "total"]:
        rows.append([k.replace("_", " ").title(), local_s[k], claude_s[k]])
    rows.append(["TOTAL SCORE (/4)", local_s["total"], claude_s["total"]])
    rows.append(["Error", local_r["error"] or "None", claude_r["error"] or "None"])
    headers = ["Metric", f"Local ({OLLAMA_MODEL})", f"Claude ({CLAUDE_MODEL})"]
    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("\t".join(headers))
        for r in rows:
            print("\t".join(str(c) for c in r))
    print("\n--- Local response ---\n" + (local_r["text"] or "(none)"))
    print("\n--- Claude response ---\n" + (claude_r["text"] or "(none)"))


def main():
    print("HO1 Sample 04 — Document Redaction (optional benchmark)")
    print(f"Prompt: {PROMPT[:70]}...\n")
    local_r = call_ollama(PROMPT)
    claude_r = call_claude(PROMPT)
    local_s = score_response(local_r["text"])
    claude_s = score_response(claude_r["text"])
    print_comparison(local_r, claude_r, local_s, claude_s)
    out = {"sample": "04-document-redaction", "prompt": PROMPT,
           "local": {"model": OLLAMA_MODEL, **local_r, "score": local_s},
           "claude": {"model": CLAUDE_MODEL, **claude_r, "score": claude_s}}
    path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {path}")


if __name__ == "__main__":
    main()
