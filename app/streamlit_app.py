# Import necessary libraries
import streamlit as st  # Streamlit for creating the web app UI
import tempfile  # For creating temporary files
from PIL import Image  # For image processing
import cv2  # OpenCV for image operations
import os  # For operating system interactions

# Import custom modules
from detector import detect_potholes  # Module to detect potholes from image
from roast_engine import roast_pothole  # Module to generate humorous comments on potholes
from certificate_generator import generate_certificate  # Module to create pothole certificate

# Set Streamlit app configuration: title, layout, sidebar behavior, and About info
st.set_page_config(
    page_title="Vazhi Illae Kuzhi 🚧",  # Webpage title
    layout="wide",  # Use wide screen layout
    initial_sidebar_state="expanded",  # Sidebar is expanded by default
    menu_items={
        'About': "# Vazhi Illae Kuzhi\nAn AI-powered pothole detection and certification system"  # About section info
    }
)

# Apply custom CSS styles to enhance visual appearance
st.markdown(""" ... """, unsafe_allow_html=True)  # HTML + CSS block for styling

# Initialize session state variables to track app state across pages
if 'potholes' not in st.session_state:  # List to store detected potholes
    st.session_state.potholes = []
if 'road_name' not in st.session_state:  # Name of the road being analyzed
    st.session_state.road_name = ""
if 'current_page' not in st.session_state:  # Tracks which page is currently being displayed
    st.session_state.current_page = "upload"

# Sidebar UI with navigation and status display
with st.sidebar:
    st.markdown("### 🚧 Navigation")  # Section header for navigation
    st.markdown("---")  # Horizontal separator
    
    # Upload & Analyze Button
    col1, col2 = st.columns([1, 3])  # Layout for icon and button
    with col1:
        st.markdown("📤")  # Upload icon
    with col2:
        if st.button("Upload & Analyze", use_container_width=True, type="secondary"):  # Button to switch to upload page
            st.session_state.current_page = "upload"
    
    # Generate Certificate Button
    col1, col2 = st.columns([1, 3])  # Layout for icon and button
    with col1:
        st.markdown("📄")  # Certificate icon
    with col2:
        if st.button("Generate Certificate", use_container_width=True, type="secondary"):  # Button to switch to certificate page
            st.session_state.current_page = "certificate"
    
    st.markdown("---")  # Horizontal separator
    
    # Show current detection status
    if st.session_state.potholes:  # If potholes are detected, show status
        st.markdown("### ✅ Status")  # Status header
        st.ma  # (Possibly an incomplete or truncated line in the original code)
