import os
import re
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

VIDEO_ID = "XdYWM7KoZFM"
TITLE_FORMAT = "الفيديو ده عنده ({views})مشاهده"

# قراءة مجانية - بنقرا صفحة الفيديو العامة (0 كوته)
page = requests.get(
    f"https://www.youtube.com/watch?v={VIDEO_ID}",
    headers={"User-Agent": "Mozilla/5.0"}
).text

views_match = re.search(r'"viewCount":"(\d+)"', page)
title_match = re.search(r'"title":"(.*?)","lengthSeconds"', page)

if not views_match:
    raise SystemExit("مقدرش أجيب عدد المشاهدات من الصفحة")

current_views = views_match.group(1)
current_title_on_page = title_match.group(1) if title_match else ""

old_number_match = re.search(r"\d+", current_title_on_page.replace(",", ""))
old_number = old_number_match.group() if old_number_match else None

if old_number == current_views:
    print(f"مفيش تغيير، لسه {current_views} مشاهدة. (0 كوته)")
else:
    new_title = TITLE_FORMAT.format(views=current_views)

    creds = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token"
    )
    youtube = build("youtube", "v3", credentials=creds)

    video_response = youtube.videos().list(part="snippet", id=VIDEO_ID).execute()
    snippet = video_response["items"][0]["snippet"]
    snippet["title"] = new_title

    youtube.videos().update(part="snippet", body={"id": VIDEO_ID, "snippet": snippet}).execute()
    print(f"اتحدث العنوان لـ: {new_title} (استهلك 51 وحدة)")
