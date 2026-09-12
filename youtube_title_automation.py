import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

VIDEO_ID = "ضع_ايدي_الفيديو_هنا"
TITLE_FORMAT = "الفيديو ده عنده {views} مشاهدة… وأنا هكرت اليوتيوب 😂"

creds = Credentials(
    None,
    refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    token_uri="https://oauth2.googleapis.com/token"
)

youtube = build("youtube", "v3", credentials=creds)

# قراءة رخيصة (1 وحدة بس)
video_response = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID).execute()
video = video_response["items"][0]
current_views = video["statistics"]["viewCount"]
snippet = video["snippet"]
current_title = snippet["title"]

# نشوف الرقم المكتوب في العنوان الحالي فعلاً
match = re.search(r"\d+", current_title.replace(",", ""))
title_views = match.group() if match else None

if title_views == str(current_views):
    print(f"مفيش تغيير، لسه {current_views} مشاهدة.")
else:
    new_title = TITLE_FORMAT.format(views=current_views)
    snippet["title"] = new_title
    youtube.videos().update(part="snippet", body={"id": VIDEO_ID, "snippet": snippet}).execute()
    print(f"اتحدث العنوان لـ: {new_title}")
