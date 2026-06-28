"""
HO1 Sample — LLM Evaluation Starter
-------------------------------------
This file is a skeleton. Fill in the TODOs to run this benchmark programmatically.

For the course exercise, you do NOT need to run this file.
Use LM Studio and Claude.ai manually, then fill in index.html.

If you want to go further and automate it, complete the steps below.
"""

# TODO: import the libraries you need (e.g. anthropic, requests, time, json)

# TODO: define your test prompt
PROMPT = "[TODO: write your test prompt here]"

# TODO: define a function to call LM Studio / Ollama
def call_local_model(prompt: str) -> dict:
    """
    Call a local model via LM Studio or Ollama.
    Return a dict with keys: text, elapsed, error
    """
    # TODO: implement this
    raise NotImplementedError("Fill this in")

# TODO: define a function to call Claude.ai via the API
def call_claude(prompt: str) -> dict:
    """
    Call Claude via the Anthropic SDK.
    Return a dict with keys: text, elapsed, cost_usd, error
    """
    # TODO: implement this (requires ANTHROPIC_API_KEY env var)
    raise NotImplementedError("Fill this in")

# TODO: define a scoring function
def score_response(text: str) -> dict:
    """
    Score the model response against your rubric criteria.
    Return a dict with one key per criterion and a 'total' key.
    """
    # TODO: implement your scoring logic
    raise NotImplementedError("Fill this in")

def main():
    print("HO1 — LLM Evaluation Benchmark")
    print(f"Prompt: {PROMPT[:80]}...")
    print()

    # TODO: call both models
    local_result = call_local_model(PROMPT)
    claude_result = call_claude(PROMPT)

    # TODO: score both responses
    local_score = score_response(local_result.get("text", ""))
    claude_score = score_response(claude_result.get("text", ""))

    # TODO: print a comparison table
    print("Local model score:", local_score)
    print("Claude score:     ", claude_score)

    # TODO: save results to results.json

if __name__ == "__main__":
    main()
