import os
import subprocess
from hooks import generate_hooks
from scene_generator import generate_scenes
from image_generator import generate_image
from video_builder import build_video_ffmpeg
from elevenlabs import generate, set_api_key
from uploader import upload_video
from PIL import Image

# --------------------------
# Setup ElevenLabs API key
# --------------------------
set_api_key(os.getenv("ELEVENLABS_KEY"))

# --------------------------
# Generate AI voice
# --------------------------
def generate_ai_voice(text, file_name):
    """Generate MP3 narration for given text using ElevenLabs."""
    audio_bytes = generate(
        text=text,
        voice="alloy",
        model="eleven_multilingual_v1"
    )
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

def build_video_ffmpeg(images, audio_file, output_file, duration_per_image=3):
    """
    Build video from images and audio using FFmpeg.
    Each image lasts `duration_per_image` seconds.
    """
    # Create a temporary text file for FFmpeg image input
    with open("temp_images.txt", "w") as f:
        for img in images:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {duration_per_image}\n")
        # Repeat last image for proper ending
        f.write(f"file '{os.path.abspath(images[-1])}'\n")

    # FFmpeg command to create video from images
    video_temp = "temp_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "temp_images.txt",
        "-vsync", "vfr", "-pix_fmt", "yuv420p", video_temp
    ], check=True)

    # Merge audio with video
    subprocess.run([
        "ffmpeg", "-y", "-i", video_temp, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
    ], check=True)

    # Clean up temp files
    os.remove(video_temp)
    os.remove("temp_images.txt")
    return output_file

# --------------------------
# Generate subtitles (SRT)
# --------------------------
def generate_subtitles(script, output_srt, duration_per_line=3):
    lines = script.split(". ")
    with open(output_srt, "w") as f:
        for i, line in enumerate(lines):
            start_time = i * duration_per_line
            end_time = (i + 1) * duration_per_line
            start_hms = f"{start_time//3600:02}:{(start_time%3600)//60:02}:{start_time%60:02},000"
            end_hms = f"{end_time//3600:02}:{(end_time%3600)//60:02}:{end_time%60:02},000"
            f.write(f"{i+1}\n{start_hms} --> {end_hms}\n{line}\n\n")
    return output_srt

# --------------------------
# Generate thumbnail
# --------------------------
def generate_thumbnail(image_path, output_thumb, size=(1280, 720)):
    img = Image.open(image_path)
    img = img.resize(size)
    img.save(output_thumb)
    return output_thumb

# --------------------------
# Burn subtitles onto video
# --------------------------
def burn_subtitles(video_file, srt_file, output_file):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-vf", f"subtitles={srt_file}",
        "-c:a", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file

# --------------------------
# Step 1: Generate top 6 hooks
# --------------------------
hooks = generate_hooks(count=6)
print("Selected hooks:", hooks)

for i, hook in enumerate(hooks):
    print(f"\n--- Generating Short {i+1} ---")
    
    # Step 2: Generate script
    script = f"{hook} - explained in short video format"
    
    # Step 3: Generate scene prompts
    scenes = generate_scenes(script)
    print("Scene prompts:", scenes)
    # Step 4: Generate AI images for scenes
    images = []
    for idx, scene in enumerate(scenes):
        img_path = generate_image(scene, idx)
        images.append(img_path)
    # Step 5: Generate AI voice
    audio_file = f"output/voice_{i}.mp3"
    generate_ai_voice(script, audio_file)
    
    # Step 6: Build video using FFmpeg
    video_file = f"output/short_{i+1}.mp4"
    build_video_ffmpeg(images, audio_file, video_file, duration_per_image=3)
    
    # Step 7: Generate subtitles
    srt_file = f"output/subs_{i+1}.srt"
    generate_subtitles(script, srt_file)
    
    # Step 8: Burn subtitles onto video
    video_with_subs = f"output/short_{i+1}_sub.mp4"
    burn_subtitles(video_file, srt_file, video_with_subs)
    
    # Step 9: Generate thumbnail (from first scene)
    thumbnail_file = f"output/thumb_{i+1}.png"
    generate_thumbnail(images[0], thumbnail_file)
    
    # Step 10: Upload to YouTube
    upload_video(
        video_with_subs,
        title=hook,
        description="AI Generated Shorts",
        tags=["shorts"],
        thumbnail=thumbnail_file
    )

print("\nAll 6 Shorts generated successfully!")
