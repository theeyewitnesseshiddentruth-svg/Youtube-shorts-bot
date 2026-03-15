import os
import openai
import base64

openai.api_key = os.getenv("OPENAI_KEY")

def generate_image(prompt, index):
    """
    Generate a PNG image from a scene prompt
    """
    result = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_bytes = result.data[0].b64_json
    file_name = f"output/scene_{index}.png"
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(image_bytes))

    return file_name
