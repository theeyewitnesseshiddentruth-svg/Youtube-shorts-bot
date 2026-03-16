import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Get API key from GitHub secrets
YOUTUBE_API_KEY = os.getenv("YOUTUBE_KEY")

def upload_video(video_path, title, description="", tags=None, thumbnail=None):
    """
    Uploads a video to YouTube using the API.
    
    Args:
        video_path (str): Path to video file.
        title (str): Video title.
        description (str): Video description.
        tags (list): Optional list of tags.
        thumbnail (str): Optional path to a custom thumbnail.
    """
    tags = tags or []
    
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    print(f"Video uploaded: {response['id']}")

    if thumbnail:
        youtube.thumbnails().set(
            videoId=response['id'],
            media_body=MediaFileUpload(thumbnail)
        ).execute()
        print("Thumbnail uploaded.")

    return response['id']
