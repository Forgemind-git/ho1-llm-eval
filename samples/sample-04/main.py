"""
HO1 Sample 04 — Document Redaction  (OPTIONAL convenience script)
============================================================
100% OFFLINE. No API key, no cloud, no Claude.

The course's primary path is no-code: run the example prompt on TWO local models
in the LM Studio chat UI, read off tokens/sec and model size, and fill in the
results table in index.html. You do NOT need this script.

This script is only an optional convenience. It sends the SAME prompt to two
local models through LM Studio's local OpenAI-compatible server (no key) and
prints a tokens/sec + accuracy comparison so you can reproduce the table.

Setup:
  1. In LM Studio, download the two models you want to compare.
  2. LM Studio -> Developer (Local Server) tab -> Start Server.
  3. pip install -r requirements.txt
  4. cp .env.example .env   # set MODEL_A / MODEL_B to the exact model IDs
  5. python main.py

Model size (GB) and RAM are read from the LM Studio UI — add them to index.html.
"""

import os
import time
import json
import requests

BASE_URL = os.environ.get("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
MODEL_A = os.environ.get("MODEL_A", "llama-3.2-1b-instruct")
MODEL_B = os.environ.get("MODEL_B", "qwen2.5-3b-instruct")

PROMPT = """\
You are a privacy redaction tool. Rewrite the text below, replacing every piece of personally identifiable information with a label in square brackets: [NAME], [DATE_OF_BIRTH], [ADDRESS], [PHONE], [EMAIL], [ID_NUMBER]. Keep all medical and clinical details exactly as written — do NOT redact symptoms, diagnoses, or medication names.

Text:
"Patient Maria Gonzalez, DOB 03/07/1984, lives at 42 Elm Street, Leeds. Phone 07700 900123, email maria.g@example.com. NHS number 945 220 1864. Diagnosed with type 2 diabetes; prescribed metformin 500mg twice daily."
"""


def score(text):
    t = text or ''
    tl = t.lower()
    masked = all(x not in tl for x in ['maria', 'elm street', 'maria.g@example.com']) \
        and all(x not in t for x in ['900123', '945 220 1864', '1984'])
    labels = t.count('[') >= 4
    medical = ('diabetes' in tl) and ('metformin' in tl)
    good = sum([masked, labels, medical])
    return {'All PII masked': masked, 'Labels used': labels, 'Medical preserved': medical, '_good': good, '_max': 3}


def run_model(model: str) -> dict:
    url = BASE_URL.rstrip("/") + "/chat/completions"
    payload = {"model": model, "messages": [{"role": "user", "content": PROMPT}], "temperature": 0.2}
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot reach LM Studio at {BASE_URL}. Open LM Studio -> Developer tab -> Start Server."}
    except Exception as exc:
        return {"error": str(exc)}
    elapsed = time.time() - start
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    out_tokens = (data.get("usage") or {}).get("completion_tokens") or len(text.split())
    tps = out_tokens / elapsed if elapsed > 0 else 0.0
    return {"text": text, "elapsed": elapsed, "tokens": out_tokens, "tps": tps, "error": None}


def main():
    print(f"HO1 Sample 04 — Document Redaction")
    print(f"Comparing two LOCAL models via LM Studio ({BASE_URL})\n")
    results = {}
    for label, model in [("A", MODEL_A), ("B", MODEL_B)]:
        print(f"[Model {label}] {model} ...")
        res = run_model(model)
        if res.get("error"):
            print(f"  ERROR: {res['error']}")
            res["score"] = {}
        else:
            res["score"] = score(res["text"])
            pct = round(100 * res["score"]["_good"] / res["score"]["_max"])
            print(f"  {res['tps']:.1f} tok/s · {res['tokens']} tokens · {res['elapsed']:.1f}s · accuracy {pct}%")
        res["model"] = model
        results[label] = res

    a, b = results["A"], results["B"]

    def col(res, key, fmt="{}"):
        return "n/a" if res.get("error") else fmt.format(res[key])

    def acc(res):
        if res.get("error"):
            return "n/a"
        return f"{round(100 * res['score']['_good'] / res['score']['_max'])}%"

    print("\n" + "=" * 58)
    print(f"{'Metric':<24}{'Model A':>17}{'Model B':>17}")
    print("-" * 58)
    print(f"{'Accuracy (rubric)':<24}{acc(a):>17}{acc(b):>17}")
    print(f"{'Tokens/sec':<24}{col(a, 'tps', '{:.1f}'):>17}{col(b, 'tps', '{:.1f}'):>17}")
    print(f"{'Response time (s)':<24}{col(a, 'elapsed', '{:.1f}'):>17}{col(b, 'elapsed', '{:.1f}'):>17}")
    print(f"{'Model size (GB)':<24}{'from LM Studio UI':>17}{'from LM Studio UI':>17}")
    print(f"{'RAM (GB)':<24}{'from LM Studio UI':>17}{'from LM Studio UI':>17}")
    print("=" * 58)
    print("\nAdd Model size (GB) and RAM from the LM Studio UI into index.html to complete the table.")

    out = {"sample": "04-document-redaction", "prompt": PROMPT,
           "model_a": {"model": a["model"], **{k: v for k, v in a.items() if k != "model"}},
           "model_b": {"model": b["model"], **{k: v for k, v in b.items() if k != "model"}}}
    path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"Results saved to {path}")


if __name__ == "__main__":
    main()
