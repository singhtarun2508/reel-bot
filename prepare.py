import os
import subprocess
from dotenv import load_dotenv
from drive_utils import *

load_dotenv()

MAIN_FOLDER_ID = os.getenv("MAIN_FOLDER_ID")
READY_FOLDER_ID = os.getenv("READY_FOLDER_ID")

READY_TEMP = "temp/ready"

os.makedirs(READY_TEMP, exist_ok=True)

ready_files = list_files(READY_FOLDER_ID)

if len(ready_files) >= 4:
    print("Enough clips already ready")
    exit()

main_files = list_files(MAIN_FOLDER_ID)

if not main_files:
    print("No main videos")
    exit()

video = main_files[0]

input_video = "temp/input.mp4"

download_file(video['id'], input_video)

subprocess.run([
    "ffmpeg",
    "-i",
    input_video,
    "-c",
    "copy",
    "-map",
    "0",
    "-segment_time",
    "60",
    "-f",
    "segment",
    "temp/ready/clip_%03d.mp4"
])

for file in sorted(os.listdir(READY_TEMP)):
    upload_file(
        os.path.join(READY_TEMP, file),
        READY_FOLDER_ID
    )

delete_file(video['id'])

print("Preparation completed")