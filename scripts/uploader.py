import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():

    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                SCOPES
            )
            credentials = flow.run_console()

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


def upload_video(file, title, description="Shorts Video", tags=["shorts"]):

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(file)
    )

    response = request.execute()

    print("Upload successful:", response["id"])
