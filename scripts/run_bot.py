import os
from hooks import generate_hooks
from scene_generator import generate_scenes
from image_generator import generate_image
from video_builder import build_video
from moviepy.editor import AudioFileClip, CompositeVideoClip, TextClip
from elevenlabs import generate, set_api_key
import os

# Set API key from GitHub secrets
set_api_key(os.getenv("ELEVENLABS_KEY"))

def generate_ai_voice(text, file_name):
    """
    Generate MP3 narration for given text
    """
    audio_bytes = generate(
        text=text,
        voice="alloy",  # You can pick any ElevenLabs voice
        model="eleven_multilingual_v1"
    )

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name

# --------------------------
# Step 1: Generate top 6 hooks
# --------------------------
hooks = generate_hooks(count=6)
print("Selected hooks:", hooks)

for i, hook in enumerate(hooks):
    print(f"\n--- Generating Short {i+1} ---")
    
    # --------------------------
    # Step 2: Generate script
    # --------------------------
    # Here we just use hook as script for simplicity
    script = hook + " - explained in short video format"
    
    # --------------------------
    # Step 3: Generate scene prompts
    # --------------------------
    scenes = generate_scenes(script)
    print("Scene prompts:", scenes)
    
    # --------------------------
    # Step 4: Generate AI images for scenes
    # --------------------------
    images = []
    for idx, scene in enumerate(scenes):
        img_path = generate_image(scene, idx)
        images.append(img_path)
    
    # --------------------------
    # Step 5: Build video
    # --------------------------
    video_file = build_video(images)
    
    # --------------------------
    # Step 6: Generate AI voice
    # --------------------------
    audio_file = f"output/voice_{i}.mp3"
    voice_audio = generate_ai_voice(text=script, voice="alloy")
    with open(audio_file, "wb") as f:
        f.write(voice_audio)
    
    # --------------------------
    # Step 7: Combine video + audio
    # --------------------------
    video_clip = CompositeVideoClip([video_file])
    audio_clip = AudioFileClip(audio_file)
    final_video = video_clip.set_audio(audio_clip)
    
    final_output = f"output/short_{i+1}.mp4"
    final_video.write_videofile(final_output, fps=24)
    
    print(f"Short {i+1} generated:", final_output)

    # --------------------------
    # Step 8: Add subtitles & thumbnail
    # --------------------------
    # (Optional: you can auto-generate subtitles using your AI or ElevenLabs script)
    # (Optional: thumbnail generation can be added similarly)

    # --------------------------
    # Step 9: Upload to YouTube
    # --------------------------
    # Make sure YOUTUBE_KEY is set and uploader.py is ready
    # from uploader import upload_video
    # upload_video(final_output, title=hook)
    
print("\nAll 6 Shorts generated successfully!")
