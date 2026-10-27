import streamlit as st
import os
import time
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip
)

st.set_page_config(page_title="AI Property Video Generator", page_icon="✨", layout="wide")

# Universe Background & Sparkle White Theme CSS Styling
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
        color: #ffffff;
    }
    .sparkle-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(255, 255, 255, 0.15);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>✨ AI Property Video Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0;'>CapCut-Style Templates & Universe Aesthetics</p>", unsafe_allow_html=True)

TEMPLATES = {
    "Cosmic Luxury": {"bg_color": (10, 10, 35), "text_color": "white", "opacity": 0.4},
    "Neon Cyber": {"bg_color": (5, 25, 45), "text_color": "#00ffff", "opacity": 0.3},
    "Minimal Sparkle": {"bg_color": (240, 240, 245), "text_color": "black", "opacity": 0.1},
    "Cinematic Dark": {"bg_color": (0, 0, 0), "text_color": "#f1c40f", "opacity": 0.6},
    "Eco Estate": {"bg_color": (15, 35, 20), "text_color": "#e8f8f5", "opacity": 0.3},
    "Sunset Warm": {"bg_color": (45, 20, 10), "text_color": "#f39c12", "opacity": 0.35},
    "CapCut Dynamic": {"bg_color": (20, 20, 20), "text_color": "#ff0055", "opacity": 0.25},
    "Royal Galaxy": {"bg_color": (30, 10, 45), "text_color": "#e0aaff", "opacity": 0.4},
    "Vintage Grain": {"bg_color": (35, 30, 25), "text_color": "#f5ebe0", "opacity": 0.45},
    "Bold Punchy": {"bg_color": (15, 15, 15), "text_color": "#ffffff", "opacity": 0.3}
}

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

with st.container():
    st.markdown('<div class="sparkle-card">', unsafe_allow_html=True)
    st.subheader("🎨 1. Choose Template")
    selected_template = st.selectbox("Select a video theme style:", list(TEMPLATES.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sparkle-card">', unsafe_allow_html=True)
    st.subheader("📝 2. Property Information")
    col1, col2 = st.columns(2)
    with col1:
        prop_name = st.text_input("Property Name", "Galaxy Heights Villa")
        prop_type = st.text_input("Property Type", "Penthouse")
        price = st.text_input("Price", "$650,000")
    with col2:
        location = st.text_input("Location", "Orbit Sector 9, Sky City")
        features_input = st.text_input("Key Features (Comma separated)", "Panoramic Glass Views, Infinity Pool, Smart Home, Private Terrace")
        contact = st.text_input("Contact Info", "Call: +1-800-UNIVERSE")
    cta = st.text_input("Call To Action (CTA)", "Book Your Private Stargazing Tour Today!")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sparkle-card">', unsafe_allow_html=True)
    st.subheader("🖼️ 3. Upload Property Images")
    uploaded_files = st.file_uploader("Upload property photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sparkle-card">', unsafe_allow_html=True)
    st.subheader("✂️ 4. Video Editing Settings")
    col3, col4 = st.columns(2)
    with col3:
        scene_duration = st.slider("Scene Duration (Seconds)", 2.0, 6.0, 3.5)
    with col4:
        font_size = st.selectbox("Font Size", [35, 42, 50], index=1)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("✨ Generate AI Video Now", type="primary", use_container_width=True):
    with st.spinner("Rendering video using AI engine... Please wait..."):
        theme = TEMPLATES[selected_template]
        saved_images = []
        
        if uploaded_files:
            for file in uploaded_files:
                path = os.path.join("uploads", file.name)
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                saved_images.append(path)
        else:
            fallback_path = "uploads/placeholder.png"
            dummy = ColorClip(size=(1280, 720), color=theme["bg_color"], duration=1)
            dummy.save_frame(fallback_path)
            saved_images.append(fallback_path)

        width, height = 1280, 720
        clips = []

        def make_text(txt_content):
            try:
                return TextClip(txt_content, fontsize=font_size, color=theme["text_color"], font='Arial-Bold', size=(width-120, None), method='caption').set_duration(scene_duration).set_position('center')
            except:
                return ColorClip(size=(width, height), color=(0,0,0), duration=scene_duration)

        title_str = f"{prop_name}\n{prop_type} | {location}\nPrice: {price}"
        bg1 = ImageClip(saved_images[0]).set_duration(scene_duration).resize(newsize=(width, height))
        ov1 = ColorClip(size=(width, height), color=theme["bg_color"]).set_duration(scene_duration).set_opacity(theme["opacity"])
        clips.append(CompositeVideoClip([bg1, ov1, make_text(title_str)]))

        features = [f.strip() for f in features_input.split(',')]
        img_idx = 1
        for feat in features:
            img_p = saved_images[img_idx % len(saved_images)]
            img_idx += 1
            bg = ImageClip(img_p).set_duration(scene_duration).resize(newsize=(width, height))
            ov = ColorClip(size=(width, height), color=theme["bg_color"]).set_duration(scene_duration).set_opacity(theme["opacity"])
            clips.append(CompositeVideoClip([bg, ov, make_text(f"Key Feature:\n{feat}")]))

        cta_str = f"{cta}\n{contact}"
        bg_end = ImageClip(saved_images[-1]).set_duration(scene_duration).resize(newsize=(width, height))
        ov_end = ColorClip(size=(width, height), color=theme["bg_color"]).set_duration(scene_duration).set_opacity(theme["opacity"])
        clips.append(CompositeVideoClip([bg_end, ov_end, make_text(cta_str)]))

        final_video = concatenate_videoclips(clips, method="compose")
        output_path = f"outputs/property_promo_{int(time.time())}.mp4"
        final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

        st.success("Video successfully generated!")
        st.video(output_path)
        with open(output_path, "rb") as f:
            st.download_button("📥 Download MP4 Video", f, file_name="property_promo.mp4", mime="video/mp4")
