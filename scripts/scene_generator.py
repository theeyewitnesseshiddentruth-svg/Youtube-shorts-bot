def generate_scenes(script_text, max_scenes=5):
    """
    Generate descriptive scene prompts from a script.
    
    Args:
        script_text (str): The text of the short video script.
        max_scenes (int): Maximum number of scenes to generate.
    
    Returns:
        List[str]: A list of scene prompts for image generation.
    """
    # Split script into sentences
    sentences = [s.strip() for s in script_text.replace("\n", " ").split(". ") if s.strip()]
    
    # Limit the number of scenes
    scenes = sentences[:max_scenes]
    
    # Convert sentences into image-friendly prompts
    scene_prompts = []
    for sentence in scenes:
        prompt = f"Illustration for: {sentence}, cinematic, high quality, vibrant colors, 16:9"
        scene_prompts.append(prompt)
    
    return scene_prompts
