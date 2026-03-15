import random
import json

def pick_style_and_prompt(hook):
    with open("assets/styles.json") as f:
        styles = json.load(f)
    
    # Mood detection (simple keyword-based)
    hook_lower = hook.lower()
    if any(word in hook_lower for word in ["truth", "money", "secret"]):
        mood = "serious"
    elif any(word in hook_lower for word in ["fun", "crazy", "shocking"]):
        mood = "funny"
    else:
        mood = "informative"
    
    possible_styles = [s for s in styles if s["mood"] == mood]
    if not possible_styles:
        possible_styles = styles
    
    choice = random.choice(possible_styles)
    style = choice["style"]
    
    # AI prompt: combines hook + style for video generation
    video_prompt = f"Create a 20-second {style} video illustrating: {hook}"
    return style, video_prompt
