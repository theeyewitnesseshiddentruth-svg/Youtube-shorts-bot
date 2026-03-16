import os
from hooks import generate_hooks
from scene_generator import generate_scenes
from image_generator import generate_image
from video_builder import build_video_ffmpeg
from uploader import upload_video
from elevenlabs import generate, set_api_key

# --------------------------
# Setup ElevenLabs API key
# --------------------------
set_api_key(os.getenv("ELEVENLABS_KEY"))

# --------------------------
# Generate AI voice
# --------------------------
def generate_ai_voice(text, file_name):
    """
    Generate MP3 narration for a given text using ElevenLabs.
    """
    audio_bytes = generate(
        text=text,
        voice="alloy",  # change voice if you want
        model="eleven_multilingual_v1"
    )
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

# --------------------------
# Main bot loop
# --------------------------
def main():
    hooks = generate_hooks(count=6)
    print("Selected hooks:", hooks)

    for i, hook in enumerate(hooks):
        print(f"\n--- Generating Short {i+1} ---")
        
        # Generate script (you can expand this logic later)
        script = f"{hook} - explained in short video format"
        
        # Generate scene prompts
        scenes = generate_scenes(script)
        print("Scene prompts:", scenes)
        
        # Generate AI images for scenes
        images = [generate_image(scene, idx) for idx, scene in enumerate(scenes)]
        
        # Generate AI voice narration
        audio_file = f"output/voice_{i}.mp3"
        generate_ai_voice(script, audio_file)
        
        # Build video
        output_video = f"output/short_{i+1}.mp4"
        build_video_ffmpeg(images, audio_file, output_video, duration_per_image=3)
        
        # Upload video
        upload_video(
            output_video,
            title=hook,
            description="AI Generated Shorts",
            tags=["shorts"]
        )
    
    print("\nAll 6 Shorts generated successfully!")

if __name__ == "__main__":
    main()
