import os
import openai
import random

# Set OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_KEY")

def generate_hooks(count=6):
    """
    Generate top viral YouTube Shorts hooks.
    
    Each hook is maximum 10 words, curiosity-driven, and 
    related to money, psychology, truth, or hidden knowledge.
    """
    prompt = f"""
Generate 50 short, viral YouTube Shorts hooks.
- Max 10 words
- Curiosity-driven
- Topics: money, psychology, truth, hidden knowledge
- Format: one hook per line
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        hooks_text = response.choices[0].message["content"]
        hooks = [h.strip("- ").strip() for h in hooks_text.split("\n") if len(h.strip()) > 5]
    except Exception as e:
        print("Error generating hooks:", e)
        hooks = [
            "Hidden money secrets you never knew",
            "Psychology tricks that change behavior fast",
            "Truth about hidden knowledge revealed",
            "Secrets wealthy people don’t want you to know",
            "Mind hacks to improve your life today",
            "The unseen forces controlling your choices"
        ]
    
    # Randomly select top `count` hooks
    if len(hooks) < count:
        count = len(hooks)
    best_hooks = random.sample(hooks, count)
    return best_hooks
