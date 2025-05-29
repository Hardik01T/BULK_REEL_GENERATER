import sys
import io
import os
import random
from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
)
from moviepy.video.fx.all import fadein, fadeout

# Force UTF-8 encoding for Windows console output to avoid UnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths - update if needed
video_folder = r"C:\joke-reel-generator\Videos"
music_folder = r"C:\joke-reel-generator\Music"
quotes_file = r"C:\joke-reel-generator\quotes.txt"
output_folder = r"C:\joke-reel-generator\Output"

# Specify your font path here (use bold or semi-bold variant if available)
font_path = r"C:\joke-reel-generator\Fonts\\boldfinger-cufonfonts\Boldfinger.ttf"

output_width, output_height = 1080, 1920  # 9:16 aspect ratio
os.makedirs(output_folder, exist_ok=True)

# Load videos and music
videos = sorted([os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.lower().endswith(('.mp4', '.mov'))])
music_tracks = sorted([os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.lower().endswith(('.mp3', '.wav'))])

# Load quotes
with open(quotes_file, "r", encoding="utf-8") as f:
    quotes = [line.strip() for line in f if line.strip()]

# Prepare cycles
total_quotes = len(quotes)
video_cycle = (videos * ((total_quotes // len(videos)) + 1))[:total_quotes]
music_cycle = (music_tracks * ((total_quotes // len(music_tracks)) + 1))[:total_quotes]

# Shuffle with seed
random.seed(42)
random.shuffle(video_cycle)
random.shuffle(music_cycle)

for i, quote in enumerate(quotes):
    video_path = video_cycle[i]
    music_path = music_cycle[i]

    print(f"\nReel {i + 1}:")
    print(f"Video: {os.path.basename(video_path)}")
    print(f"Music: {os.path.basename(music_path)}")
    print(f"Quote: {quote}")

    # Load and crop video
    clip = VideoFileClip(video_path).subclip(0, min(15, VideoFileClip(video_path).duration))
    clip = clip.resize(height=output_height)
    if clip.w < output_width:
        clip = clip.resize(width=output_width)
    clip = clip.crop(x_center=clip.w // 2, y_center=clip.h // 2, width=output_width, height=output_height)

    # Load audio
    audio = AudioFileClip(music_path).subclip(0, clip.duration)
    clip = clip.set_audio(audio.volumex(0.6))

    # Create base text clip
    base_txt = TextClip(
        quote,
        fontsize=100,
        font=font_path,
        color='white',
        method='caption',
        size=(int(output_width * 0.9), None),
        align='center'
    ).set_duration(clip.duration)

    # Layer copies shifted by 1 pixel around center for fake bold effect
    offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    layers = [base_txt.set_position("center")]
    for ox, oy in offsets[1:]:
        layers.append(base_txt.set_position((ox, oy)))

    txt_clip = CompositeVideoClip(layers).set_duration(clip.duration)
    txt_clip = fadein(txt_clip, 1).fadeout(1)
    txt_clip = txt_clip.set_position("center")

    # Fade out clip at end
    clip = fadeout(clip, 1.5)

    # Combine video and text
    final = CompositeVideoClip([clip, txt_clip]).set_duration(clip.duration)

    output_path = os.path.join(output_folder, f"reel_{i + 1}.mp4")
    final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=30)

    print(f"Saved: {output_path}")
#commewnt to add