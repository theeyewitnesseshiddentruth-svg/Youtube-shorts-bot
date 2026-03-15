from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip

def build_video(audio_file, output_file="output/short.mp4"):
    clip = VideoFileClip("assets/videos/background.mp4").subclip(0,20)
    audio = AudioFileClip(audio_file)
    
    clip = clip.set_audio(audio)
    
    # Optional: add subtitle overlay
    txt_clip = TextClip("subscribe and like for more!", fontsize=40, color='white')
    txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)
    
    final = CompositeVideoClip([clip, txt_clip])
    final.write_videofile(output_file, fps=24)
    return output_file
