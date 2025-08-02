# Import required modules from PIL for image generation and drawing
from PIL import Image, ImageDraw, ImageFont
# Import datetime to generate the issue date for the certificate
import datetime

# Function to generate a humorous certificate for road potholes
def generate_certificate(road_name, pothole_data):
    width, height = 1000, 700  # Define dimensions for the certificate image
    cert = Image.new("RGB", (width, height), color="white")  # Create a blank white image
    draw = ImageDraw.Draw(cert)  # Create a drawing context for the image

    # Load various font sizes for title, subtitle, body, and small text
    title_font = ImageFont.truetype("arial.ttf", 40)
    subtitle_font = ImageFont.truetype("arial.ttf", 28)
    regular_font = ImageFont.truetype("arial.ttf", 22)
    small_font = ImageFont.truetype("arial.ttf", 18)

    # Title
    draw.text((width // 2 - 270, 40), "CERTIFICATE OF NEGLECTED INFRASTRUCTURE", font=title_font, fill="black")  # Draw title text

    # Subtitle
    draw.text((width // 2 - 200, 100), "Issued in Recognition of Road Surface Degradation", font=subtitle_font, fill="black")  # Draw subtitle text

    # Road info
    draw.text((60, 180), f"Road Name: {road_name}", font=regular_font, fill="black")  # Display road name
    draw.text((60, 220), f"Total Potholes Identified: {len(pothole_data)}", font=regular_font, fill="black")  # Display pothole count

    # Pothole breakdown
    draw.text((60, 270), "Detailed Report:", font=regular_font, fill="black")  # Section header for pothole list
    for idx, pothole in enumerate(pothole_data, start=1):  # Enumerate through each pothole
        msg = f"{idx}. Approximate Area: {int(pothole['area'])} px² — Hazard Level: {get_danger(pothole['area'])}"  # Generate message
        draw.text((80, 310 + 30 * (idx - 1)), msg, font=small_font, fill="black")  # Draw each pothole's details

    # Footer
    draw.text((60, 640), f"Issued on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", font=regular_font, fill="gray")  # Timestamp
    draw.text((60, 670), "This document serves as formal acknowledgment of ongoing infrastructural oversight.", font=small_font, fill="gray")  # Closing statement

    return cert  # Return the generated certificate image

# Helper function to determine hazard level based on area
def get_danger(area):
    if area > 10000:
        return "Severe Structural Risk"  # Large pothole
    elif area > 3000:
        return "Notable Safety Concern"  # Medium pothole
    else:
        return "Minor Surface Imperfection"  # Small pothole
