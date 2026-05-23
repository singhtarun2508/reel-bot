import os
import subprocess

INPUT_DIR = "input"
OUTPUT_DIR = "clips"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):

    if file.endswith((".mp4", ".mkv", ".webm")):

        input_path = os.path.join(INPUT_DIR, file)

        filename = os.path.splitext(file)[0]

        output_pattern = os.path.join(
            OUTPUT_DIR,
            f"{filename}_%03d.mp4"
        )

        command = [
            "ffmpeg",
            "-i", input_path,

            # keep only first video + audio stream
            "-map", "0:v:0",
            "-map", "0:a:0",

            # re-encode safely for instagram/mp4
            "-c:v", "libx264",
            "-c:a", "aac",

            # split every 20 seconds
            "-f", "segment",
            "-segment_time", "20",
            "-reset_timestamps", "1",

            output_pattern
        ]

        subprocess.run(command)

print("Done splitting videos.")
