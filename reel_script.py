import textwrap
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

background_video = "C:\\joke-reel-generator\\backgroud.mp4"
music = "C:\\joke-reel-generator\\music.mp3"
font_path = "C:/Windows/Fonts/arialuni.ttf"  # Use a Unicode font

captions = [
    "KABHI HAAR MAT MAANO My name is Hardik and I am a boss of this universe, screw you boys.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "Don’t wait for the opportunity. Create it!",
    # Add more quotes here as needed...
]

# Function to create text clip with dynamic font size and padding
def create_text_clip(text, font_path, max_width=800, font_size=60, padding=50):
    # Wrap the text
    wrapped_text = '\n'.join(textwrap.wrap(text, width=15))  # Adjust the width for wrapping

    # Create a TextClip with dynamic size
    text_clip = TextClip(
        wrapped_text,
        font=font_path,
        fontsize=font_size,
        color='white',
        stroke_color='black',  # Black border
        stroke_width=2,        # Border thickness
        method='caption',      # This method allows text wrapping
        align='center'
    )

    # Adjust font size if text is too wide
    while text_clip.size[0] > max_width:
        font_size -= 5
        text_clip = TextClip(
            wrapped_text,
            font=font_path,
            fontsize=font_size,
            color='white',
            stroke_color='black',  # Black border
            stroke_width=2,        # Border thickness
            method='caption',      # This method allows text wrapping
            align='center'
        )

    # Add padding on the left and right
    text_clip = text_clip.margin(left=padding, right=padding, opacity=0)

    # Set position to bottom and duration
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(15)

    return text_clip

# Generate reels
for i, text in enumerate(captions, 1):
    output_file = f"output\\reel_{i}.mp4"

    # Create video and audio clips
    video = VideoFileClip(background_video).resize(height=1920)  # Resize video to fit Instagram reel aspect ratio
    audio = AudioFileClip(music)

    # Create the text clip with dynamic size and padding
    text_clip = create_text_clip(text, font_path)

    # Combine the video, text, and audio
    final_clip = CompositeVideoClip([video, text_clip])
    final_clip = final_clip.set_audio(audio).set_duration(video.duration)

    # Write the final output file
    try:
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24)
        print(f" Created: {output_file}")
    except Exception as e:
        print(f"Failed to create {output_file}\n{e}")
