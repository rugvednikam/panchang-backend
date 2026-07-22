
import swisseph as swe
from datetime import datetime
import math

swe.set_ephe_path('.')

RASHIS = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]
NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

# BPHS Data
EXALTATION = {
    "Surya": ("Mesha", 10), "Chandra": ("Vrishabha", 3), "Mangal": ("Makara", 28),
    "Budh": ("Kanya", 15), "Guru": ("Karka", 5), "Shukra": ("Meena", 27), "Shani": ("Tula", 20),
    "Rahu": ("Vrishabha", 20), "Ketu": ("Vrishchika", 20)
}
DEBILITATION = {
    "Surya": ("Tula", 10), "Chandra": ("Vrishchika", 3), "Mangal": ("Karka", 28),
    "Budh": ("Meena", 15), "Guru": ("Makara", 5), "Shukra": ("Kanya", 27), "Shani": ("Mesha", 20),
    "Rahu": ("Vrishchika", 20), "Ketu": ("Vrishabha", 20)
}
OWN_HOUSE = {
    "Surya": ["Simha"], "Chandra": ["Karka"], "Mangal": ["Mesha","Vrishchika"],
    "Budh": ["Mithuna","Kanya"], "Guru": ["Dhanu","Meena"], "Shukra": ["Vrishabha","Tula"],
    "Shani": ["Makara","Kumbha"], "Rahu": ["Kumbha"], "Ketu": ["Vrishchika"]
}
FRIENDS = {
    "Surya": ["Chandra","Mangal","Guru"], "Chandra": ["Surya","Budh"], "Mangal": ["Surya","Chandra","Guru"],
    "Budh": ["Surya","Shukra"], "Guru": ["Surya","Chandra","Mangal"], "Shukra": ["Budh","Shani"],
    "Shani": ["Budh","Shukra"], "Rahu": ["Shukra","Shani"], "Ketu": ["Mangal","Shukra"]
}
ENEMIES = {
    "Surya": ["Shukra","Shani"], "Chandra": ["Rahu","Ketu"], "Mangal": ["Budh"],
    "Budh": ["Chandra"], "Guru": ["Budh","Shukra"], "Shukra": ["Surya","Chandra"],
    "Shani": ["Surya","Chandra","Mangal"]
}

SHAYANADI_NAMES = [
    "Shayan", "Upaveshan", "Netrapani", "Prakashan", "Gaman", "Agaman",
    "Sabha", "Agama", "Bhojan", "Nrityalipsa", "Kautuk", "Nidra"
]
SHAYANADI_HINDI = [
    "शयन", "उपवेशन", "नेत्रपाणि", "प्रकाशन", "गमन", "आगमन",
    "सभा", "आगम", "भोजन", "नृत्यलिप्सा", "कौतुक", "निद्रा"
]

BALAADI_NAMES = ["Baalya", "Kumara", "Yuva", "Vriddha", "Mrita"]
BALAADI_HINDI = ["बाल्य", "कुमार", "यौवन", "वृद्ध", "मृत"]

DEEPTADI_NAMES = ["Deepta","Swastha","Mudita","Shanta","Shakta","Peedita","Deena","Khala","Vikala","Bheeta"]
DEEPTADI_HINDI = ["दीप्त","स्वस्थ","मुदित","शांत","शक्त","पीड़ित","दीन","खल","विकल","भीत"]

JAGRATADI_NAMES = ["Jagrat", "Swapna", "Sushupti"]
JAGRATADI_HINDI = ["जागृत", "स्वप्न", "सुषुप्ति"]

def get_rashi_from_deg(deg):
    return RASHIS[int(deg/30) % 12], int(deg/30) % 12

