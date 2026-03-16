import os
import subprocess

def build_video_ffmpeg(images, audio_file, output_file, duration_per_image=3):
    """
    Build a video from images and an audio file using FFmpeg.
    
    Args:
        images (list): List of image file paths.
        audio_file (str): Path to narration audio (mp3/wav).
        output_file (str): Output video path (mp4).
        duration_per_image (int, optional): Duration each image shows in seconds.
    Returns:
        str: Path to the output video.
    """
    # Create temporary text file for FFmpeg
    temp_file = "temp_images.txt"
    with open(temp_file, "w") as f:
        for img in images:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {duration_per_image}\n")
        # Repeat last image for proper ending
        f.write(f"file '{os.path.abspath(images[-1])}'\n")

    # Step 1: Create silent video from images
    temp_video = "temp_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", temp_file,
        "-vsync", "vfr", "-pix_fmt", "yuv420p", temp_video
    ], check=True)

    # Step 2: Merge audio with video
    subprocess.run([
        "ffmpeg", "-y", "-i", temp_video, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
    ], check=True)

    # Clean up temporary files
    os.remove(temp_video)
    os.remove(temp_file)

    return output_file
