import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

def generate_scenes(script):
    """
    Generate visual scene prompts for a given script
    """
    prompt = f"""
Break this YouTube Shorts script into 5 visual scenes.

Script:
{script}

Each scene: short cinematic description, easy to convert into an image.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    scenes_text = response.choices[0].message.content
    scenes = [s.strip("- ").strip() for s in scenes_text.split("\n") if len(s.strip()) > 5]

    return scenes
