def get_daily_horoscope(natal_moon_sign: int, transit_moon_sign: int):
    """
    Generates a daily horoscope based on the transit of the Moon relative to the natal Moon.
    Signs are 1 (Aries) to 12 (Pisces).
    """
    if not (1 <= natal_moon_sign <= 12) or not (1 <= transit_moon_sign <= 12):
        return {"error": "Invalid moon signs."}
        
    # Calculate distance: if natal is 1 and transit is 1, distance is 1 (1st house from natal moon)
    # If natal is 12 and transit is 1, distance is 2 (2nd house)
    relative_house = ((transit_moon_sign - natal_moon_sign) % 12) + 1
    
    predictions = {
        1: {
            "title": "Focus on Self & Emotions",
            "prediction": "The Moon is transiting your natal Moon sign today. You may feel more emotionally sensitive but also more in tune with your true needs. It's an excellent day for self-care, personal projects, and setting new intentions. Trust your intuition.",
            "lucky_color": "White",
            "mood": "Reflective"
        },
        2: {
            "title": "Financial Matters & Family",
            "prediction": "The Moon transits the 2nd house from your natal Moon. Focus turns toward your finances, investments, and personal resources. You might find joy in family gatherings or good food. Avoid impulsive purchases and think long-term.",
            "lucky_color": "Silver",
            "mood": "Practical"
        },
        3: {
            "title": "Courage & Communication",
            "prediction": "With the Moon in the 3rd house from your birth sign, your communication skills are heightened. It's a great day for networking, short travels, and clearing out your inbox. You'll feel a surge of courage to tackle pending tasks.",
            "lucky_color": "Light Green",
            "mood": "Energetic"
        },
        4: {
            "title": "Home, Comfort & Mother",
            "prediction": "The Moon in the 4th house brings focus to your domestic life and inner peace. You might prefer staying indoors or spending quality time with family, especially mother figures. Take care of your emotional well-being today.",
            "lucky_color": "Blue",
            "mood": "Peaceful"
        },
        5: {
            "title": "Creativity & Romance",
            "prediction": "The 5th house transit of the Moon lights up your creative and romantic sectors. It's a joyful day for hobbies, spending time with children, or enjoying entertainment. Your intellect is sharp, making it good for learning.",
            "lucky_color": "Yellow",
            "mood": "Joyful"
        },
        6: {
            "title": "Health & Overcoming Obstacles",
            "prediction": "The Moon transits your 6th house today. Focus on your daily routines, diet, and health. You have the upper hand over competitors, but avoid getting into unnecessary arguments. A good day for organizing your workspace.",
            "lucky_color": "Earth Tones",
            "mood": "Productive"
        },
        7: {
            "title": "Partnerships & Relationships",
            "prediction": "With the Moon in the 7th house, relationships—both business and personal—take center stage. Compromise and diplomacy will go a long way. It's a favorable day for signing agreements or spending quality time with your spouse.",
            "lucky_color": "Pink",
            "mood": "Harmonious"
        },
        8: {
            "title": "Caution & Introspection",
            "prediction": "The Moon transiting the 8th house suggests taking things slow. You might feel a bit anxious or face sudden changes in plans. It's better to avoid starting major new ventures today. Focus on research, meditation, or hidden matters.",
            "lucky_color": "Dark Blue",
            "mood": "Introspective"
        },
        9: {
            "title": "Luck, Travel & Dharma",
            "prediction": "The 9th house transit brings a touch of luck and expansiveness. You might feel drawn to spiritual or philosophical subjects. It's an excellent day for long-distance travel planning, higher learning, and seeking advice from mentors.",
            "lucky_color": "Gold",
            "mood": "Optimistic"
        },
        10: {
            "title": "Career & Public Image",
            "prediction": "The Moon in the 10th house puts the spotlight on your professional life. Your hard work is visible to superiors, making it a great day to step up and take responsibilities. Maintain a professional demeanor to make the best of today.",
            "lucky_color": "Black",
            "mood": "Ambitious"
        },
        11: {
            "title": "Gains, Friends & Networking",
            "prediction": "A highly favorable 11th house transit brings opportunities for gains and fulfillment of desires. Socializing, networking, and spending time with friends will bring joy and possible beneficial connections. Share your ideas freely.",
            "lucky_color": "Purple",
            "mood": "Social"
        },
        12: {
            "title": "Rest & Spirituality",
            "prediction": "The Moon in the 12th house indicates a need for rest and retreat. You might feel drained by too much social interaction. Watch out for unnecessary expenses. It's the perfect day for meditation, sleep, and letting go of the past.",
            "lucky_color": "Sea Green",
            "mood": "Quiet"
        }
    }
    
    rashi_names = [
        "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", 
        "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)", 
        "Tula (Libra)", "Vrishchika (Scorpio)", "Dhanu (Sagittarius)", 
        "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
    ]
    
    result = predictions.get(relative_house)
    result["natal_rashi"] = rashi_names[natal_moon_sign - 1]
    result["transit_rashi"] = rashi_names[transit_moon_sign - 1]
    result["relative_house"] = relative_house
    
    return result
