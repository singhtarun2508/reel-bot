import requests
import os
from dotenv import load_dotenv

load_dotenv()

IG_USER_ID = os.getenv("IG_USER_ID")
TOKEN = os.getenv("IG_ACCESS_TOKEN")

CAPTION = "caption string"

def upload_reel(video_url):

    url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"

    data = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": CAPTION,
        "access_token": TOKEN
    }

    response = requests.post(url, data=data).json()

    creation_id = response["id"]

    publish_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"

    publish_data = {
        "creation_id": creation_id,
        "access_token": TOKEN
    }

    publish_response = requests.post(
        publish_url,
        data=publish_data
    )

    return publish_response.json()