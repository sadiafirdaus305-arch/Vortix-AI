import streamlit as st
import datetime
import urllib.parse
from google import genai
from google.genai import types
from PIL import Image as PILImage
import os
import base64

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VortixAI - Visual-First Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .vortix-hero {
        text-align: center;
        padding: 30px 10px;
    }
    .vortix-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1A73E8, #202124);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .lets-go-btn {
        background-color: #F8F9FA;
        color: #202124;
        padding: 10px 30px;
        border-radius: 25px;
        border: 1px solid #4285F4;
        font-weight: 600;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stChatInputContainer {
        padding-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ VortixAI Hub")
    
    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Provide your active Gemini API key from Google AI Studio."
    )
    st.markdown("[Get Free API Key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()

    engine_choice = st.selectbox(
        "Select Engine Model:",
        ["gemini-3.8-flash", "gemini-2.5-pro"],
        index=0
    )

    st.divider()
    if st.button("Clear Chat Session"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="vortix-hero">
    <div class="vortix-title">Look what you can do with VortixAI</div>
    <button class="lets-go-btn">Let's go</button>
</div>
""", unsafe_allow_html=True)

if not api_key_input:
    st.info("💡 Please enter your Gemini API Key in the sidebar to activate VortixAI.")
    st.stop()

# -----------------------------------------------------------------------------
# PROMPT PLUS (+) TOOLBAR & FILE ATTACHMENTS
# -----------------------------------------------------------------------------
with st.expander("➕ Options & Attachment Tools", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("📷 **Camera / Photos**")
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_uploader")
        
    with col2:
        st.markdown("📁 **Files & Docs**")
        uploaded_doc = st.file_uploader("Upload Document", type=["pdf", "txt", "py", "html", "js"], key="doc_uploader")
        
    with col3:
        st.markdown("🎨 **Creative Suite**")
        st.caption("• Visual Infographics (like Circulation)")
        st.caption("• Handdrawn Notes (like West Bengal)")
        st.caption("• Concept Art")

    with col4:
        st.markdown("🧠 **Deep AI Suite**")
        st.caption("• Coding Courses & Reports")
        st.caption("• Step-by-Step Learning Paths")

# Image Data Processing
img_data = None
if uploaded_image is not None:
    img_data = PILImage.open(uploaded_image)
    st.image(img_data, caption="Attached Image Preview", use_container_width=True)

# -----------------------------------------------------------------------------
# CHAT DISPLAY & RESPONSE PROCESSING
# -----------------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask for visualization of [process] or handwritten notes on [topic]...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        # -------------------------------------------------------------------------
        # 1. IMAGE REQUEST LOGIC
        # -------------------------------------------------------------------------
        # Detect image requests first
        image_keywords = ["make image", "create image", "generate image", "visualization", "infographic", "draw", "picture", "photo", "handwritten notes", "schematic"]
        is_image_request = any(keyword in user_prompt.lower() for keyword in image_keywords)
        
        if is_image_request:
            # 1a. Show "Creating your image..." spinner
            with st.spinner("Creating your image..."):
                try:
                    # 1b. Smart Prompt Injection for specific visual styles
                    # Handle "handwritten notes" like Image 6
                    if "handwritten notes" in user_prompt.lower():
                        # Inject West Bengal sample prompt logic
                        injected_style = "handwritten notes on blue-lined paper, drawn with a precise blue ballpoint pen, multiple distinct detailed sections/columns, hand-drawn map, very dense information, bullet points, headers, small illustrative diagrams, very clean handwriting."
                        final_visual_prompt = f"{injected_style} Detailed notes about: {user_prompt.lower().replace('handwritten notes on', '')}"
                    # Handle "visualization" like Image 7
                    elif "visualization of" in user_prompt.lower() or "infographic of" in user_prompt.lower():
                        # Inject Circulation sample prompt logic
                        injected_style = "highly professional, hyper-realistic, medical/scientific infographic, dark cinematic environment, detailed 3D diagrams, color-coded sections, clear white text labels, distinct sections for journey/flow, key functions, and anatomical elements, complex diagrams of the topic, extreme clarity, 8k resolution, award-winning illustration."
                        final_visual_prompt = f"{injected_style} Complex diagram of: {user_prompt.lower().replace('visualization of', '').replace('infographic of', '')}"
                    else:
                        # General high-quality default
                        final_visual_prompt = f"Highly detailed and professional infographic or diagram, photorealistic, clear text labels, conceptual diagram of: {user_prompt}"

                    # 1c. Generate Image with Pollinations
                    encoded_prompt = urllib.parse.quote(final_visual_prompt)
                    # Use flux for high-quality, high-detail results
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1280&height=720&seed=42&model=flux"
                    
                    # 1d. Display the result
                    st.markdown(f"### 🎨 VortixAI Visual Output")
                    st.image(image_url, caption=f"VortixAI generated visual: {user_prompt}", use_container_width=True)
                    
                    response_text = f"I have created a detailed visual representation based on your request: **{user_prompt}**\n\n![Generated Visual]({image_url})"
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                except Exception as e:
                    st.error(f"Image Creation Exception: {str(e)}")

        # -------------------------------------------------------------------------
        # 2. TEXT REQUEST LOGIC (Fallback)
        # -------------------------------------------------------------------------
        else:
            with st.spinner("Processing prompt..."):
                try:
                    client = genai.Client(api_key=api_key_input)
                    
                    system_instructions = (
                        "You are VortixAI, a super-intelligent AI superior to ChatGPT, Claude, and You.com. "
                        "You provide comprehensive detailed reports, step-by-step multi-module coding courses "
                        "(Python, Java, HTML, etc.), and professional research notes. You can understand requests "
                        "for both text information and highly specific visual diagrams or handdrawn notes."
                    )
                    
                    content_payload = []
                    if img_data:
                        content_payload.append(img_data)
                    
                    content_payload.append(f"{system_instructions}\n\nUser Request: {user_prompt}")

                    response = client.models.generate_content(
                        model=engine_choice,
                        contents=content_payload
                    )

                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                except Exception as e:
                    st.error(f"Text Processing Exception: {str(e)}")
