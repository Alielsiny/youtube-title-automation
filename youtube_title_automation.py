from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

VIDEO_ID = "XdYWM7KoZFM"

credentials = Credentials(
    token=None,
    refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/youtube"]
)

youtube = build("youtube", "v3", credentials=credentials)

video = youtube.videos().list(
    part="snippet,statistics",
    id=VIDEO_ID
).execute()["items"][0]

views = int(video["statistics"].get("viewCount", 0))

new_title = f"الفيديو ده عنده {views} مشاهدة… وأنا هكرت اليوتيوب 😂"

if video["snippet"]["title"] != new_title:
    video["snippet"]["title"] = new_title

    youtube.videos().update(
        part="snippet",
        body={
            "id": VIDEO_ID,
            "snippet": video["snippet"]
        }
    ).execute()

    print("تم تحديث العنوان:", new_title)
else:
    print("العنوان بالفعل محدث:", new_title)
