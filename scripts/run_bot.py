import os
import random
import time
from hooks import generate_hooks
from scene_generator import generate_scenes
from image_generator import generate_image
from video_builder import build_video
from moviepy.editor import AudioFileClip, CompositeVideoClip, TextClip
from elevenlabs import generate, set_api_key
from uploader import upload_video
from PIL import Image, ImageDraw, ImageFont

# --------------------------
# Set API key
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
# Generate thumbnail
# --------------------------
def generate_thumbnail(title, file_name):
    img = Image.new('RGB', (1280, 720), color=(20, 20, 20))
    d = ImageDraw.Draw(img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        font = ImageFont.truetype(font_path, 80)
    except:
        font = ImageFont.load_default()
    d.text((50, 300), title, font=font, fill=(255, 255, 0))
    img.save(file_name)
    return file_name

# --------------------------
# Random delay for natural posting (0–10 minutes)
# --------------------------
delay_seconds = random.randint(0, 600)
print(f"Delaying upload by {delay_seconds} seconds for natural posting...")
time.sleep(delay_seconds)

# --------------------------
# Generate top 6 hooks
# --------------------------
hooks = generate_hooks(count=6)
print("Selected hooks:", hooks)

for i, hook in enumerate(hooks):
    print(f"\n--- Generating Short {i+1} ---")

    # Script
    script = f"{hook} - explained in short video format"

    # Scene prompts
    scenes = generate_scenes(script)
    print("Scene prompts:", scenes)

    # Generate AI images
    images = []
    for idx, scene in enumerate(scenes):
        img_path = generate_image(scene, idx)
        images.append(img_path)

    # Build video
    video_file = build_video(images)

    # Generate AI voice
    audio_file = f"output/voice_{i}.mp3"
    generate_ai_voice(script, audio_file)

    # Combine video + audio
    video_clip = CompositeVideoClip([video_file])
    audio_clip = AudioFileClip(audio_file)
    final_video = video_clip.set_audio(audio_clip)

    # Add simple subtitles per scene
    subtitle_clips = []
    for idx, scene in enumerate(scenes):
        txt_clip = TextClip(
            scene,
            fontsize=40,
            color='white',
            method='caption',
            size=(1280, 100)
        )
        txt_clip = txt_clip.set_start(idx*4).set_duration(4)
        subtitle_clips.append(txt_clip)

    final_video = CompositeVideoClip([final_video, *subtitle_clips])

    # Write final video
    final_output = f"output/short_{i+1}.mp4"
    final_video.write_videofile(final_output, fps=24)

    # Generate thumbnail
    thumbnail_file = f"output/thumbnail_{i+1}.png"
    generate_thumbnail(hook, thumbnail_file)

    # Upload to YouTube
    upload_video(final_output, title=hook, description="AI Generated Shorts", tags=["shorts"])

print("\nAll 6 Shorts generated successfully!")
