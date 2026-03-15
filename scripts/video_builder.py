from moviepy.editor import ImageClip, concatenate_videoclips

def build_video(images):
    clips = [ImageClip(img).set_duration(4) for img in images]
    video = concatenate_videoclips(clips)
    output_file = "output/video.mp4"
    video.write_videofile(output_file, fps=24)
    return output_file
