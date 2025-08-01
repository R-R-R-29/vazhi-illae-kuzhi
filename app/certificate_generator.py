from PIL import Image, ImageDraw, ImageFont
import datetime

def generate_certificate(road_name, pothole_data):
    width, height = 1000, 700
    cert = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(cert)

    title_font = ImageFont.truetype("arial.ttf", 40)
    regular_font = ImageFont.truetype("arial.ttf", 24)

    draw.text((width // 2 - 250, 50), "🏆 Official Pothole Certificate 🏆", font=title_font, fill="black")

    draw.text((50, 150), f"📍 Road Name: {road_name}", font=regular_font, fill="black")
    draw.text((50, 200), f"🕳️ Total Potholes Detected: {len(pothole_data)}", font=regular_font, fill="black")

    for idx, pothole in enumerate(pothole_data, start=1):
        msg = f"{idx}. Area: {int(pothole['area'])} px² — Danger: {get_danger(pothole['area'])}"
        draw.text((70, 250 + 30 * (idx - 1)), msg, font=regular_font, fill="black")

    draw.text((50, 650), f"🗓️ Issued on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", font=regular_font, fill="gray")

    return cert

def get_danger(area):
    if area > 10000:
        return "☠️ EXTREME"
    elif area > 3000:
        return "⚠️ Moderate"
    else:
        return "🙂 Tiny"
