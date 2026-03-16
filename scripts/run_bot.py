import os
from hooks import generate_hooks
from scene_generator import generate_scenes
from image_generator import generate_image
from video_builder import build_video_ffmpeg
from uploader import upload_video
from elevenlabs import generate, set_api_key
from PIL import Image
import subprocess

# --------------------------
# Setup ElevenLabs API key
# --------------------------
set_api_key(os.getenv("ELEVENLABS_KEY"))

# --------------------------
# Generate AI voice
# --------------------------
def generate_ai_voice(text, file_name):
    audio_bytes = generate(
        text=text,
        voice="alloy",
        model="eleven_multilingual_v1"
    )
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

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
# Main bot loop
# --------------------------
def main():
    hooks = generate_hooks(count=6)
    print("Selected hooks:", hooks)

    for i, hook in enumerate(hooks):
        print(f"\n--- Generating Short {i+1} ---")
        
        script = f"{hook} - explained in short video format"
        scenes = generate_scenes(script)
        print("Scene prompts:", scenes)
        
        images = [generate_image(scene, idx) for idx, scene in enumerate(scenes)]
        
        audio_file = f"output/voice_{i}.mp3"
        generate_ai_voice(script, audio_file)
        
        # Build video
        video_file = f"output/short_{i+1}.mp4"
        build_video_ffmpeg(images, audio_file, video_file, duration_per_image=3)
        
        # Generate subtitles
        srt_file = f"output/subs_{i+1}.srt"
        generate_subtitles(script, srt_file)
        
        # Burn subtitles onto video
        video_with_subs = f"output/short_{i+1}_sub.mp4"
        burn_subtitles(video_file, srt_file, video_with_subs)
        
        # Generate thumbnail (optional)
        thumbnail_file = f"output/thumb_{i+1}.png"
        generate_thumbnail(images[0], thumbnail_file)
        
        # Upload video
        upload_video(
            video_with_subs,
            title=hook,
            description="AI Generated Shorts",
            tags=["shorts"],
            thumbnail=thumbnail_file
        )
    
    print("\nAll 6 Shorts generated successfully!")

if __name__ == "__main__":
    main()
