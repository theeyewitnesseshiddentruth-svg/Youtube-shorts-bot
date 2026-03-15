import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generate_hooks(count=6):

    # Step 1: Generate many hooks
    prompt = """
Generate 50 viral YouTube Shorts hooks.

Rules:
- Maximum 10 words
- Curiosity driven
- Topics: money, psychology, truth, hidden knowledge
- One hook per line
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    hooks_text = response.choices[0].message.content
    hooks = [h.strip("- ").strip() for h in hooks_text.split("\n") if h.strip()]

    # Step 2: Score hooks
    scored = []

    for hook in hooks:

        score_prompt = f"""
Score this YouTube Shorts hook from 1 to 10 based on virality:

Hook: "{hook}"

Only return the number.
"""

        score_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": score_prompt}]
        )

        try:
            score = int(score_response.choices[0].message.content.strip())
        except:
            score = 5

        scored.append((hook, score))

    # Step 3: Sort hooks by score
    scored.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Select best hooks
    best_hooks = [hook for hook, score in scored[:count]]

    return best_hooks
