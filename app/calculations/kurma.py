def get_kurma_chakra(
    nakshatra: int = 13,
    planet: str = "Saturn",
    planet_nak: int = 20,
    muhurta_type: str = "marriage"
):
    kurma_parts = {
        "mukha_face": {"nakshatras": [1, 2, 3], "result": "ASHUBH", "malefic": "Ati Ashubh Death", "benefic": "Madhyam"},
        "hasta": {"nakshatras": [4, 5, 6, 7], "result": "MADHYAM"},
        "kukshi": {"nakshatras": [8, 9, 10, 11, 12, 13], "result": "SHUBH"},
        "prishtha": {"nakshatras": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "result": "ATI SHUBH Best, Malefic becomes Shubh"},
        "puccha": {"nakshatras": [24, 25, 26, 27], "result": "ASHUBH"}
    }
    
    def find_part(nak):
        for part, data in kurma_parts.items():
            if nak in data["nakshatras"]:
                return part, data
        return "prishtha", kurma_parts["prishtha"]
        
    planet_part, planet_data = find_part(planet_nak)
    
    benefic = ["Jupiter", "Venus", "Mercury", "Moon"]
    malefic = ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]
    
    score = 3 if planet_part == "prishtha" else -3 if planet_part == "mukha_face" else 1
    if planet in malefic and planet_part == "prishtha": 
        score += 2
        
    auspicious = score >= 1
    
    return {
        "kurma_chakra": kurma_parts,
        "planet_part": planet_part,
        "auspicious": auspicious,
        "score": score,
        "result": f"{'SHUBH' if auspicious else 'ASHUBH'} - {planet} in {planet_part} ({planet_data['result']})",
        "remedy": f"{'No remedy' if auspicious else 'Kurma avatar puja, wait till Prishtha'}"
    }

def get_numerology_kurma_kundali(
    dob: str = "1990-05-20",
    name: str = "Prasad",
    house: str = "101"
):
    def red(n):
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n
        
    level = [int(d) for d in dob if d.isdigit()]
    mulank = red(level[0] if len(level) > 0 else 1)
    bhagyank = red(sum(level))
    house_s = red(sum(int(d) for d in house if d.isdigit()) or 1)
    
    kurma = {
        "head_9": {"nums": [9], "planet": "Mars", "res": "Raksha BEST"},
        "neck_6": {"nums": [6], "planet": "Venus", "res": "Luxury"},
        "front_r_4": {"nums": [4], "planet": "Rahu", "res": "Sudden"},
        "front_l_2": {"nums": [2], "planet": "Moon", "res": "Peace"},
        "belly_r_3": {"nums": [3], "planet": "Jupiter", "res": "Knowledge"},
        "center_5": {"nums": [5], "planet": "Mercury", "res": "ATI SHUBH Center BEST"},
        "belly_l_7": {"nums": [7], "planet": "Ketu", "res": "Luck"},
        "back_8": {"nums": [8], "planet": "Saturn", "res": "Hard"},
        "tail_1": {"nums": [1], "planet": "Sun", "res": "Unstable tail"}
    }
    
    def find(n):
        for k, v in kurma.items():
            if n in v["nums"]:
                return k, v
        return "center_5", kurma["center_5"]
        
    m_part, m_data = find(mulank)
    b_part, b_data = find(bhagyank)
    h_part, h_data = find(house_s)
    
    ben_map = {
        1: [1, 3, 5, 9], 2: [1, 2, 3, 5], 3: [1, 2, 3, 6, 9], 
        4: [4, 5, 6, 7], 5: [1, 5, 6], 6: [2, 3, 6, 9], 
        7: [1, 2, 4, 5, 7], 8: [5, 6], 9: [1, 3, 6, 9]
    }
    
    house_ben = house_s in ben_map.get(bhagyank, [5, 6])
    
    return {
        "kurma": kurma,
        "your": {"mulank": mulank, "bhagyank": bhagyank, "house_single": house_s},
        "placements": {
            "mulank": {"part": m_part},
            "bhagyank": {"part": b_part},
            "house": {
                "part": h_part, 
                "benefic": house_ben, 
                "result": f"{'SHUBH' if house_ben else 'ASHUBH'} - House {house}={house_s} in {h_part}"
            }
        },
        "remedies": {
            "house": f"{'No remedy' if house_ben else 'Paint entrance Green, Kurma yantra North'}",
            "best": "Keep 5 in center, 9 in head"
        }
    }
