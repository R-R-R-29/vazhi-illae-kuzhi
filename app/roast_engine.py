# Import the random module to enable random selection of roast messages
import random

# Function to generate a humorous roast based on pothole characteristics
def roast_pothole(pothole_data):
    """Enhanced roasting based on pothole characteristics"""
    area = pothole_data.get('area', 0)  # Get area of the pothole
    danger_level = pothole_data.get('danger_level', 'Unknown')  # Get danger level
    is_water_filled = pothole_data.get('is_water_filled', False)  # Check if water is filled
    water_percentage = pothole_data.get('water_percentage', 0)  # Get water percentage
    circularity = pothole_data.get('circularity', 0)  # Get circularity of the pothole
    
    # Water-specific roasts
    if is_water_filled and water_percentage > 50:
        water_roasts = [
            "Ayo! This one's got its own swimming pool! 🏊‍♂️",
            "Free bathing facility courtesy Roads Department! 🛁",
            "Mosquito breeding center detected! 🦟",
            "Somebody call the Navy, we found the Indian Ocean! 🌊",
            "Perfect spot for a romantic boat ride! 🚣‍♀️"
        ]
        return random.choice(water_roasts)  # Return a random water-based roast
    
    # Danger level specific roasts
    if danger_level == "Critical":
        critical_roasts = [
            "BRUH! This isn't a pothole, it's a portal to the underworld! 👹",
            "NASA called - they want to use this as a moon crater simulator! 🌙",
            "This needs its own PIN code and municipal corporation! 🏛️",
            "Emergency! Call 108... for the road! 🚑",
            "Vehicle insurance companies hate this ONE SIMPLE TRICK! 💸"
        ]
        return random.choice(critical_roasts)  # Return a critical-level roast
    
    elif danger_level == "High":
        high_roasts = [
            "This one's playing hide and seek with your car's undercarriage! 🙈",
            "Suspension killer incoming! RIP shocks! ⚰️",
            "Your chai will definitely spill here! ☕💥",
            "Speed breaker? Nah, this is a speed DESTROYER! 💀",
            "Plot twist: The road decided to take a vacation! 🏖️"
        ]
        return random.choice(high_roasts)  # Return a high-level roast
    
    elif danger_level == "Medium":
        medium_roasts = [
            "Medium spicy pothole! Just enough to ruin your mood! 🌶️",
            "Your car's going to have trust issues after this! 💔",
            "Not big enough for swimming, perfect for ankle sprains! 🦶",
            "Goldilocks pothole - not too big, not too small, just ANNOYING! 🐻",
            "This one whispers 'gotcha!' as you drive over it! 😈"
        ]
        return random.choice(medium_roasts)  # Return a medium-level roast
    
    elif danger_level == "Low":
        low_roasts = [
            "Baby pothole taking its first steps into chaos! 👶",
            "Starter pack pothole - perfect for beginners! 📦",
            "This one's still in pothole kindergarten! 🎒",
            "Aww, look! A pothole in training! 🥺",
            "Not dangerous, just... disappointingly there! 😑"
        ]
        return random.choice(low_roasts)  # Return a low-level roast
    
    # Shape-based roasts
    if circularity > 0.8:
        return "Perfect circle! Did someone use a compass to dig this? 📐"  # Roast for circular potholes
    elif circularity < 0.4:
        return "This pothole has commitment issues - can't decide its shape! 🤷‍♂️"  # Roast for irregular shape
    
    # Area-based roasts (fallback)
    if area > 15000:
        return "This ain't a pothole, it's a geological feature! 🏔️"  # Roast for very large area
    elif area > 8000:
        return "Big enough to host a small wedding! 💒"  # Roast for large area
    elif area > 3000:
        return "Medium-sized chaos generator! ⚡"  # Roast for medium area
    else:
        return "Tiny but mighty road irritant! 🐜"  # Roast for small area

# Function to roast the overall road condition based on list of potholes
def roast_road_condition(potholes):
    """Roast the overall road condition"""
    if not potholes:
        return "Wow! A road smoother than my pickup lines! ✨"  # Roast for perfect road
    
    total_count = len(potholes)  # Total number of potholes
    critical_count = len([p for p in potholes if p.get('danger_level') == 'Critical'])  # Count critical ones
    water_count = len([p for p in potholes if p.get('is_water_filled', False)])  # Count water-filled ones
    
    if critical_count > 5:
        return f"This road has {critical_count} critical potholes! It's not a road, it's an obstacle course! 🏃‍♂️💨"
    elif total_count > 10:
        return f"{total_count} potholes detected! This road is more hole than road! 🕳️"
    elif water_count > 3:
        return f"{water_count} water-filled potholes! Perfect for a splash party! 💦🎉"
    elif total_count > 5:
        return f"{total_count} potholes found! Road maintenance took a long vacation! 🏖️"
    else:
        return f"Only {total_count} potholes! Not bad, but still annoying! 😤"

# Function to provide driving safety tips based on detected potholes
def get_safety_tip(potholes):
    """Provide safety tips based on detected potholes"""
    if not potholes:
        return "Road looks good! Drive safe and enjoy the smooth ride! 🚗✨"  # Tip for clean road
    
    critical_count = len([p for p in potholes if p.get('danger_level') == 'Critical'])  # Count critical potholes
    water_count = len([p for p in potholes if p.get('is_water_filled', False)])  # Count water-filled potholes
    
    tips = []  # Initialize list to collect tips
    
    if critical_count > 0:
        tips.append("⚠️ CRITICAL potholes detected! Reduce speed significantly!")  # Tip for critical potholes
    
    if water_count > 0:
        tips.append("💧 Water-filled potholes present - depth unknown, proceed with caution!")  # Tip for water-filled
    
    tips.extend([
        "🚗 Maintain safe following distance",  # Generic safety tip
        "🔦 Use headlights in low visibility",  # Visibility tip
        "📱 Report dangerous potholes to authorities"  # Encourage civic reporting
    ])
    
    return " | ".join(tips[:3])  # Return top 3 tips

# Legacy function for backward compatibility using only area
def roast_pothole_legacy(area):
    """Legacy function for backward compatibility"""
    fake_pothole = {'area': area, 'danger_level': 'Medium', 'is_water_filled': False}  # Simulate pothole input
    return roast_pothole(fake_pothole)  # Use main roast function
