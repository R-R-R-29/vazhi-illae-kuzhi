import random

names = [
    "Scooter Swallower", 
    "Frog Palace", 
    "Auto Trap", 
    "Kuzhi Raja", 
    "Deathly Ditch", 
    "Tyre Terminator", 
    "Suspension Slayer", 
    "The Abyss", 
    "Bumper Snapper", 
    "Rainwater Jacuzzi",
    "Mini Mariana", 
    "Spine Realigner", 
    "Wheelbreaker 3000",
    "Shock Absorber's Hell",
    "The Dark Hole of Doom",
    "The Crater Formerly Known as Road"
]

def roast_pothole(area):
    name = random.choice(names)

    try:
        area = float(area)  # Make sure it's numeric
    except (TypeError, ValueError):
        return f"{name} – 🤷‍♀️ Unknown sized kuzhi"

    if area > 10000:
        roast = f"{name} – ☠️ Bro, this one's big enough to host a wedding!"
    elif area > 5000:
        roast = f"{name} – ⚠️ That’s not a pothole, that’s a swimming pool!"
    elif area > 2000:
        roast = f"{name} – 🟡 Your shock absorbers are praying right now."
    else:
        roast = f"{name} – 🟢 Baby kuzhi, but still ready to mess your ride."

    return roast
