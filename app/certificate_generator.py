from PIL import Image, ImageDraw, ImageFont
import datetime

def generate_certificate(road_name, pothole_data):
    width, height = 1000, 700
    cert = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(cert)

    title_font = ImageFont.truetype("arial.ttf", 40)
    subtitle_font = ImageFont.truetype("arial.ttf", 28)
    regular_font = ImageFont.truetype("arial.ttf", 22)
    small_font = ImageFont.truetype("arial.ttf", 18)

    # Title
    draw.text((width // 2 - 270, 40), "CERTIFICATE OF NEGLECTED INFRASTRUCTURE", font=title_font, fill="black")

    # Subtitle
    draw.text((width // 2 - 200, 100), "Issued in Recognition of Road Surface Degradation", font=subtitle_font, fill="black")

    # Road info
    draw.text((60, 180), f"Road Name: {road_name}", font=regular_font, fill="black")
    draw.text((60, 220), f"Total Potholes Identified: {len(pothole_data)}", font=regular_font, fill="black")

    # Pothole breakdown
    draw.text((60, 270), "Detailed Report:", font=regular_font, fill="black")
    for idx, pothole in enumerate(pothole_data, start=1):
        msg = f"{idx}. Approximate Area: {int(pothole['area'])} px² — Hazard Level: {get_danger(pothole['area'])}"
        draw.text((80, 310 + 30 * (idx - 1)), msg, font=small_font, fill="black")

    # Footer
    draw.text((60, 640), f"Issued on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", font=regular_font, fill="gray")
    draw.text((60, 670), "This document serves as formal acknowledgment of ongoing infrastructural oversight.", font=small_font, fill="gray")

    return cert

def get_danger(area):
    if area > 10000:
        return "Severe Structural Risk"
    elif area > 3000:
        return "Notable Safety Concern"
    else:
        return "Minor Surface Imperfection"
