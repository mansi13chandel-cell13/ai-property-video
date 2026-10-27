import os
import time
from flask import Flask, render_template, request, send_from_directory
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip
)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 10+ Template Theme Configurations
TEMPLATES = {
    "cosmic_luxury": {"bg_color": (10, 10, 35), "text_color": "white", "overlay_opacity": 0.4},
    "neon_cyber": {"bg_color": (5, 25, 45), "text_color": "#00ffff", "overlay_opacity": 0.3},
    "minimal_white": {"bg_color": (240, 240, 245), "text_color": "black", "overlay_opacity": 0.1},
    "cinematic_dark": {"bg_color": (0, 0, 0), "text_color": "#f1c40f", "overlay_opacity": 0.6},
    "nature_green": {"bg_color": (15, 35, 20), "text_color": "#e8f8f5", "overlay_opacity": 0.3},
    "sunset_gold": {"bg_color": (45, 20, 10), "text_color": "#f39c12", "overlay_opacity": 0.35},
    "capcut_fast": {"bg_color": (20, 20, 20), "text_color": "#ff0055", "overlay_opacity": 0.25},
    "royal_purple": {"bg_color": (30, 10, 45), "text_color": "#e0aaff", "overlay_opacity": 0.4},
    "vintage_film": {"bg_color": (35, 30, 25), "text_color": "#f5ebe0", "overlay_opacity": 0.45},
    "modern_bold": {"bg_color": (15, 15, 15), "text_color": "#ffffff", "overlay_opacity": 0.3}
}

def create_text_layer(text, fontsize, color, duration, size=(1280, 720)):
    try:
        txt = TextClip(
            text, 
            fontsize=fontsize, 
            color=color, 
            font='Arial-Bold', 
            size=(size[0] - 120, None), 
            method='caption'
        ).set_duration(duration)
        return txt.set_position('center')
    except Exception as e:
        print(f"Text Render Notice: {e}")
        return ColorClip(size=size, color=(0, 0, 0), duration=duration)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    # Fetch Form Inputs
    prop_name = request.form.get('name', 'Luxury Space Property')
    prop_type = request.form.get('type', 'Penthouse')
    price = request.form.get('price', 'Contact Agent')
    location = request.form.get('location', 'Prime Location')
    features_raw = request.form.get('features', 'Modern Amenities, Great View')
    contact = request.form.get('contact', 'realty@assistant.com')
    cta = request.form.get('cta', 'Book Now!')
    
    template_key = request.form.get('template', 'cosmic_luxury')
    scene_duration = float(request.form.get('duration', 3.5))
    font_size = int(request.form.get('font_size', 42))
    
    # Theme configuration
    theme = TEMPLATES.get(template_key, TEMPLATES['cosmic_luxury'])
    
    # Handle File Uploads
    uploaded_files = request.files.getlist('images')
    saved_images = []
    
    for file in uploaded_files:
        if file and file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            saved_images.append(filepath)

    # Fallback placeholder image generation if no image provided
    if not saved_images:
        placeholder = os.path.join(UPLOAD_FOLDER, 'placeholder.png')
        dummy = ColorClip(size=(1280, 720), color=theme['bg_color'], duration=1)
        dummy.save_frame(placeholder)
        saved_images.append(placeholder)

    width, height = 1280, 720
    clips = []

    # Scene 1: Title Scene
    title_text = f"{prop_name}\n{prop_type} | {location}\nPrice: {price}"
    bg_1 = ImageClip(saved_images[0]).set_duration(scene_duration).resize(newsize=(width, height))
    overlay_1 = ColorClip(size=(width, height), color=theme['bg_color']).set_duration(scene_duration).set_opacity(theme['overlay_opacity'])
    txt_1 = create_text_layer(title_text, font_size, theme['text_color'], scene_duration)
    clips.append(CompositeVideoClip([bg_1, overlay_1, txt_1]))

    # Feature Scenes
    features = [f.strip() for f in features_raw.split(',')]
    img_idx = 1
    for feature in features:
        img_path = saved_images[img_idx % len(saved_images)]
        img_idx += 1
        
        bg = ImageClip(img_path).set_duration(scene_duration).resize(newsize=(width, height))
        overlay = ColorClip(size=(width, height), color=theme['bg_color']).set_duration(scene_duration).set_opacity(theme['overlay_opacity'])
        txt = create_text_layer(f"Key Feature:\n{feature}", font_size, theme['text_color'], scene_duration)
        clips.append(CompositeVideoClip([bg, overlay, txt]))

    # Closing CTA Scene
    closing_text = f"{cta}\n{contact}"
    bg_end = ImageClip(saved_images[-1]).set_duration(scene_duration).resize(newsize=(width, height))
    overlay_end = ColorClip(size=(width, height), color=theme['bg_color']).set_duration(scene_duration).set_opacity(theme['overlay_opacity'])
    txt_end = create_text_layer(closing_text, font_size, theme['text_color'], scene_duration)
    clips.append(CompositeVideoClip([bg_end, overlay_end, txt_end]))

    # Stitch video
    final_video = concatenate_videoclips(clips, method="compose")
    output_filename = f"video_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

    # Return HTML Video Embed
    return f'''
    <div class="text-center">
        <video controls autoplay class="mb-3">
            <source src="/{output_path}" type="video/mp4">
            Your browser does not support video playback.
        </video>
        <br>
        <a href="/{output_path}" download class="btn btn-sparkle">📥 Download Generated Video</a>
    </div>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
