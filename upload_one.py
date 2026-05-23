import os
import time
from dotenv import load_dotenv
from drive_utils import *
from cloudinary_utils import *
from instagram_utils import *

load_dotenv()

READY_FOLDER_ID = os.getenv("READY_FOLDER_ID")

LOCK_FILE = "upload.lock"

if os.path.exists(LOCK_FILE):

    print("Upload already running")
    time.sleep(600)

    exit()

open(LOCK_FILE, "w").close()

try:

    ready_files = list_files(READY_FOLDER_ID)

    if not ready_files:
        print("No clips available")
        exit()

    clip = ready_files[0]

    local_file = "temp/upload.mp4"

    download_file(clip['id'], local_file)

    video_url, public_id = upload_to_cloudinary(local_file)

    result = upload_reel(video_url)

    print(result)

    delete_file(clip['id'])

    delete_cloudinary(public_id)

    os.remove(local_file)

finally:

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)