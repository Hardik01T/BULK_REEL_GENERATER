import textwrap
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os
import gc
from multiprocessing import Pool, cpu_count

background_video = "C:\\joke-reel-generator\\backgroud.mp4"
music = "C:\\joke-reel-generator\\music.mp3"
font_path = "C:/Windows/Fonts/arialuni.ttf"

captions = [
    "KABHI HAAR MAT MAANO My name is Hardik and I am a boss of this universe, screw you boys.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Don’t wait for the opportunity. Create it!",
    # Add more quotes...
]

def create_text_clip(text, font_path, max_width=800, font_size=60, padding=50):
    wrapped_text = '\n'.join(textwrap.wrap(text, width=15))
    
    while True:
        try:
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
            if text_clip.size[0] <= max_width:
                break
            font_size -= 5
        except Exception as e:
            print(f"[X] TextClip creation error: {e}")
            return None

    return text_clip.margin(left=padding, right=padding, opacity=0).set_position(('center', 'bottom')).set_duration(15)

def generate_reel(args):
    i, text = args
    output_file = f"output/reel_{i}.mp4"
    final_clip = None

    try:
        video = VideoFileClip(background_video).resize(height=720)  # lower height for memory optimization
        audio = AudioFileClip(music)
        text_clip = create_text_clip(text, font_path)

        if text_clip is None:
            raise Exception("TextClip generation failed")

        final_clip = CompositeVideoClip([video, text_clip])
        final_clip = final_clip.set_audio(audio).set_duration(video.duration)

        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24)
        print(f"[✓] Created: {output_file}")

    except Exception as e:
        print(f"[X] Failed to create {output_file} – {e}")

    finally:
        if final_clip:
            final_clip.close()
        if 'video' in locals():
            video.close()
        if 'audio' in locals():
            audio.close()
        if 'text_clip' in locals() and text_clip:
            text_clip.close()
        gc.collect()

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    with Pool(processes=min(cpu_count(), 2)) as pool:  # Use only 2 cores to avoid memory overflow
        pool.map(generate_reel, list(enumerate(captions, 1)))
