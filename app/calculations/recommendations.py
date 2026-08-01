from typing import Dict, List, Any

# Map of signs to their lord planet
SIGN_LORDS = {
    1: "Mars",      # Aries
    2: "Venus",     # Taurus
    3: "Mercury",   # Gemini
    4: "Moon",      # Cancer
    5: "Sun",       # Leo
    6: "Mercury",   # Virgo
    7: "Venus",     # Libra
    8: "Mars",      # Scorpio
    9: "Jupiter",   # Sagittarius
    10: "Saturn",   # Capricorn
    11: "Saturn",   # Aquarius
    12: "Jupiter"   # Pisces
}

# Map of planet to its primary gemstone
GEMSTONES = {
    "Sun": {
        "name": "Ruby",
        "metal": "Gold or Copper",
        "finger": "Ring Finger",
        "day": "Sunday",
        "deity": "Surya",
        "benefits": "Enhances leadership, confidence, health, and vitality."
    },
    "Moon": {
        "name": "Pearl",
        "metal": "Silver",
        "finger": "Little Finger",
        "day": "Monday",
        "deity": "Chandra",
        "benefits": "Brings mental peace, emotional stability, and creativity."
    },
    "Mars": {
        "name": "Red Coral",
        "metal": "Gold or Copper",
        "finger": "Ring Finger",
        "day": "Tuesday",
        "deity": "Mangal / Hanuman",
        "benefits": "Boosts courage, energy, property matters, and blood health."
    },
    "Mercury": {
        "name": "Emerald",
        "metal": "Gold or Silver",
        "finger": "Little Finger",
        "day": "Wednesday",
        "deity": "Budh / Ganesha",
        "benefits": "Improves intellect, communication, business, and memory."
    },
    "Jupiter": {
        "name": "Yellow Sapphire",
        "metal": "Gold",
        "finger": "Index Finger",
        "day": "Thursday",
        "deity": "Brihaspati / Vishnu",
        "benefits": "Brings wealth, wisdom, good fortune, and marital bliss."
    },
    "Venus": {
        "name": "Diamond or White Sapphire",
        "metal": "Gold or Platinum",
        "finger": "Middle or Ring Finger",
        "day": "Friday",
        "deity": "Shukra / Goddess Lakshmi",
        "benefits": "Attracts luxury, romance, beauty, and artistic success."
    },
    "Saturn": {
        "name": "Blue Sapphire",
        "metal": "Silver, Platinum, or Iron",
        "finger": "Middle Finger",
        "day": "Saturday",
        "deity": "Shani",
        "benefits": "Provides discipline, success in career, and removes obstacles."
    }
}

