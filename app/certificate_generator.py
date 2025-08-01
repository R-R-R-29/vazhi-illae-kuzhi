from PIL import Image, ImageDraw, ImageFont
import datetime
import random

def generate_certificate(road_name, pothole_data):
    width, height = 1200, 900
    cert = Image.new("RGB", (width, height), color="#FFF8DC")  # Cream background
    draw = ImageDraw.Draw(cert)

    # Try to load fonts, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
        regular_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw a fancy border
    draw.rectangle([10, 10, width-10, height-10], outline="red", width=5)
    draw.rectangle([20, 20, width-20, height-20], outline="gold", width=3)

    # Funny title
    draw.text((width // 2 - 280, 40), "🎭 OFFICIAL MOCK CERTIFICATE OF", font=subtitle_font, fill="red")
    draw.text((width // 2 - 320, 80), "🕳️ POTHOLE EXCELLENCE & CHAOS 🕳️", font=title_font, fill="darkred")
    
    # Mock disclaimer - very prominent
    draw.text((width // 2 - 200, 130), "⚠️ THIS IS A PARODY CERTIFICATE ⚠️", font=subtitle_font, fill="red")
    draw.text((width // 2 - 250, 155), "Created to MOCK poor road conditions & raise awareness!", font=regular_font, fill="darkred")

    # Funny subtitle
    funny_subtitles = [
        "Proudly Certifying Roads That Identify as Swiss Cheese 🧀",
        "Where Every Journey is an Adventure in Suspension Repair 🚗💥",
        "Officially Recognizing Roads That Double as Moon Surface Training 🌙",
        "Celebrating Infrastructure That Makes Minecraft Look Realistic 🎮"
    ]
    subtitle = random.choice(funny_subtitles)
    draw.text((50, 190), subtitle, font=regular_font, fill="purple")

    # Road information with humor
    draw.text((50, 240), f"📍 Road of 'Honor': {road_name}", font=regular_font, fill="black")
    draw.text((50, 270), f"🕳️ Total Crater Count: {len(pothole_data)} magnificent specimens", font=regular_font, fill="black")
    
    # Funny road condition assessment
    total_area = sum(p['area'] for p in pothole_data)
    if len(pothole_data) > 5:
        condition = "🌋 APOCALYPTIC - This road has given up on life"
    elif len(pothole_data) > 3:
        condition = "💀 CATASTROPHIC - Cars go to die here"
    elif len(pothole_data) > 1:
        condition = "🤕 PAINFUL - Your car will need therapy"
    elif len(pothole_data) == 1:
        condition = "😅 LONELY HOLE - At least it has character"
    else:
        condition = "🌈 UNICORN ROAD - Doesn't actually exist"
    
    draw.text((50, 300), f"🏆 Official Road Condition: {condition}", font=regular_font, fill="darkgreen")

    # Individual pothole roasts
    draw.text((50, 350), "🎪 Individual Pothole Hall of Fame:", font=regular_font, fill="darkblue")
    
    for idx, pothole in enumerate(pothole_data, start=1):
        area = int(pothole['area'])
        roast = get_funny_pothole_description(area, idx)
        y_pos = 380 + 35 * (idx - 1)
        if y_pos < height - 200:  # Don't overflow
            draw.text((70, y_pos), f"🕳️ Pothole #{idx}: {roast}", font=regular_font, fill="darkred")

    # Funny official stamps and signatures
    stamp_y = height - 180
    draw.text((50, stamp_y), "🎭 Certified by: The Department of Comedic Road Disasters", font=regular_font, fill="blue")
    draw.text((50, stamp_y + 25), "📋 Approved by: Chief Inspector of Vehicular Torture Devices", font=regular_font, fill="blue")
    draw.text((50, stamp_y + 50), "🏛️ Ministry of 'We'll Fix It Tomorrow' (Est. Never)", font=regular_font, fill="blue")

    # Mock official seal
    draw.ellipse([width-200, stamp_y-20, width-50, stamp_y+80], outline="red", width=3)
    draw.text((width-180, stamp_y+10), "OFFICIAL", font=small_font, fill="red")
    draw.text((width-175, stamp_y+25), "MOCK", font=small_font, fill="red")
    draw.text((width-175, stamp_y+40), "SEAL", font=small_font, fill="red")

    # Disclaimer at bottom
    draw.text((50, height-80), "⚠️ IMPORTANT: This certificate is SATIRICAL and created to highlight poor road conditions.", font=regular_font, fill="red")
    draw.text((50, height-55), "It has NO legal value and is meant to raise PUBLIC AWARENESS about infrastructure issues.", font=regular_font, fill="red")
    draw.text((50, height-30), f"🗓️ Date of Mock Certification: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | Made with 💔 for better roads", font=small_font, fill="gray")

    return cert

def get_funny_pothole_description(area, index):
    """Generate hilarious descriptions for potholes based on their area"""
    
    if area > 15000:
        descriptions = [
            f"Area: {area} px² - This isn't a pothole, it's a swimming pool without water! 🏊‍♂️",
            f"Area: {area} px² - NASA called, they want to use this as a Mars rover testing site 🚀",
            f"Area: {area} px² - Congratulations! You've discovered a new geological formation! 🏔️",
            f"Area: {area} px² - This pothole has its own weather system ⛈️"
        ]
    elif area > 8000:
        descriptions = [
            f"Area: {area} px² - Perfect size for a small car to take a nap in 🚗💤",
            f"Area: {area} px² - This pothole charges rent to passing vehicles 💰",
            f"Area: {area} px² - Local wildlife has established a colony here 🐸",
            f"Area: {area} px² - This hole has commitment issues - it keeps getting deeper! 💔"
        ]
    elif area > 3000:
        descriptions = [
            f"Area: {area} px² - Medium-rare pothole, just the way suspension systems hate it 🥩",
            f"Area: {area} px² - This pothole went to college and got a degree in tire destruction 🎓",
            f"Area: {area} px² - Perfectly sized to swallow your hopes and dreams 😢",
            f"Area: {area} px² - This pothole practices yoga - it's very flexible with your wheel alignment 🧘‍♀️"
        ]
    elif area > 1000:
        descriptions = [
            f"Area: {area} px² - Bite-sized pothole for when you want just a little vehicular suffering 🍪",
            f"Area: {area} px² - This pothole is still learning, but shows great potential for chaos 📚",
            f"Area: {area} px² - Modest pothole with big dreams of becoming a sinkhole 🌟",
            f"Area: {area} px² - This pothole believes in minimalism - maximum damage, minimum size 🎨"
        ]
    else:
        descriptions = [
            f"Area: {area} px² - Baby pothole! Aww, look how it's trying to destroy your car 👶",
            f"Area: {area} px² - This pothole is just getting started in its career of vehicular terrorism 🔰",
            f"Area: {area} px² - Tiny but mighty! Like a mosquito bite for your tires 🦟",
            f"Area: {area} px² - This pothole is still in training at Pothole University 🎓"
        ]
    
    return random.choice(descriptions)

def get_danger(area):
    """Keep the original function for backward compatibility"""
    if area > 10000:
        return "☠️ EXTREME"
    elif area > 3000:
        return "⚠️ Moderate"
    else:
        return "🙂 Tiny"
