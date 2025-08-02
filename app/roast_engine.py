import random

def roast_pothole(pothole_data):
    """Enhanced roasting based on pothole characteristics"""
    area = pothole_data.get('area', 0)
    danger_level = pothole_data.get('danger_level', 'Unknown')
    is_water_filled = pothole_data.get('is_water_filled', False)
    water_percentage = pothole_data.get('water_percentage', 0)
    circularity = pothole_data.get('circularity', 0)
    
    # Water-specific roasts
    if is_water_filled and water_percentage > 50:
        water_roasts = [
            "Ayo! This one's got its own swimming pool! 🏊‍♂️",
            "Free bathing facility courtesy Roads Department! 🛁",
            "Mosquito breeding center detected! 🦟",
            "Somebody call the Navy, we found the Indian Ocean! 🌊",
            "Perfect spot for a romantic boat ride! 🚣‍♀️"
        ]
        return random.choice(water_roasts)
    
    # Danger level specific roasts
    if danger_level == "Critical":
        critical_roasts = [
            "BRUH! This isn't a pothole, it's a portal to the underworld! 👹",
            "NASA called - they want to use this as a moon crater simulator! 🌙",
            "This needs its own PIN code and municipal corporation! 🏛️",
            "Emergency! Call 108... for the road! 🚑",
            "Vehicle insurance companies hate this ONE SIMPLE TRICK! 💸"
        ]
        return random.choice(critical_roasts)
    
    elif danger_level == "High":
        high_roasts = [
            "This one's playing hide and seek with your car's undercarriage! 🙈",
            "Suspension killer incoming! RIP shocks! ⚰️",
            "Your chai will definitely spill here! ☕💥",
            "Speed breaker? Nah, this is a speed DESTROYER! 💀",
            "Plot twist: The road decided to take a vacation! 🏖️"
        ]
        return random.choice(high_roasts)
    
    elif danger_level == "Medium":
        medium_roasts = [
            "Medium spicy pothole! Just enough to ruin your mood! 🌶️",
            "Your car's going to have trust issues after this! 💔",
            "Not big enough for swimming, perfect for ankle sprains! 🦶",
            "Goldilocks pothole - not too big, not too small, just ANNOYING! 🐻",
            "This one whispers 'gotcha!' as you drive over it! 😈"
        ]
        return random.choice(medium_roasts)
    
    elif danger_level == "Low":
        low_roasts = [
            "Baby pothole taking its first steps into chaos! 👶",
            "Starter pack pothole - perfect for beginners! 📦",
            "This one's still in pothole kindergarten! 🎒",
            "Aww, look! A pothole in training! 🥺",
            "Not dangerous, just... disappointingly there! 😑"
        ]
        return random.choice(low_roasts)
    
    # Shape-based roasts
    if circularity > 0.8:
        return "Perfect circle! Did someone use a compass to dig this? 📐"
    elif circularity < 0.4:
        return "This pothole has commitment issues - can't decide its shape! 🤷‍♂️"
    
    # Area-based roasts (fallback)
    if area > 15000:
        return "This ain't a pothole, it's a geological feature! 🏔️"
    elif area > 8000:
        return "Big enough to host a small wedding! 💒"
    elif area > 3000:
        return "Medium-sized chaos generator! ⚡"
    else:
        return "Tiny but mighty road irritant! 🐜"

def roast_road_condition(potholes):
    """Roast the overall road condition"""
    if not potholes:
        return "Wow! A road smoother than my pickup lines! ✨"
    
    total_count = len(potholes)
    critical_count = len([p for p in potholes if p.get('danger_level') == 'Critical'])
    water_count = len([p for p in potholes if p.get('is_water_filled', False)])
    
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

def get_safety_tip(potholes):
    """Provide safety tips based on detected potholes"""
    if not potholes:
        return "Road looks good! Drive safe and enjoy the smooth ride! 🚗✨"
    
    critical_count = len([p for p in potholes if p.get('danger_level') == 'Critical'])
    water_count = len([p for p in potholes if p.get('is_water_filled', False)])
    
    tips = []
    
    if critical_count > 0:
        tips.append("⚠️ CRITICAL potholes detected! Reduce speed significantly!")
    
    if water_count > 0:
        tips.append("💧 Water-filled potholes present - depth unknown, proceed with caution!")
    
    tips.extend([
        "🚗 Maintain safe following distance",
        "🔦 Use headlights in low visibility",
        "📱 Report dangerous potholes to authorities"
    ])
    
    return " | ".join(tips[:3])  # Return top 3 tips

# Backward compatibility
def roast_pothole_legacy(area):
    """Legacy function for backward compatibility"""
    fake_pothole = {'area': area, 'danger_level': 'Medium', 'is_water_filled': False}
    return roast_pothole(fake_pothole)