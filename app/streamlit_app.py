import streamlit as st
import tempfile
from PIL import Image
import cv2
import os

from detector import detect_potholes
from roast_engine import roast_pothole
from certificate_generator import generate_certificate

st.set_page_config(page_title="Vazhi Illae Kuzhi 🚧", layout="wide")
st.title("🕳️ Vazhi Illae Kuzhi - Pothole Detector + Roaster 🤪")
st.markdown("Upload a road image and let’s detect potholes and roast them 🌧️💥")

uploaded_file = st.file_uploader("📤 Upload Road Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.image(temp_path, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing potholes..."):
        result = detect_potholes(temp_path)
        potholes = result["potholes"]
        stages = result["stages"]

    st.success(f"✅ Found {len(potholes)} pothole(s)!")

    # Show processing stages
    st.subheader("🔍 Processing Steps")
    cols = st.columns(len(stages))
    for i, (label, img_stage) in enumerate(stages.items()):
        rgb_img = cv2.cvtColor(img_stage, cv2.COLOR_BGR2RGB)
        cols[i].image(rgb_img, caption=label, use_column_width=True)

    # Show roasts
    if potholes:
        st.subheader("🔥 Pothole Roasts:")
        for i, pothole in enumerate(potholes, 1):
            area = pothole["area"]
            roast = roast_pothole(area)
            st.markdown(f"**{i}.** {roast}")
    else:
        st.info("No potholes found! 🌈 Blessed ground 🙏")
    # Clean temp file
    os.remove(temp_path)

    # Certificate generation
st.subheader("📄 Pothole Certificate")

road_name = st.text_input("Enter Road Name for Certificate", "Unnamed Road")

if st.button("Generate Certificate"):
    cert_img = generate_certificate(road_name, potholes)
    cert_path = "pothole_certificate.png"
    cert_img.save(cert_path)

    st.image(cert_path, caption="🚧 Downloadable Pothole Certificate", use_column_width=True)

    with open(cert_path, "rb") as file:
        btn = st.download_button(
            label="📥 Download as PNG",
            data=file,
            file_name="pothole_certificate.png",
            mime="image/png"
        )





