from moviepy.editor import TextClip

font_path = r"C:\joke-reel-generator\Fonts\Montserrat-VariableFont_wght.ttf"  # Adjust path

txt_clip = TextClip(
    "Test Text",
    fontsize=70,
    font=font_path,
    color='white',
    stroke_color='black',
    stroke_width=3,
    method='caption',
    size=(800, None),
    align='center'
)

txt_clip.save_frame("test_text.png")
print("Text image saved as test_text.png")