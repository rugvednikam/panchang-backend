from datetime import datetime
from app.calculations.v6_doshas import get_house

def get_current_mahadasha(dasha_data: dict) -> str:
    now = datetime.now()
    for period in dasha_data.get("periods", []):
        start = datetime.fromisoformat(period["start_date"])
        end = datetime.fromisoformat(period["end_date"])
        if start <= now <= end:
            return period["planet"]
    return "Unknown"

def _get_planets_in_house(kundli: dict, target_house: int) -> list:
    asc_rashi = kundli["ascendant"]["rashi"]
    planets = []
    for p in kundli["planets"]:
        if get_house(p["rashi"], asc_rashi) == target_house:
            planets.append(p["name"])
    return planets

def generate_career_prediction(kundli: dict, dasha_data: dict) -> dict:
    mahadasha = get_current_mahadasha(dasha_data)
    planets_10th = _get_planets_in_house(kundli, 10)
    
    text = f"The current Mahadasha of {mahadasha} indicates a period of dynamic professional shifts. "
    
    if "Surya" in planets_10th:
        text += "With the Sun illuminating your 10th house of career, you are naturally positioned for leadership and recognition. "
    elif "Shani" in planets_10th:
        text += "Saturn's presence in your career sector demands hard work and discipline, but promises long-term, stable success. "
    elif "Guru" in planets_10th:
        text += "Jupiter brings tremendous expansion and wisdom to your professional life, making this a great time for consulting or teaching. "
    elif not planets_10th:
        text += "Your career house is currently an open canvas, suggesting you have the flexibility to pivot paths without heavy karmic resistance. "
        
    if mahadasha in ["Shukra", "Guru", "Budh"]:
        text += "This planetary cycle is highly supportive for financial gains and expanding your professional network."
    elif mahadasha in ["Shani", "Rahu", "Ketu"]:
        text += "This phase asks for patience and strategic planning rather than impulsive career changes."
        
    return {
        "title": "Career & Wealth",
        "icon": "work_outline",
        "description": text.strip()
    }

def generate_love_prediction(kundli: dict, dasha_data: dict) -> dict:
    mahadasha = get_current_mahadasha(dasha_data)
    planets_7th = _get_planets_in_house(kundli, 7)
    
    text = ""
    
    if "Shukra" in planets_7th:
        text += "Venus in your 7th house creates a powerful magnetism, bringing intense harmony and passion into your relationships. "
    elif "Mangal" in planets_7th:
        text += "Mars in your relationship sector adds fiery passion, but requires you to actively manage temper and impatience with your partner. "
    elif "Ketu" in planets_7th:
        text += "Ketu's placement suggests a deeply spiritual or unconventional approach to partnerships, often feeling detached from standard relationship norms. "
    else:
        text += "Your relationship sector is relatively balanced. The energy you put into your partnerships is exactly what you will get back. "
        
    if mahadasha == "Shukra":
        text += "Being in the Mahadasha of Venus, this is the ultimate period for romance, marriage, and aesthetic pleasures."
    elif mahadasha == "Chandra":
        text += "The Moon's cycle brings deep emotional bonding and a strong desire for security in your love life."
    else:
        text += f"The current {mahadasha} cycle brings a practical, grounded energy to how you approach commitments."
        
    return {
        "title": "Love & Relationships",
        "icon": "favorite_border",
        "description": text.strip()
    }

def generate_health_prediction(kundli: dict, dasha_data: dict) -> dict:
    mahadasha = get_current_mahadasha(dasha_data)
    planets_6th = _get_planets_in_house(kundli, 6)
    
    text = "Overall vitality is strong, but the cosmos suggests specific areas of focus. "
    
    if "Shani" in planets_6th:
        text += "Saturn in the 6th house is actually a strong placement for overcoming illness, giving you a robust immune system over time. "
    elif "Rahu" in planets_6th:
        text += "Rahu here gives you the energy to crush obstacles, but beware of mysterious or stress-related ailments. "
    elif "Chandra" in planets_6th:
        text += "The Moon's placement indicates that your physical health is deeply tied to your emotional well-being. Prioritize mental rest. "
    
    if mahadasha in ["Surya", "Mangal"]:
        text += f"Under the fiery influence of the {mahadasha} Mahadasha, you have excess physical energy. Channel this into regular exercise to avoid inflammation."
    elif mahadasha in ["Guru", "Shukra"]:
        text += f"The {mahadasha} period brings a tendency to overindulge. Be mindful of your diet and sugar intake."
        
    return {
        "title": "Health & Vitality",
        "icon": "health_and_safety_outlined",
        "description": text.strip()
    }

def get_all_predictions(kundli: dict, dasha_data: dict) -> list:
    return [
        generate_career_prediction(kundli, dasha_data),
        generate_love_prediction(kundli, dasha_data),
        generate_health_prediction(kundli, dasha_data)
    ]
