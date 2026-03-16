import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# --------------------------
# YouTube Upload Function
# --------------------------
def upload_video(video_file, title, description="", tags=None, thumbnail=None):
    """
    Upload a video to YouTube.
    
    Args:
        video_file (str): Path to the video file.
        title (str): Video title.
        description (str, optional): Video description.
        tags (list, optional): List of tags.
        thumbnail (str, optional): Path to thumbnail image.
    
    Returns:
        dict: Response from YouTube API.
    """
    # Define API scope
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Load OAuth credentials from environment or local client_secret.json
    # For GitHub Actions, it's better to use a JSON secret
    client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS", "client_secret.json")

    # Run OAuth flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_console()
    
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
        }
    }

    # Upload video
    media_file = googleapiclient.http.MediaFileUpload(video_file)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()

    # Upload thumbnail if provided
    if thumbnail:
        youtube.thumbnails().set(
            videoId=response["id"],
            media_body=googleapiclient.http.MediaFileUpload(thumbnail)
        ).execute()

    print(f"Uploaded video: {title} (ID: {response['id']})")
    return response
