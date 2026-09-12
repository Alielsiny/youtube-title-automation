import os
import re
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

VIDEO_ID = "XdYWM7KoZFM"
TITLE_FORMAT = "الفيديو ده عنده ({views})مشاهده"

creds = Credentials(
    None,
    refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    token_uri="https://oauth2.googleapis.com/token"
)
youtube = build("youtube", "v3", credentials=creds)

# محاولة القراءة المجانية (ممكن تنجح أو تفشل، مفيش مشكلة في الحالتين)
current_views = None
try:
    page = requests.get(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"},
        cookies={"CONSENT": "YES+1"},
        timeout=10
    ).text
    m = re.search(r'"viewCount":"(\d+)"', page)
    if m:
        current_views = m.group(1)
except Exception:
    pass

# القراءة المضمونة من API الرسمي (احتياطي، وبرضو مصدرنا الأساسي للعنوان الحالي)
video_response = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID).execute()
video = video_response["items"][0]
snippet = video["snippet"]

if current_views is None:
    current_views = video["statistics"]["viewCount"]
    print("الـ scraping فشل، استخدمنا الـ API الرسمي بدالًا منه.")
else:
    print("الـ scraping نجح! وفرنا كوته.")

current_title = snippet["title"]
old_number_match = re.search(r"\d+", current_title.replace(",", ""))
old_number = old_number_match.group() if old_number_match else None

if old_number == current_views:
    print(f"مفيش تغيير، لسه {current_views} مشاهدة.")
else:
    new_title = TITLE_FORMAT.format(views=current_views)
    snippet["title"] = new_title
    youtube.videos().update(part="snippet", body={"id": VIDEO_ID, "snippet": snippet}).execute()
    print(f"اتحدث العنوان لـ: {new_title}")
