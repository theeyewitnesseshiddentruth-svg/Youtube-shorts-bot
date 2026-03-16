import os
import requests
import random

# Read API key from environment
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_hooks(count=6):
    """
    Generate top YouTube Shorts hooks using OpenRouter API.

    Args:
        count (int): Number of hooks to return (top scoring).

    Returns:
        list[str]: List of hooks.
    """
    # Prompt to generate 50 viral hooks
    prompt = """
Generate 50 viral YouTube Shorts hooks.
Rules:
- Maximum 10 words
- Curiosity-driven
- Topics: money, psychology, truth, hidden knowledge
- Format: one hook per line
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 1000
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()

    # Extract text
    hooks_text = data["choices"][0]["message"]["content"]
    hooks_list = [h.strip("- ").strip() for h in hooks_text.split("\n") if len(h.strip()) > 5]

    # Optional: score hooks (simple random scoring for now)
    scored = [(hook, min(10, len(hook) // 2 + 5)) for hook in hooks_list]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return top `count` hooks
    top_hooks = [hook for hook, score in scored[:count]]
    return top_hooks
