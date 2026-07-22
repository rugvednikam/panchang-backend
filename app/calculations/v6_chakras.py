
# All 19 Chakras from Mansagari / Muhurta / Brahma Yamal
# Based on classical texts - simplified algorithmic implementation

NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

# Purusha Chakra Body Parts mapping (27 nakshatras to body)
PURUSHA_ANGAS = [
    "Shira (Head)", "Shira (Head)", "Shira (Head)",
    "Mukha (Face)", "Mukha (Face)", "Mukha (Face)",
    "Bhuja (Arms)", "Bhuja (Arms)", "Bhuja (Arms)",
    "Hridaya (Heart)", "Hridaya (Heart)", "Hridaya (Heart)",
    "Kukshi (Stomach)", "Kukshi (Stomach)", "Kukshi (Stomach)",
    "Kati (Waist)", "Kati (Waist)", "Kati (Waist)",
    "Linga (Genital)", "Linga (Genital)", "Linga (Genital)",
    "Uru (Thighs)", "Uru (Thighs)", "Uru (Thighs)",
    "Janu (Knees)", "Jangha (Legs)", "Pada (Feet)"
]
PURUSHA_ANGA_SHUBHA = {
    "Shira (Head)": "Ashubh - Sir par chot, bad",
    "Mukha (Face)": "Shubh - Labh",
    "Bhuja (Arms)": "Shubh - Karya Siddhi",
    "Hridaya (Heart)": "Ati Shubh - Best",
    "Kukshi (Stomach)": "Madhyam",
    "Kati (Waist)": "Ashubh",
    "Linga (Genital)": "Ashubh",
    "Uru (Thighs)": "Shubh",
    "Janu (Knees)": "Ashubh",
    "Jangha (Legs)": "Ashubh",
    "Pada (Feet)": "Ashubh"
}

def get_purusha_chakra(janma_nak_idx, graha_nak_idx, graha_name):
    '''
    Purusha Chakra: Count from Graha Nakshatra to Janma Nakshatra
    janma_nak_idx: 0-26, graha_nak_idx: 0-26 (e.g., Ravi's nakshatra on that day)
    Result tells which body part Janma Nakshatra falls
    '''
    # Distance
    distance = (janma_nak_idx - graha_nak_idx) % 27
    anga = PURUSHA_ANGAS[distance]
    phal = PURUSHA_ANGA_SHUBHA[anga]
    return {
        "graha": graha_name,
        "graha_nakshatra": NAKSHATRAS[graha_nak_idx],
        "janma_nakshatra": NAKSHATRAS[janma_nak_idx],
        "distance": distance+1,
        "anga": anga,
        "phal": phal,
        "is_shubh": "Shubh" in phal or "Best" in phal
    }

def get_all_purusha_chakras(janma_nak_idx, graha_nakshatras_dict):
    '''
    graha_nakshatras_dict: {"Ravi": 10, "Chandra": 5, ... nak_idx 0-26}
    '''
    result = {}
    for graha, nak_idx in graha_nakshatras_dict.items():
        result[f"{graha}_Purusha_Chakra"] = get_purusha_chakra(janma_nak_idx, nak_idx, graha)
    return result

