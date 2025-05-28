# 🎬 Joke Reel Generator

Automatically generate vertical short-form video reels using background videos, music, and one-liner quotes or jokes.  
Ideal for social media content creators who want to produce multiple reels quickly and efficiently.

---

## 🧩 What Problem Does This Solve?

Manually editing short reels for Instagram, YouTube Shorts, or TikTok is time-consuming and repetitive.  
This script **automates the process**, saving hours of editing by:

- Randomly combining videos, music, and quotes
- Styling text with bold-like appearance and animation
- Exporting polished vertical reels ready to post

Perfect for meme pages, joke-of-the-day content, quote channels, or anyone building content in bulk.

---

## 🚀 Features

- Automatically pairs one-liner quotes with random videos and music
- Outputs reels in 1080x1920 (9:16) format — ideal for mobile platforms
- Bold-styled white text without stroke (centered on screen)
- Text fades in and out smoothly
- No ImageMagick needed (uses PIL via `method='caption'`)
- Works with any custom `.ttf` font file

---

## 📂 Folder Structure

joke-reel-generator/
├── Videos/ # Background video clips (.mp4/.mov)
├── Music/ # Music tracks (.mp3/.wav)
├── Fonts/ # Font file (.ttf), e.g., Boldfinger.ttf
├── quotes.txt # One quote or joke per line
├── Output/ # Final reels will be saved here
├── script.py # The main Python script

yaml
Copy
Edit

---

## 🛠️ Requirements

- Python 3.7+
- [MoviePy](https://github.com/Zulko/moviepy)

Install dependencies:

```bash
pip install moviepy
▶️ How to Use
Place your background videos in the Videos/ folder.

Place your music files in the Music/ folder.

Put a .ttf font file (e.g., Boldfinger.ttf) in Fonts/.

Add one-line quotes or jokes to quotes.txt, one per line.

Open script.py and make sure to update paths if needed.

Run the script:

bash
Copy
Edit
python script.py
Your final reels will be saved in the Output/ folder.

✏️ Customization
Feature	How to Change
Font style	Update font_path in the script
Text size	Change fontsize (default: 100)
Video duration	Adjust subclip(0, 15)
Fade duration	Change fadein and fadeout values
Output size	Set output_width and output_height (default: 1080x1920)

🧠 Tips
Works best with one-line quotes for clean formatting.

Make sure all videos and audio files are of sufficient length.

For better boldness, the script fakes bold by layering multiple text clips with slight offsets.