# Map of Nakshatras to Rudraksha
NAKSHATRA_RUDRAKSHA = {
    1: {"mukhi": "9 Mukhi", "ruling_planet": "Ketu", "benefits": "Brings courage and removes fears."},
    2: {"mukhi": "6 Mukhi", "ruling_planet": "Venus", "benefits": "Enhances focus, wisdom, and brings luxury."},
    3: {"mukhi": "12 Mukhi", "ruling_planet": "Sun", "benefits": "Brings leadership, radiance, and removes stress."},
    4: {"mukhi": "2 Mukhi", "ruling_planet": "Moon", "benefits": "Brings emotional balance and harmony in relationships."},
    5: {"mukhi": "3 Mukhi", "ruling_planet": "Mars", "benefits": "Boosts self-esteem, energy, and burns past karmas."},
    6: {"mukhi": "8 Mukhi", "ruling_planet": "Rahu", "benefits": "Removes obstacles and brings success in endeavors."},
    7: {"mukhi": "5 Mukhi", "ruling_planet": "Jupiter", "benefits": "Brings health, peace, and spiritual growth."},
    8: {"mukhi": "7 Mukhi", "ruling_planet": "Saturn", "benefits": "Attracts wealth, opportunities, and reduces Saturn's malefic effects."},
    9: {"mukhi": "4 Mukhi", "ruling_planet": "Mercury", "benefits": "Enhances communication, intelligence, and vocal power."},
    10: {"mukhi": "9 Mukhi", "ruling_planet": "Ketu", "benefits": "Brings courage and removes fears."},
    11: {"mukhi": "6 Mukhi", "ruling_planet": "Venus", "benefits": "Enhances focus, wisdom, and brings luxury."},
    12: {"mukhi": "12 Mukhi", "ruling_planet": "Sun", "benefits": "Brings leadership, radiance, and removes stress."},
    13: {"mukhi": "2 Mukhi", "ruling_planet": "Moon", "benefits": "Brings emotional balance and harmony in relationships."},
    14: {"mukhi": "3 Mukhi", "ruling_planet": "Mars", "benefits": "Boosts self-esteem, energy, and burns past karmas."},
    15: {"mukhi": "8 Mukhi", "ruling_planet": "Rahu", "benefits": "Removes obstacles and brings success in endeavors."},
    16: {"mukhi": "5 Mukhi", "ruling_planet": "Jupiter", "benefits": "Brings health, peace, and spiritual growth."},
    17: {"mukhi": "7 Mukhi", "ruling_planet": "Saturn", "benefits": "Attracts wealth, opportunities, and reduces Saturn's malefic effects."},
    18: {"mukhi": "4 Mukhi", "ruling_planet": "Mercury", "benefits": "Enhances communication, intelligence, and vocal power."},
    19: {"mukhi": "9 Mukhi", "ruling_planet": "Ketu", "benefits": "Brings courage and removes fears."},
    20: {"mukhi": "6 Mukhi", "ruling_planet": "Venus", "benefits": "Enhances focus, wisdom, and brings luxury."},
    21: {"mukhi": "12 Mukhi", "ruling_planet": "Sun", "benefits": "Brings leadership, radiance, and removes stress."},
    22: {"mukhi": "2 Mukhi", "ruling_planet": "Moon", "benefits": "Brings emotional balance and harmony in relationships."},
    23: {"mukhi": "3 Mukhi", "ruling_planet": "Mars", "benefits": "Boosts self-esteem, energy, and burns past karmas."},
    24: {"mukhi": "8 Mukhi", "ruling_planet": "Rahu", "benefits": "Removes obstacles and brings success in endeavors."},
    25: {"mukhi": "5 Mukhi", "ruling_planet": "Jupiter", "benefits": "Brings health, peace, and spiritual growth."},
    26: {"mukhi": "7 Mukhi", "ruling_planet": "Saturn", "benefits": "Attracts wealth, opportunities, and reduces Saturn's malefic effects."},
    27: {"mukhi": "4 Mukhi", "ruling_planet": "Mercury", "benefits": "Enhances communication, intelligence, and vocal power."},
}

class RecommendationsCalculator:
    
    @staticmethod
    def get_gemstones(ascendant_sign: int) -> Dict[str, Any]:
        """
        Calculates Life Stone, Lucky Stone, and Fortune Stone based on Ascendant.
        Life Stone: Lord of 1st House (Lagna)
        Lucky Stone: Lord of 5th House
        Fortune Stone: Lord of 9th House
        """
        first_lord = SIGN_LORDS[ascendant_sign]
        fifth_sign = ((ascendant_sign + 4 - 1) % 12) + 1
        fifth_lord = SIGN_LORDS[fifth_sign]
        ninth_sign = ((ascendant_sign + 8 - 1) % 12) + 1
        ninth_lord = SIGN_LORDS[ninth_sign]
        
        return {
            "life_stone": {
                "type": "Life Stone",
                "planet": first_lord,
                **GEMSTONES[first_lord]
            },
            "lucky_stone": {
                "type": "Lucky Stone",
                "planet": fifth_lord,
                **GEMSTONES[fifth_lord]
            },
            "fortune_stone": {
                "type": "Fortune Stone",
                "planet": ninth_lord,
                **GEMSTONES[ninth_lord]
            }
        }

    @staticmethod
    def get_rudraksha(nakshatra_number: int) -> Dict[str, Any]:
        """
        Recommends Rudraksha based on Nakshatra.
        """
        if nakshatra_number in NAKSHATRA_RUDRAKSHA:
            return NAKSHATRA_RUDRAKSHA[nakshatra_number]
        return {"mukhi": "5 Mukhi", "ruling_planet": "Jupiter", "benefits": "General well-being and peace."}
