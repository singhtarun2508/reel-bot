import os
import subprocess

INPUT_DIR = "input"
OUTPUT_DIR = "clips"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(INPUT_DIR):

    if file.endswith(".mp4"):

        input_path = os.path.join(INPUT_DIR, file)

        output_pattern = os.path.join(
            OUTPUT_DIR,
            file.replace(".mp4", "_%03d.mp4")
        )

        command = [
            "ffmpeg",
            "-i", input_path,
            "-c", "copy",
            "-map", "0",
            "-segment_time", "20",
            "-f", "segment",
            output_pattern
        ]

        subprocess.run(command, shell=True)

print("Done splitting videos.")