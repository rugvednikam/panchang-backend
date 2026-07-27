def get_baby_names_by_nakshatra(nakshatra_number: int, pada: int):
    """
    Returns the starting syllables (Namakaran letters) for a given Nakshatra (1-27) and Pada (1-4).
    """
    if not (1 <= nakshatra_number <= 27) or not (1 <= pada <= 4):
        return {"error": "Invalid Nakshatra or Pada."}
        
    nakshatra_syllables = {
        1: ["Chu", "Che", "Cho", "La"],       # Ashwini
        2: ["Li", "Lu", "Le", "Lo"],         # Bharani
        3: ["A", "I", "U", "E"],             # Krittika
        4: ["O", "Va", "Vi", "Vu"],          # Rohini
        5: ["Ve", "Vo", "Ka", "Ki"],         # Mrigashira
        6: ["Ku", "Gha", "Ng", "Chha"],      # Ardra
        7: ["Ke", "Ko", "Ha", "Hi"],         # Punarvasu
        8: ["Hu", "He", "Ho", "Da"],         # Pushya
        9: ["Di", "Du", "De", "Do"],         # Ashlesha
        10: ["Ma", "Mi", "Mu", "Me"],        # Magha
        11: ["Mo", "Ta", "Ti", "Tu"],        # Purva Phalguni
        12: ["Te", "To", "Pa", "Pi"],        # Uttara Phalguni
        13: ["Pu", "Sha", "Na", "Tha"],      # Hasta
        14: ["Pe", "Po", "Ra", "Ri"],        # Chitra
        15: ["Ru", "Re", "Ro", "Ta"],        # Swati
        16: ["Ti", "Tu", "Te", "To"],        # Vishakha
        17: ["Na", "Ni", "Nu", "Ne"],        # Anuradha
        18: ["No", "Ya", "Yi", "Yu"],        # Jyeshtha
        19: ["Ye", "Yo", "Ba", "Bi"],        # Mula
        20: ["Bu", "Dha", "Bha", "Dha"],     # Purva Ashadha
        21: ["Bhe", "Bho", "Ja", "Ji"],      # Uttara Ashadha
        22: ["Ju", "Je", "Jo", "Gha"],       # Shravana
        23: ["Ga", "Gi", "Gu", "Ge"],        # Dhanishta
        24: ["Go", "Sa", "Si", "Su"],        # Shatabhisha
        25: ["Se", "So", "Da", "Di"],        # Purva Bhadrapada
        26: ["Du", "Tha", "Jha", "Na"],      # Uttara Bhadrapada
        27: ["De", "Do", "Cha", "Chi"]       # Revati
    }
    
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    syllables = nakshatra_syllables.get(nakshatra_number, [])
    if not syllables:
        return {"error": "Syllables not found"}
        
    specific_syllable = syllables[pada - 1]
    
    return {
        "nakshatra_name": nakshatra_names[nakshatra_number - 1],
        "nakshatra_number": nakshatra_number,
        "pada": pada,
        "syllable": specific_syllable,
        "all_pada_syllables": syllables
    }
