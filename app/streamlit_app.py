import streamlit as st
import tempfile
from PIL import Image
from detector import detect_potholes
from roast_engine import roast_pothole

st.set_page_config(page_title="Vazhi Illae Kuzhi 🚧", layout="centered")

st.title("🕳️ Vazhi Illae Kuzhi - Pothole Detector + Roaster 🤪")
st.markdown("Upload a road image and let’s detect potholes and roast them 🌧️💥")

uploaded_file = st.file_uploader("📤 Upload Road Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.image(temp_path, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing potholes..."):
        potholes, _ = detect_potholes(temp_path)

    st.success(f"✅ Found {len(potholes)} pothole(s)!")

    if potholes:
        st.subheader("🔥 Pothole Roasts:")
        for i, pothole in enumerate(potholes, 1):
            area = pothole["area"]
            roast = roast_pothole(area)
            st.markdown(f"**{i}.** {roast}")
    else:
        st.info("No potholes found! 🌈 Blessed ground 🙏")
