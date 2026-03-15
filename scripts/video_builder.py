def build_ai_video(video_prompt, audio_file):
    """
    Generates a video using an AI video model (RunDiffusion / Pika Labs / Gen-2) 
    from the prompt, then overlays the AI-generated voice.
    """
    # Pseudo-code for AI video generation
    video_file = f"output/{hash(video_prompt)}.mp4"
    
    # Call your AI video generation API here
    # video_file = ai_video_api.generate(prompt=video_prompt, duration=20)
    
    # Combine with audio using MoviePy
    from moviepy.editor import VideoFileClip, AudioFileClip
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    
    final_clip.write_videofile(video_file, fps=24)
    return video_file