def is_combust(planet_deg, sun_deg, planet_name):
    if planet_name == "Surya": return False
    diff = abs(planet_deg - sun_deg) % 360
    if diff > 180: diff = 360 - diff
    # Combust degrees: Mercury 14, Venus 10, Mars 17, Jupiter 11, Saturn 15
    limits = {"Chandra":12, "Mangal":17, "Budh":14, "Guru":11, "Shukra":10, "Shani":15, "Rahu":10, "Ketu":10}
    return diff < limits.get(planet_name, 10)

def get_balaadi_avastha(deg, rashi_index):
    deg_in_rashi = deg % 30
    is_odd = (rashi_index % 2 == 0)  # Mesha is odd
    if is_odd:
        if deg_in_rashi < 6: idx=0
        elif deg_in_rashi < 12: idx=1
        elif deg_in_rashi < 18: idx=2
        elif deg_in_rashi < 24: idx=3
        else: idx=4
    else:
        if deg_in_rashi < 6: idx=4
        elif deg_in_rashi < 12: idx=3
        elif deg_in_rashi < 18: idx=2
        elif deg_in_rashi < 24: idx=1
        else: idx=0
    power = [25, 50, 100, 50, 10][idx]
    return {"en": BALAADI_NAMES[idx], "hi": BALAADI_HINDI[idx], "power": f"{power}%", "degree_in_rashi": round(deg_in_rashi,2), "is_odd_rashi": is_odd}

def get_deeptadi_avastha(planet_name, rashi_name, deg, sun_deg, is_retro):
    # Deepta - Exalted
    ex_rashi, ex_deg = EXALTATION.get(planet_name, (None,None))
    deb_rashi, _ = DEBILITATION.get(planet_name, (None,None))
    own = OWN_HOUSE.get(planet_name, [])
    
    if rashi_name == ex_rashi:
        return {"en":"Deepta","hi":"दीप्त","meaning":"Exalted - 100% Powerful","power":100}
    if rashi_name in own:
        return {"en":"Swastha","hi":"स्वस्थ","meaning":"Own House - Very Strong","power":90}
    if is_combust(deg, sun_deg, planet_name):
        return {"en":"Vikala","hi":"विकल","meaning":"Combust/Asta - Weak","power":10}
    if rashi_name == deb_rashi:
        return {"en":"Deena","hi":"दीन","meaning":"Debilitated - Very Weak","power":5}
    if is_retro:
        return {"en":"Shakta","hi":"शक्त","meaning":"Retrograde Vakri - Powerful","power":80}
    # Check friend/enemy based on rashi lord - simplified
    # For simplicity: if enemy rashi lord
    if rashi_name in ["Mesha","Vrishchika"] and planet_name in ["Budh"]: # example
        return {"en":"Peedita","hi":"पीड़ित","meaning":"Enemy house - Afflicted","power":30}
    # Default mapping based on generic strength
    # We will cycle through Mudita, Shanta, etc.
    # Friend check
    # This is simplified - in real need to check rashi lord friendship
    return {"en":"Mudita","hi":"मुदित","meaning":"Friend's house - Happy","power":70}

def get_jagratadi_avastha(rashi_name, planet_name):
    # Simplified BPHS: Kendra (1,4,7,10 from Lagna) = Jagrat - but we use planet own/neutral
    # Using own/exalt = Jagrat, friend = Swapna, enemy = Sushupti
    ex_rashi, _ = EXALTATION.get(planet_name, (None,None))
    own = OWN_HOUSE.get(planet_name, [])
    if rashi_name == ex_rashi or rashi_name in own:
        return {"en":"Jagrat","hi":"जागृत","meaning":"Awake - Active result"}
    elif rashi_name in DEBILITATION.get(planet_name, [""]):
        return {"en":"Sushupti","hi":"सुषुप्ति","meaning":"Deep Sleep - No result"}
    else:
        return {"en":"Swapna","hi":"स्वप्न","meaning":"Dreaming - Medium result"}

