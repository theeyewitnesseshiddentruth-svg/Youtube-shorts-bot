import os
import requests
import random

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_hooks(count=6):
    """
    Generate viral YouTube Shorts hooks using OpenRouter.
    
    Args:
        count (int): Number of hooks to return.
    Returns:
        List[str]: Top hooks selected for virality.
    """
    prompt = (
        "Generate 50 viral YouTube Shorts hooks.\n"
        "Rules:\n"
        "- Maximum 10 words per hook\n"
        "- Curiosity-driven\n"
        "- Topics: money, psychology, truth, hidden knowledge\n"
        "- Format: one hook per line"
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # Extract text from response
    hooks_text = result["choices"][0]["message"]["content"]
    hooks = [
    re.sub(r'^\d+\.\s*', '', h).strip()
    for h in hooks_text.split("\n")
    if len(h.strip()) > 5
    ]
    
    # Optional: score hooks (simple random scoring for now)
    scored = [(hook, min(10, len(hook) // 2 + 5)) for hook in hooks_list]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    if len(hooks_list) < count:
        return hooks_list
    return random.sample(hooks_list, count)
