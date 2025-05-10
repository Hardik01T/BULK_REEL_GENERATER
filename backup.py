import subprocess
import textwrap 
import sys
import os

# Ensure console prints Unicode correctly (Windows)
sys.stdout.reconfigure(encoding='utf-8')

# Path setup
background_video = "C:\\joke-reel-generator\\backgroud.mp4"
music = "C:\\joke-reel-generator\\music.mp3"
font_path = "C:/Windows/Fonts/arialuni.ttf"  # Use a Unicode-supporting font like Arial Unicode or Noto

# Create output directory if not exists
os.makedirs("output", exist_ok=True)

# 10 Hindi captions
captions = [
    "KABHI HAAR MAT MAANO",
]

# Generate reels
for i, text in enumerate(captions, 1):
    output_file = f"output\\reel_{i}.mp4"

    # Escape single quotes in text for ffmpeg
    safe_text = text.replace("'", r"\'")
    
    # For text wrapping (text inside reel)
    wrapped_text = '\n'.join(textwrap.wrap(text, width=15))  # Increased width for better visibility
    escaped_text = wrapped_text.replace("'", r"\'").replace("\n", r'\n')

    # Control font style and animations
    filter_str = (
        f"[0:v]scale=1080:1920,"
        f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
        f"fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2:"
        f"alpha='if(lt(t,1),0,if(lt(t,2),(t-1)/1,1))'[v]"
    )

    # Final FFmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-i", background_video,
        "-i", music,
        "-filter_complex", filter_str,
        "-map", "[v]",
        "-map", "1:a",
        "-shortest",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create {output_file}\n{e}")
