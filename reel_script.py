import textwrap
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from multiprocessing import Pool, cpu_count
import os
import gc

# Set paths
background_video = "C:\\joke-reel-generator\\backgroud.mp4"
music = "C:\\joke-reel-generator\\music.mp3"
font_path = "C:/Windows/Fonts/arialuni.ttf"

# Create output folder
os.makedirs("output", exist_ok=True)

# Captions
captions = [
    "KABHI HAAR MAT MAANO My name is Hardik and I am a boss of this universe, screw you boys.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Don’t wait for the opportunity. Create it!",
    # Add more quotes here...
]

# Create wrapped and padded text clip
def create_text_clip(text, font_path, max_width=800, font_size=60, padding=50, duration=15):
    wrapped_text = '\n'.join(textwrap.wrap(text, width=15))

    while True:
        text_clip = TextClip(
            wrapped_text,
            font=font_path,
            fontsize=font_size,
            color='white',
            stroke_color='black',
            stroke_width=2,
            method='caption',
            align='center'
        )
        if text_clip.size[0] <= max_width or font_size <= 20:
            break
        font_size -= 5

    text_clip = text_clip.margin(left=padding, right=padding, opacity=0)
    return text_clip.set_position(('center', 'bottom')).set_duration(duration)

# Function to generate reel (to be used with multiprocessing)
def generate_reel(args):
    i, text = args
    output_file = f"output/reel_{i}.mp4"

    try:
        video = VideoFileClip(background_video).resize(height=1080)
        audio = AudioFileClip(music).set_duration(video.duration)

        text_clip = create_text_clip(text, font_path, duration=video.duration)
        final_clip = CompositeVideoClip([video, text_clip])
        final_clip = final_clip.set_audio(audio).set_duration(video.duration)

        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24, logger=None)
        print(f"[✔] Created: {output_file}")

    except Exception as e:
        print(f"[✖] Failed to create {output_file} — {e}")

    finally:
        video.close()
        audio.close()
        text_clip.close()
        final_clip.close()
        del video, audio, text_clip, final_clip
        gc.collect()

# Run in parallel using multiprocessing
if __name__ == "__main__":
    print("Generating reels...")
    with Pool(processes=min(cpu_count(), len(captions))) as pool:
        pool.map(generate_reel, list(enumerate(captions, 1)))
