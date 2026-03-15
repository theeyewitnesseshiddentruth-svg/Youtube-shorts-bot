import subprocess
import os

def build_video_ffmpeg(images, audio_file, output_file, duration_per_image=3, subtitles_file=None):
    """
    Build a video from images + audio using FFmpeg.
    Optionally adds subtitles.
    
    images: list of image file paths
    audio_file: path to MP3 narration
    output_file: final MP4 path
    duration_per_image: seconds per image
    subtitles_file: optional .srt file path
    """
    if not images:
        raise ValueError("No images provided for video creation.")

    # Step 1: Create a temporary text file listing images for FFmpeg
    list_file = "temp_images.txt"
    with open(list_file, "w") as f:
        for img in images:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {duration_per_image}\n")
        # Repeat last image to avoid early cut
        f.write(f"file '{os.path.abspath(images[-1])}'\n")

    # Step 2: Build base video from images
    temp_video = "temp_video.mp4"
    cmd_video = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-vsync", "vfr",
        "-pix_fmt", "yuv420p",
        temp_video
    ]
    subprocess.run(cmd_video, check=True)

    # Step 3: Merge audio with video
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_file
    ]
    subprocess.run(cmd_merge, check=True)

    # Step 4: Optional subtitles overlay
    if subtitles_file and os.path.exists(subtitles_file):
        temp_subbed = "temp_subbed.mp4"
        cmd_subs = [
            "ffmpeg", "-y",
            "-i", output_file,
            "-vf", f"subtitles={subtitles_file}",
            "-c:a", "copy",
            temp_subbed
        ]
        subprocess.run(cmd_subs, check=True)
        os.replace(temp_subbed, output_file)

    # Step 5: Cleanup temporary files
    os.remove(list_file)
    if os.path.exists(temp_video):
        os.remove(temp_video)

    print(f"Video created: {output_file}")
    return output_file


def create_thumbnail(image_file, output_thumb):
    """
    Create a thumbnail (resized) for YouTube upload.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", image_file,
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
        "-vframes", "1",
        output_thumb
    ]
    subprocess.run(cmd, check=True)
    print(f"Thumbnail created: {output_thumb}")
    return output_thumb
