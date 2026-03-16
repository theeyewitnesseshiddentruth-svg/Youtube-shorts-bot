import os
from PIL import Image
import requests
from io import BytesIO

def generate_image(prompt, index, output_dir="output/images"):
    """
    Generate an image from a text prompt and save it locally.

    Args:
        prompt (str): The scene description for the image.
        index (int): Index of the scene (used for filename).
        output_dir (str): Directory to save generated images.

    Returns:
        str: Path to the saved image.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # === Placeholder for AI image generation API ===
    # For now, we generate a blank placeholder image
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    
    # Optionally, you can draw the prompt text on the image for testing
    # from PIL import ImageDraw
    # draw = ImageDraw.Draw(img)
    # draw.text((50, 50), prompt, fill=(255, 255, 255))
    
    file_path = os.path.join(output_dir, f"scene_{index}.png")
    img.save(file_path)
    
    # === If you integrate an API, you would replace the above with API call ===
    # Example: send `prompt` to API and save the returned image
    
    return file_path
