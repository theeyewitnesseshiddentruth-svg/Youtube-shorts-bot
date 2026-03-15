import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generate_script(hook):
    prompt = f"""
    Write a 20-second YouTube Shorts script with:
    Hook: {hook}
    Structure:
    Hook
    Curiosity
    Truth
    Call to action
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text