def get_shayanadi_avastha(planet_deg, planet_name):
    # BPHS method: Planet's nakshatra + calculation
    # Nakshatra number 0-26
    nak_num = int(planet_deg / 13.333333)
    nak_deg = planet_deg % 13.333333
    # Factor as per planet (Surya 1, Chandra 2 etc as per BPHS 45.12)
    factors = {"Surya":1,"Chandra":2,"Mangal":3,"Budh":4,"Guru":5,"Shukra":6,"Shani":7,"Rahu":8,"Ketu":9}
    f = factors.get(planet_name, 1)
    # Formula: (nak_num * f + nak_deg) % 12
    avastha_idx = int((nak_num * f + (nak_deg*2)) % 12)
    return {
        "en": SHAYANADI_NAMES[avastha_idx],
        "hi": SHAYANADI_HINDI[avastha_idx],
        "number": avastha_idx+1,
        "nakshatra": NAKSHATRAS[nak_num],
        "description": get_shayanadi_description(SHAYANADI_NAMES[avastha_idx])
    }

def get_shayanadi_description(name):
    desc = {
        "Shayan":"Sleeping - No power, needs daan",
        "Upaveshan":"Sitting - Ready to give result",
        "Netrapani":"Eyes on hand - Searching",
        "Prakashan":"Shining - Full auspicious result",
        "Gaman":"Going - Result will go away",
        "Agaman":"Coming - Result coming soon",
        "Sabha":"In assembly - With help of others",
        "Agama":"Arrival - Near",
        "Bhojan":"Eating - Enjoying",
        "Nrityalipsa":"Desiring to dance - Very happy, best",
        "Kautuk":"Curiosity - Playful, good",
        "Nidra":"Deep sleep - Worst, no result"
    }
    return desc.get(name, "")

def get_full_avastha(dt: datetime, lat: float, lon: float):
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sun_deg = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0] % 360
    
    PLANETS = [(swe.SUN,"Surya"),(swe.MOON,"Chandra"),(swe.MARS,"Mangal"),(swe.MERCURY,"Budh"),(swe.JUPITER,"Guru"),(swe.VENUS,"Shukra"),(swe.SATURN,"Shani"),(swe.TRUE_NODE,"Rahu")]
    
    result = {}
    for pid, pname in PLANETS:
        calc = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)
        deg = calc[0][0] % 360
        is_retro = calc[0][3] < 0  # speed negative
        rashi_name, rashi_idx = get_rashi_from_deg(deg)
        
        balaadi = get_balaadi_avastha(deg, rashi_idx)
        deeptadi = get_deeptadi_avastha(pname, rashi_name, deg, sun_deg, is_retro)
        jagratadi = get_jagratadi_avastha(rashi_name, pname)
        shayanadi = get_shayanadi_avastha(deg, pname)
        
        # Ketu
        if pname == "Rahu":
            ketu_deg = (deg + 180) % 360
            krashi, kidx = get_rashi_from_deg(ketu_deg)
            result["Ketu"] = {
                "degree": round(ketu_deg,2),
                "rashi": krashi,
                "nakshatra": NAKSHATRAS[int(ketu_deg/13.3333)],
                "balaadi": get_balaadi_avastha(ketu_deg, kidx),
                "deeptadi": get_deeptadi_avastha("Ketu", krashi, ketu_deg, sun_deg, False),
                "jagratadi": get_jagratadi_avastha(krashi, "Ketu"),
                "shayanadi": get_shayanadi_avastha(ketu_deg, "Ketu")
            }
        
        result[pname] = {
            "degree": round(deg,2),
            "rashi": rashi_name,
            "rashi_index": rashi_idx+1,
            "nakshatra": NAKSHATRAS[int(deg/13.3333)],
            "is_retrograde": is_retro,
            "is_combust": is_combust(deg, sun_deg, pname),
            "balaadi": balaadi,
            "deeptadi": deeptadi,
            "jagratadi": jagratadi,
            "shayanadi": shayanadi
        }
    
    return result
