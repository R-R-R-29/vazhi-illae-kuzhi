import streamlit as st
import tempfile
from PIL import Image
import cv2
import os
from detector import detect_potholes
from roast_engine import roast_pothole
from certificate_generator import generate_certificate

# Enhanced page configuration
st.set_page_config(
    page_title="Vazhi Illae Kuzhi 🚧", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Vazhi Illae Kuzhi\nAn AI-powered pothole detection and certification system"
    }
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4ECDC4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: #d1edff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Roast styling */
    .roast-item {
        background: #fff5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #ff6b6b;
        margin: 0.5rem 0;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-top: 3px solid #4ECDC4;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #4ECDC4;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Progress styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'potholes' not in st.session_state:
    st.session_state.potholes = []
if 'road_name' not in st.session_state:
    st.session_state.road_name = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "upload"

# Enhanced Sidebar Navigation
with st.sidebar:
    st.markdown("### 🚧 Navigation")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("📤")
    with col2:
        if st.button("Upload & Analyze", use_container_width=True, type="secondary"):
            st.session_state.current_page = "upload"
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("📄")
    with col2:
        if st.button("Generate Certificate", use_container_width=True, type="secondary"):
            st.session_state.current_page = "certificate"
    
    st.markdown("---")
    
    # Status indicator
    if st.session_state.potholes:
        st.markdown("### ✅ Status")
        st.markdown(f"**{len(st.session_state.potholes)}** potholes detected")
        st.markdown(f"**Road:** {st.session_state.road_name or 'Not specified'}")
    else:
        st.markdown("### ⏳ Status")
        st.markdown("No analysis performed yet")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    total_area = sum(p.get('area', 0) for p in st.session_state.potholes)
    st.metric("Total Damage Area", f"{total_area:,} px²")
    st.metric("Severity Level", "High" if len(st.session_state.potholes) > 3 else "Medium" if len(st.session_state.potholes) > 0 else "Low")

# Page 1: Upload Documents
if st.session_state.current_page == "upload":
    # Enhanced header
    st.markdown('<h1 class="main-header">🕳️ Vazhi Illae Kuzhi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Pothole Detection & Roasting System 🤪</p>', unsafe_allow_html=True)
    
    # Instructions card
    st.markdown("""
    <div class="info-card" >
        <h4 style="color: black;">🚀 How it works:</h4>
<p style="color: black;">1. Upload a road image (JPG, JPEG, or PNG)</p>
<p style="color: black;">2. Our AI will detect and analyze potholes</p>
<p style="color: black;">3. Get hilarious roasts for each pothole found</p>
<p style="color: black;">4. Generate an official certificate</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Upload Road Image")
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the road for best results"
        )
    
    with col2:
        if uploaded_file:
            st.markdown("### 📋 File Info")
            st.info(f"**Name:** {uploaded_file.name}")
            st.info(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
    
    if uploaded_file:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        
        # Display uploaded image
        st.markdown("### 🖼️ Uploaded Image")
        st.image(temp_path, caption="📸 Road Image for Analysis", use_column_width=True)
        
        # Analysis button
        if st.button("🔍 Analyze Potholes", type="primary", use_container_width=True):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text('🔄 Initializing analysis...')
            progress_bar.progress(20)
            
            status_text.text('🤖 Running AI detection...')
            progress_bar.progress(60)
            
            with st.spinner("Analyzing potholes..."):
                result = detect_potholes(temp_path)
                potholes = result["potholes"]
                stages = result["stages"]
            
            progress_bar.progress(100)
            status_text.text('✅ Analysis complete!')
            
            # Store results in session state
            st.session_state.potholes = potholes
            
            # Results section
            st.markdown("---")
            
            if potholes:
                # Success message with stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Potholes Found</div>
                    </div>
                    """.format(len(potholes)), unsafe_allow_html=True)
                
                with col2:
                    avg_area = sum(p['area'] for p in potholes) / len(potholes)
                    st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number">{:.0f}</div>
                        <div class="stat-label">Avg Area (px²)</div>
                    </div>
                    """.format(avg_area), unsafe_allow_html=True)
                
                with col3:
                    severity = "🔴 High" if len(potholes) > 3 else "🟡 Medium" if len(potholes) > 0 else "🟢 Low"
                    st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Severity</div>
                    </div>
                    """.format(severity), unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Show processing stages
                st.markdown("### 🔍 AI Processing Pipeline")
                cols = st.columns(len(stages))
                for i, (label, img_stage) in enumerate(stages.items()):
                    rgb_img = cv2.cvtColor(img_stage, cv2.COLOR_BGR2RGB)
                    with cols[i]:
                        st.image(rgb_img, caption=f"**{label}**", use_column_width=True)
                
                st.markdown("---")
                
                # Show roasts with enhanced styling
                st.markdown("### 🔥 AI-Generated Pothole Roasts")
                for i, pothole in enumerate(potholes, 1):
                    area = pothole["area"]
                    roast = roast_pothole(area)
                    st.markdown(f"""
                    <div class="roast-item">
                        <strong>Pothole #{i}</strong> (Area: {area:,} px²)<br>
                        💬 "{roast}"
                    </div>
                    """, unsafe_allow_html=True)
                
                # Navigation hint
                st.markdown("""
                <div class="success-card">
                    <h4>🎉 Analysis Complete!</h4>
                    <p>Ready to generate your official pothole certificate? Click on <strong>'Generate Certificate'</strong> in the sidebar!</p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="success-card">
                    <h4>🌈 Excellent News!</h4>
                    <p>No potholes detected in this image! This road appears to be in good condition. 🙏</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Clean temp file
        os.remove(temp_path)

# Page 2: Generate Certificate
elif st.session_state.current_page == "certificate":
    st.markdown('<h1 class="main-header">📄 Certificate Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Create Official Pothole Documentation</p>', unsafe_allow_html=True)
    
    if not st.session_state.potholes:
        st.markdown("""
        <div class="warning-card">
            <h4>⚠️ No Analysis Data Found</h4>
            <p>Please upload and analyze a road image first to generate a certificate.</p>
            <p>👈 Use the sidebar to navigate to <strong>'Upload & Analyze'</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Success status
        st.markdown("""
        <div class="success-card">
            <h4>✅ Ready for Certificate Generation</h4>
            <p>Analysis data loaded successfully for <strong>{} pothole(s)</strong></p>
        </div>
        """.format(len(st.session_state.potholes)), unsafe_allow_html=True)
        
        # Enhanced pothole summary
        st.markdown("### 🕳️ Detected Potholes Summary")
        
        # Summary table
        col1, col2 = st.columns([2, 1])
        with col1:
            for i, pothole in enumerate(st.session_state.potholes, 1):
                st.markdown(f"""
                <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #FF6B6B;">
                    <strong>🕳️ Pothole #{i}</strong><br>
                    📏 Area: <strong>{pothole['area']:,} pixels</strong><br>
                    📊 Severity: <strong>{'High' if pothole['area'] > 1000 else 'Medium' if pothole['area'] > 500 else 'Low'}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            total_area = sum(p['area'] for p in st.session_state.potholes)
            st.metric("Total Potholes", len(st.session_state.potholes))
            st.metric("Total Damage Area", f"{total_area:,} px²")
            st.metric("Road Condition", "Poor" if len(st.session_state.potholes) > 3 else "Fair")
        
        st.markdown("---")
        
        # Certificate generation section
        st.markdown("### 📄 Certificate Configuration")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            road_name = st.text_input(
                "🛣️ Road Name for Certificate", 
                value=st.session_state.road_name or "",
                placeholder="Enter the name of the road (e.g., Main Street, Highway 101)",
                help="This will appear on the official certificate"
            )
            st.session_state.road_name = road_name
        
        with col2:
            st.markdown("### 📋 Certificate Info")
            st.info("**Type:** Official Pothole Documentation")
            st.info("**Format:** PNG Image")
            st.info("**Status:** Ready to Generate")
        
        # Generate button
        if st.button("🎯 Generate Official Certificate", type="primary", use_container_width=True):
            if not road_name.strip():
                st.error("⚠️ Please enter a road name for the certificate")
            else:
                # Progress indication
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text('📄 Preparing certificate template...')
                progress_bar.progress(25)
                
                status_text.text('📊 Processing pothole data...')
                progress_bar.progress(50)
                
                status_text.text('🎨 Generating certificate design...')
                progress_bar.progress(75)
                
                with st.spinner("Generating certificate..."):
                    cert_img = generate_certificate(road_name.strip(), st.session_state.potholes)
                    cert_path = "pothole_certificate.png"
                    cert_img.save(cert_path)
                
                progress_bar.progress(100)
                status_text.text('✅ Certificate generated successfully!')
                
                st.markdown("---")
                
                # Display generated certificate
                st.markdown("### 🎉 Your Official Pothole Certificate")
                st.image(cert_path, caption="🚧 Official Pothole Documentation Certificate", use_column_width=True)
                
                # Download section
                st.markdown("### 📥 Download Certificate")
                
                with open(cert_path, "rb") as file:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.download_button(
                            label="📥 Download Certificate (PNG)",
                            data=file,
                            file_name=f"{road_name.strip().replace(' ', '_')}_pothole_certificate.png",
                            mime="image/png",
                            type="primary",
                            use_container_width=True,
                            help="Click to download your certificate as a PNG image"
                        )
                    
                    with col2:
                        st.markdown("**File Details:**")
                        st.caption(f"📁 Name: {road_name.strip()}_certificate.png")
                        st.caption("📊 Format: PNG Image")
                        st.caption("✅ Ready for download")
                
                # Success message
                st.markdown("""
                <div class="success-card">
                    <h4>🎊 Certificate Generated Successfully!</h4>
                    <p>Your official pothole documentation certificate is ready for download and can be used for:</p>
                    <ul>
                        <li>📋 Official road condition reports</li>
                        <li>🏛️ Municipal submissions</li>
                        <li>📄 Insurance documentation</li>
                        <li>📊 Infrastructure planning</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🚧 <strong>Vazhi Illae Kuzhi</strong> - Making roads safer, one pothole at a time!</p>
    <p>Built with ❤️ using Streamlit & AI</p>
</div>
""", unsafe_allow_html=True)