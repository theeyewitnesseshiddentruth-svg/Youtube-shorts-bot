from hooks import generate_hooks
from style_picker import pick_style_and_prompt
from script_writer import generate_script
from voice import create_voice
from video_builder import build_ai_video
from thumbnail import create_thumbnail
from uploader import upload_video

# Generate 6 hooks
hooks = generate_hooks(6)

for i, hook in enumerate(hooks):
    # Pick style + generate AI video prompt
    style, video_prompt = pick_style_and_prompt(hook)
    
    # Generate AI script + voice
    script = generate_script(hook)
    audio_file = create_voice(script)
    
    # Generate AI video based on prompt + combine voice
    final_video = build_ai_video(video_prompt, audio_file)
    
    # Generate thumbnail
    create_thumbnail(hook)
    
    # Upload video at scheduled time (2-hour intervals)
    upload_video(final_video, hook, publish_delay_minutes=i*120)
    
    print(f"Short {i+1}/6 created: Hook='{hook}', Style='{style}'")
