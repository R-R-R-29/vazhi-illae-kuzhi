import random

def roast_pothole(area):
    if area > 10000:
        return random.choice([
            "Bruh, is that a crater or a portal to another dimension?",
            "This one needs its own postal code!",
            "NASA might land on this by mistake!"
        ])
    elif area > 3000:
        return random.choice([
            "Enough to break your morning chai dreams!",
            "Medium-sized chaos right there!",
            "Could host a baby swimming pool!"
        ])
    else:
        return random.choice([
            "Just a mini road pimple 😏",
            "Tiny but mighty enough to trip your soul!",
            "It’s a starter pack pothole!"
        ])
