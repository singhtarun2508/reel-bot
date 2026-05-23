import os
import subprocess
from dotenv import load_dotenv
from drive_utils import *

load_dotenv()

MAIN_FOLDER_ID = os.getenv("MAIN_FOLDER_ID")
READY_FOLDER_ID = os.getenv("READY_FOLDER_ID")

TEMP_DIR = "temp"
READY_TEMP = "temp/ready"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(READY_TEMP, exist_ok=True)

# -----------------------------------
# CHECK READY CLIPS COUNT
# -----------------------------------

ready_files = list_files(READY_FOLDER_ID)

if len(ready_files) >= 4:
    print("Enough clips already ready")
    exit()

# -----------------------------------
# CHECK MAIN VIDEOS
# -----------------------------------

main_files = list_files(MAIN_FOLDER_ID)

if not main_files:
    print("No main videos")
    exit()

video = main_files[0]

input_video = os.path.join(TEMP_DIR, "input.mp4")

# -----------------------------------
# DOWNLOAD VIDEO
# -----------------------------------

print("Downloading video...")

download_file(video['id'], input_video)

# -----------------------------------
# SPLIT VIDEO
# -----------------------------------

print("Splitting video...")

output_pattern = os.path.join(
    READY_TEMP,
    "clip_%03d.mp4"
)

command = [
    "ffmpeg",
    "-i", input_video,

    # keep only first video and audio stream
    "-map", "0:v:0",
    "-map", "0:a:0",

    # instagram-safe encoding
    "-c:v", "libx264",
    "-c:a", "aac",

    # split settings
    "-f", "segment",
    "-segment_time", "60",
    "-reset_timestamps", "1",

    output_pattern
]

subprocess.run(command)

# -----------------------------------
# UPLOAD CLIPS
# -----------------------------------

print("Uploading clips...")

for file in sorted(os.listdir(READY_TEMP)):

    file_path = os.path.join(READY_TEMP, file)

    if os.path.isfile(file_path):

        upload_file(
            file_path,
            READY_FOLDER_ID
        )

# -----------------------------------
# DELETE ORIGINAL VIDEO
# -----------------------------------

try:
    delete_file(video['id'])
    print("Original video deleted")

except Exception as e:
    print("Could not delete original video:")
    print(e)

print("Preparation completed")
