import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load client secret from environment variable
client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")

if not client_secret:
    raise Exception("YOUTUBE_CLIENT_SECRET is not set in GitHub Secrets!")

# Save JSON to a temp file
with open("client_secret.json", "w") as f:
    f.write(client_secret)

# Scopes for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Run OAuth flow
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
credentials = flow.run_local_server(port=0)  # Will show Google auth link in Actions logs

# Build YouTube API service
youtube = build("youtube", "v3", credentials=credentials)

# Minimal video metadata (replace with your test video path)
request_body = {
    "snippet": {
        "title": "Test Upload",
        "description": "This is a test upload from GitHub Actions",
        "tags": ["test", "github", "bot"]
    },
    "status": {
        "privacyStatus": "private"
    }
}

# Path to a short test video (must exist in repo or fetch from URL)
video_file = "test.mp4"  # You need to upload a small test video named test.mp4

# Upload video
request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=video_file
)
response = request.execute()

print(f"Upload successful! Video ID: {response['id']}")
