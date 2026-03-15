from googleapiclient.discovery import build
import os

def upload_video(file, title, description="Shorts Video", tags=["shorts"]):
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_KEY"))
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=file
    )
    request.execute()
