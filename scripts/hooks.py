import os
import requests
import random

# --------------------------
# OpenRouter setup
# --------------------------
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")  # GitHub secret name
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_hooks(count=6):
    """
    Generate viral YouTube Shorts hooks using OpenRouter.
    Returns a list of top `count` hooks.
    """
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
        "max_tokens": 500
    }

    response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    # OpenRouter returns the content in choices[0].message.content
    hooks_text = data["choices"][0]["message"]["content"]
    hooks = [h.strip("- ").strip() for h in hooks_text.split("\n") if len(h.strip()) > 5]

    # Simple scoring: randomly pick top `count` hooks for now
    random.shuffle(hooks)
    best_hooks = hooks[:count]

    return best_hooks