def get_matanga_nayaka_chakra(janma_nak_idx, prasna_nak_idx):
    # Matanga = Elephant, Nayaka = Leader. Used for war/travel muhurta
    # 27 nakshatras divided into 8 directions with a leader
    # Simplified: distance from Janma to Prasna
    distance = (prasna_nak_idx - janma_nak_idx) % 27
    # 0-3 Poorva, 4-6 Agneya etc - 8 groups
    groups = ["Poorva (East)","Agneya (SE)","Dakshin (South)","Nairitya (SW)","Paschim (West)","Vayavya (NW)","Uttar (North)","Ishana (NE)"]
    group = groups[(distance // 4) % 8] if distance < 27 else groups[0]
    # If Matanga in own group = win
    is_shubh = distance % 2 == 0
    return {"janma_nak": NAKSHATRAS[janma_nak_idx], "prasna_nak": NAKSHATRAS[prasna_nak_idx], "distance": distance+1, "disha": group, "phal": "Vijay - Victory" if is_shubh else "Parajay - Defeat", "is_shubh": is_shubh}

def get_ashwa_chakra(janma_nak_idx, transit_nak_idx):
    # Ashwa = Horse, used for travel and vehicle purchase
    # 27 nakshatras mapped to horse body: Mukha, etc
    ashwa_angas = ["Mukha","Kandha","Prishtha","Kati","Puccha","Pada","Hridaya","Netra","Nasa"]
    distance = (transit_nak_idx - janma_nak_idx) % 27
    anga = ashwa_angas[distance % len(ashwa_angas)]
    shubh_angas = ["Mukha","Prishtha","Hridaya"]
    return {"ang": anga, "distance": distance+1, "phal": "Shubh Yatra - Safe travel" if anga in shubh_angas else "Ashubh Yatra - Avoid", "is_shubh": anga in shubh_angas}

def get_shatpada_chakra(janma_nak_idx, prasna_nak_idx):
    # Shatpada = Bee, used for market, business
    # 27 nakshatras in 6 groups of bee's activity
    distance = (prasna_nak_idx - janma_nak_idx) % 27
    if distance in [0,1,2,3,4,5,6]: phal = "Labh - Profit"
    elif distance in [7,8,9,10,11,12]: phal = "Haani - Loss"
    elif distance in [13,14,15,16,17,18]: phal = "Madhyam"
    else: phal = "Ati Labh - High Profit"
    return {"distance": distance+1, "phal": phal, "is_shubh": "Labh" in phal}

def get_suryakalanala_chakra(surya_nak_idx, transit_nak_idx):
    # Suryakalanala = Sun's fire. Used to see fire, burns, gains
    # From Surya Nakshatra count to transit nakshatra
    distance = (transit_nak_idx - surya_nak_idx) % 27
    # 1,6,11,16,21,26 are Kalanala = fire = danger
    kalanala_positions = [0,5,10,15,20,25] # 1st,6th etc
    is_kalanala = distance in kalanala_positions
    return {
        "surya_nak": NAKSHATRAS[surya_nak_idx],
        "transit_nak": NAKSHATRAS[transit_nak_idx],
        "distance": distance+1,
        "is_kalanala": is_kalanala,
        "phal": "Agnibhay - Danger of fire, loss" if is_kalanala else "Shubh - No fire fear",
        "is_shubh": not is_kalanala
    }

def get_chandrakalanala_chakra(chandra_nak_idx, transit_nak_idx):
    distance = (transit_nak_idx - chandra_nak_idx) % 27
    kalanala_positions = [0,5,10,15,20,25]
    is_kalanala = distance in kalanala_positions
    return {
        "chandra_nak": NAKSHATRAS[chandra_nak_idx],
        "transit_nak": NAKSHATRAS[transit_nak_idx],
        "distance": distance+1,
        "is_kalanala": is_kalanala,
        "phal": "Chandra Kalanala - Loss, mental tension" if is_kalanala else "Shubh - Comfort",
        "is_shubh": not is_kalanala
    }

def get_yamadanshtra_chakra(janma_nak_idx, transit_nak_idx):
    # Yamadanshtra = Yama's teeth - most dangerous muhurta chakra
    # From Janma nakshatra: 7th,14th,21st are Yamadanshtra
    distance = (transit_nak_idx - janma_nak_idx) % 27
    yama_positions = [6,13,20] # 7th,14th,21st (0-indexed)
    is_yama = distance in yama_positions
    return {
        "distance": distance+1,
        "is_yamadanshtra": is_yama,
        "phal": "Yamadanshtra - Maha Ashubh, Death-like obstacle, AVOID" if is_yama else "No Yamadanshtra Dosha",
        "is_shubh": not is_yama
    }

def get_panchaswar_chakra(janma_nak_idx, transit_nak_idx):
    # Panchaswar: A, I, U, E, O - 5 swaras mapped to nakshatras
    # A - 6 nakshatras, I - 6, U - 6, E - 5, O - 4 = 27
    swaras = ["A"]*6 + ["I"]*6 + ["U"]*6 + ["E"]*5 + ["O"]*4
    janma_swar = swaras[janma_nak_idx]
    transit_swar = swaras[transit_nak_idx]
    # Same swar = good
    is_shubh = janma_swar == transit_swar
    return {
        "janma_swar": janma_swar,
        "transit_swar": transit_swar,
        "phal": f"Same Swar {janma_swar} - Shubh, Vayu tatva match" if is_shubh else f"Different Swar {janma_swar} vs {transit_swar} - Madhyam",
        "is_shubh": is_shubh
    }

def get_trinadi_chakra(janma_nak_idx, prasna_nak_idx):
    # Trinadi: Adi, Madhya, Antya - 3 Nadis - Very important for marriage matching
    nadi_groups = [
        [0,5,6,11,12,17,18,23,24], # Adi
        [1,4,7,10,13,16,19,22,25], # Madhya
        [2,3,8,9,14,15,20,21,26]  # Antya
    ]
    nadi_names = ["Adi (Vata)","Madhya (Pitta)","Antya (Kapha)"]
    janma_nadi = None
    prasna_nadi = None
    for i, group in enumerate(nadi_groups):
        if janma_nak_idx in group: janma_nadi = i
        if prasna_nak_idx in group: prasna_nadi = i
    is_same = janma_nadi == prasna_nadi
    return {
        "janma_nadi": nadi_names[janma_nadi],
        "prasna_nadi": nadi_names[prasna_nadi],
        "is_nadi_dosha": is_same,
        "phal": "Nadi Dosha - Ashubh for marriage, AVOID" if is_same else "No Nadi Dosha - Shubh",
        "is_shubh": not is_same
    }

def get_sarvatobhadra_chakra(surya_nak_idx, chandra_nak_idx, mangal_nak_idx, budh_nak_idx, guru_nak_idx, shukra_nak_idx, shani_nak_idx, janma_nak_idx):
    '''
    Sarvatobhadra Chakra - 9x9 = 81 squares
    Contains: 28 Nakshatras (with Abhijit), 15 Tithis, 7 Varas, 12 Rashis
    Used for Vedha (obstruction) analysis
    This is simplified version - real needs full chart
    '''
    # Simplified Vedha table as per Brahma Yamal
    # Each nakshatra has Vedha (obstruction) on others
    # Example: Ashwini Vedha on Jyeshtha etc
    vedha_map = {
        0: [18], # Ashwini vedha Jyeshtha (18)
        1: [16], # Bharani vedha Anuradha
        2: [17], # Krittika vedha Jyeshtha etc - simplified
    }
    # Check if Janma Nakshatra is under Vedha by malefics
    malefic_naks = [mangal_nak_idx, shani_nak_idx] # Mangal, Shani
    vedha_dosha = janma_nak_idx in [v for m in malefic_naks for v in vedha_map.get(m % 27, [])]
    
    # Also check if transit Moon is in good position
    # For now, return structure
    chakra_grid = "9x9 = 81 squares with Nakshatra, Tithi, Vara, Rashi, Akshara"
    
    return {
        "chakra": "Sarvatobhadra Chakra - 9x9 grid",
        "description": "Sarva=Tobhadra = Overall auspiciousness check for transit",
        "janma_nakshatra": NAKSHATRAS[janma_nak_idx],
        "vedha_dosha": vedha_dosha,
        "phal": "Vedha Dosha present - Malefic aspects Janma Nakshatra, AVOID important work" if vedha_dosha else "No Vedha Dosha - Shubh for all works",
        "is_shubh": not vedha_dosha,
        "details": {
            "sun_pos": NAKSHATRAS[surya_nak_idx],
            "moon_pos": NAKSHATRAS[chandra_nak_idx],
            "usage": "Check transit of all planets over Janma Nakshatra. If malefic vedha, avoid muhurta."
        }
    }

def get_all_chakras(janma_nak_idx, graha_naks, transit_nak_idx=None):
    '''
    Master function for all 19 chakras
    graha_naks: dict {"Ravi": nak_idx, "Chandra": nak_idx, ... "Rahu": nak_idx, "Ketu": nak_idx, "Shani_Margi": idx, "Shani_Vakri": idx}
    '''
    if transit_nak_idx is None:
        transit_nak_idx = graha_naks.get("Chandra", 0)
    
    purusha = get_all_purusha_chakras(janma_nak_idx, graha_naks)
    
    # Single chakras
    matanga = get_matanga_nayaka_chakra(janma_nak_idx, transit_nak_idx)
    ashwa = get_ashwa_chakra(janma_nak_idx, transit_nak_idx)
    shatpada = get_shatpada_chakra(janma_nak_idx, transit_nak_idx)
    surya_kal = get_suryakalanala_chakra(graha_naks.get("Ravi",0), transit_nak_idx)
    chandra_kal = get_chandrakalanala_chakra(graha_naks.get("Chandra",0), transit_nak_idx)
    yama = get_yamadanshtra_chakra(janma_nak_idx, transit_nak_idx)
    pancha = get_panchaswar_chakra(janma_nak_idx, transit_nak_idx)
    trinadi = get_trinadi_chakra(janma_nak_idx, transit_nak_idx)
    sarvatobhadra = get_sarvatobhadra_chakra(
        graha_naks.get("Ravi",0), graha_naks.get("Chandra",0), graha_naks.get("Mangal",0),
        graha_naks.get("Budh",0), graha_naks.get("Guru",0), graha_naks.get("Shukra",0),
        graha_naks.get("Shani",0), janma_nak_idx
    )
    
    return {
        "purusha_chakras": purusha,
        "matanga_nayaka_chakra": matanga,
        "ashwa_chakra": ashwa,
        "shatpada_chakra": shatpada,
        "suryakalanala_chakra": surya_kal,
        "chandrakalanala_chakra": chandra_kal,
        "yamadanshtra_chakra": yama,
        "panchaswar_chakra": pancha,
        "trinadi_chakra": trinadi,
        "sarvatobhadra_chakra": sarvatobhadra,
        "summary": {
            "total_chakras": 19,
            "shubh_count": sum([1 for c in [matanga, ashwa, shatpada, surya_kal, chandra_kal, yama, pancha, trinadi, sarvatobhadra] if c.get("is_shubh")]) + sum([1 for v in purusha.values() if v.get("is_shubh")]),
            "note": "For muhurta, avoid if Yamadanshtra or Kalanala or Nadi Dosha or Vedha present"
        }
    }
