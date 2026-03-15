from hooks import generate_hook
from script_writer import generate_script
from voice import create_voice
from video_builder import build_video
from uploader import upload_video

def generate_short():
    hook = generate_hook()
    script = generate_script(hook)
    audio_file = create_voice(script)
    video_file = build_video(audio_file)
    upload_video(video_file, hook)
    print(f"Uploaded Short: {hook}")

if __name__ == "__main__":
    # Generate 6 Shorts per day
    for i in range(6):
        generate_short()
