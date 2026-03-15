import os
import openai
import random

# Set API key from environment
openai.api_key = os.getenv("OPENAI_KEY")

def hooks(count=6):
    """
    Generate 'count' viral hooks using OpenAI GPT
    """

    # Step 1: Generate 50 hooks
    prompt = f"""
Generate 50 viral YouTube Shorts hooks.

Rules:
- Maximum 10 words
- Curiosity-driven
- Topics: money, psychology, truth, hidden knowledge
- Format: one hook per line
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    hooks_text = response.choices[0].message.content
    hooks = [h.strip("- ").strip() for h in hooks_text.split("\n") if len(h.strip()) > 5]

    # Step 2: Score hooks
    scored = []
    for hook in hooks:
        score_prompt = f"""
Score this YouTube Shorts hook from 1 to 10 for virality.

Hook: "{hook}"

Only return a number.
"""
        score_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": score_prompt}],
            temperature=0
        )
        try:
            score = int(score_resp.choices[0].message.content.strip())
        except:
            score = 5
        scored.append((hook, score))

    # Step 3: Select top hooks and temporarily save to hooks.py 
    scored.sort(key=lambda x: x[1], reverse=True)
    best_hooks = [hook for hook, score in scored[:count]]

    return best_hooks
