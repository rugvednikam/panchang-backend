
from app.calculations.v6_calculator import get_full_panchang, get_sun_times, get_choghadiya, get_abhijit_muhurta, get_brahma_muhurta

MUHURTA_TYPES = {
    # Balyavastha 7
    "garbhadhana": "Garbhadhana - Conception",
    "pumsavana": "Pumsavana - 3rd Month Pregnancy",
    "seemant": "Seemantonnayan - Baby Shower",
    "jatkarma": "Jatkarma - Birth Ritual",
    "namkaran": "Namkaran - Naming Ceremony",
    "nishkramana": "Nishkramana - First Outing",
    "annaprashan": "Annaprashan - First Food",
    # Childhood 4
    "karnavedha": "Karnavedha - Ear Piercing",
    "mundan": "Mundan / Chudakarana - First Haircut",
    "vidyarambha": "Vidyarambha - Education Start",
    "upnayan": "Upanayan / Vratabandha - Thread Ceremony",
    # Griha 6
    "bhumi_pujan": "Bhumi Pujan - Land Worship",
    "shilanyas": "Shilanyas - Foundation Laying",
    "griha_arambha": "Griha Arambha - Construction Start",
    "griha_pravesh": "Griha Pravesh - House Warming",
    "vastu_shanti": "Vastu Shanti",
    "property_purchase": "Property / Land Purchase",
    # Vivaha 5
    "engagement": "Sagai / Engagement",
    "marriage": "Vivah - Marriage",
    "vadhu_pravesh": "Vadhu Pravesh - Bride Entry",
    "dwitiya_vivah": "Dwitiya Vivah - Second Marriage",
    "godhuli_lagna": "Godhuli Lagna - Emergency Marriage",
    # Business 6
    "business": "Vyapar Arambha - Business Start",
    "shop_opening": "Dukan / Shop Opening",
    "vehicle": "Vahan - Vehicle Purchase",
    "gold_purchase": "Gold / Jewellery Purchase",
    "account_opening": "Account / Ledger Opening - Chopda Pujan",
    "krishi": "Krishi / Kheti - Sowing Crops",
    # Yatra & Others 8
    "yatra": "Yatra - Travel",
    "teertha_yatra": "Teertha Yatra - Pilgrimage",
    "court_case": "Court Case / Mukadma",
    "job_joining": "Job Joining / Naukri",
    "surgery": "Surgery / Operation",
    "medicine_start": "Aushadha Sevan - Medicine Start",
    "weapon_purchase": "Shastra Grahan - Weapon Purchase",
    "rajyabhishek": "Rajyabhishek / Oath Taking"
}

# Rules based on Muhurta Parijata + Chintamani + Mansagari
RULES = {
    # Balyavastha
    "garbhadhana": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"], "avoid_tithis": [4,8,9,14,15,30]},
    "pumsavana": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Shravana"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "seemant": {"good_tithis": [2,3,5,7,10,11], "good_nakshatra": ["Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday"]},
    "jatkarma": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "namkaran": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Uttara Phalguni","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "nishkramana": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "annaprashan": {"good_tithis": [2,3,5,7,10,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Uttara Phalguni","Hasta","Swati","Anuradha","Shravana","Dhanishta","Shatabhisha"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    # Childhood
    "karnavedha": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Mrigashira","Punarvasu","Pushya","Hasta","Chitra","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "mundan": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Mrigashira","Punarvasu","Pushya","Hasta","Chitra","Swati","Anuradha","Shravana","Dhanishta","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "vidyarambha": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Hasta","Chitra","Swati","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "upnayan": {"good_tithis": [2,3,5,10,11,12,13], "good_nakshatra": ["Punarvasu","Pushya","Magha","Uttara Phalguni","Hasta","Chitra","Swati","Anuradha","Shravana","Dhanishta"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    # Griha
    "bhumi_pujan": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Punarvasu","Uttara Phalguni","Hasta","Anuradha","Uttara Ashadha","Revati"], "good_vara": ["Wednesday","Thursday","Friday"]},
    "shilanyas": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Chitra","Swati","Anuradha","Uttara Ashadha","Dhanishta"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "griha_arambha": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Punarvasu","Uttara Phalguni","Hasta","Chitra","Swati","Anuradha","Uttara Ashadha","Dhanishta","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "griha_pravesh": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Chitra","Anuradha","Dhanishta","Revati"], "good_vara": ["Wednesday","Thursday","Friday","Saturday"], "avoid_nakshatra": ["Ardra","Ashlesha","Jyeshtha","Mula"]},
    "vastu_shanti": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Dhanishta","Revati"], "good_vara": ["Wednesday","Thursday","Friday"]},
    "property_purchase": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Uttara Ashadha","Uttara Bhadrapada","Revati"], "good_vara": ["Thursday","Friday"]},
    # Vivaha
    "engagement": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Mula","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "marriage": {"good_tithis": [2,3,5,7,10,11,13], "avoid_tithis": [4,8,9,14,15,30], "avoid_nakshatra": ["Ardra","Ashlesha","Jyeshtha","Mula","Vishakha"], "good_nakshatra": ["Rohini","Mrigashira","Magha","Uttara Phalguni","Hasta","Swati","Anuradha","Mula","Uttara Ashadha","Uttara Bhadrapada","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "vadhu_pravesh": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Uttara Ashadha","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "dwitiya_vivah": {"good_tithis": [2,3,5,7,10,11], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Revati"], "good_vara": ["Monday","Thursday","Friday"]},
    "godhuli_lagna": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Uttara Phalguni","Hasta","Anuradha","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"], "note": "Emergency - Sunset time, no Bhadra check needed"},
    # Business
    "business": {"good_tithis": [2,3,5,7,11,13], "good_nakshatra": ["Ashwini","Punarvasu","Pushya","Hasta","Chitra","Swati","Anuradha","Dhanishta","Revati"], "good_vara": ["Wednesday","Thursday","Friday"]},
    "shop_opening": {"good_tithis": [2,3,5,7,11,13], "good_nakshatra": ["Ashwini","Rohini","Punarvasu","Pushya","Uttara Phalguni","Hasta","Chitra","Swati","Anuradha","Dhanishta","Revati"], "good_vara": ["Wednesday","Thursday","Friday"]},
    "vehicle": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Mrigashira","Punarvasu","Pushya","Hasta","Chitra","Swati","Anuradha","Revati"], "good_vara": ["Wednesday","Friday"]},
    "gold_purchase": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Pushya","Uttara Phalguni","Hasta","Anuradha","Shravana","Dhanishta","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "account_opening": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Punarvasu","Pushya","Uttara Phalguni","Hasta","Chitra","Swati","Anuradha","Dhanishta","Revati"], "good_vara": ["Wednesday","Thursday","Friday"]},
    "krishi": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Rohini","Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Uttara Ashadha","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    # Yatra & Others
    "yatra": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Mrigashira","Punarvasu","Pushya","Hasta","Anuradha","Shravana","Dhanishta","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "teertha_yatra": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Punarvasu","Pushya","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "court_case": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Bharani","Ardra","Ashlesha","Magha","Vishakha","Jyeshtha","Mula"], "good_vara": ["Tuesday","Wednesday"]},
    "job_joining": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Uttara Phalguni","Hasta","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "surgery": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Uttara Phalguni","Hasta","Anuradha","Shravana"], "good_vara": ["Monday","Wednesday","Thursday","Saturday"]},
    "medicine_start": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Mrigashira","Punarvasu","Pushya","Hasta","Swati","Anuradha","Shravana","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]},
    "weapon_purchase": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ardra","Punarvasu","Pushya","Ashlesha","Magha","Uttara Phalguni","Hasta","Chitra","Anuradha","Jyeshtha"], "good_vara": ["Tuesday","Wednesday"]},
    "rajyabhishek": {"good_tithis": [2,3,5,7,10,11,13], "good_nakshatra": ["Ashwini","Rohini","Punarvasu","Pushya","Uttara Phalguni","Hasta","Chitra","Anuradha","Dhanishta","Revati"], "good_vara": ["Monday","Wednesday","Thursday","Friday"]}
}

def check_muhurta(panchang, type, sun_times=None):
    rule = RULES.get(type, RULES["business"])
    score = 0
    max_score = 4
    reasons=[]; warnings=[]
    t_num = panchang["tithi"]["number"]
    if t_num in rule.get("good_tithis", []):
        score+=1; reasons.append(f"Tithi {panchang['tithi']['name']} Shubh for {type}")
    elif t_num in rule.get("avoid_tithis", []):
        warnings.append(f"Tithi {panchang['tithi']['name']} Ashubh - avoid in {type}")
    nak_name = panchang["nakshatra"]["name"]
    if nak_name in rule.get("good_nakshatra", []):
        score+=1; reasons.append(f"Nakshatra {nak_name} Shubh")
    if nak_name in rule.get("avoid_nakshatra", []):
        warnings.append(f"Nakshatra {nak_name} Varjit for {type}")
    if panchang["vara"] in rule.get("good_vara", []):
        score+=1; reasons.append(f"Vara {panchang['vara']} Shubh")
    if not panchang["bhadra"]["is_bhadra"]:
        score+=1; reasons.append("No Bhadra - Shuddha")
    else:
        if type != "godhuli_lagna":  # Godhuli can ignore Bhadra in emergency
            warnings.append("Bhadra present - postpone")
    is_auspicious = score >= 3 and len(warnings)==0
    return {"is_auspicious": is_auspicious, "score": f"{score}/{max_score}", "shubh_muhurta": "Abhijit + Labh/Amrit Choghadiya" if is_auspicious else "Avoid today", "reasons": reasons, "warnings": warnings, "type_info": MUHURTA_TYPES.get(type)}

def get_all_muhurtas_for_day(d, lat, lon):
    p = get_full_panchang(d, lat, lon, 12.0)
    sun = get_sun_times(d, lat, lon)
    chog = get_choghadiya(d, lat, lon)
    abhijit = get_abhijit_muhurta(d, lat, lon)
    brahma = get_brahma_muhurta(d, lat, lon)
    results = {}
    for m_type in MUHURTA_TYPES:
        results[m_type] = check_muhurta(p, m_type, sun)
    return {"date": str(d), "panchang": p, "sun_times": sun, "abhijit": abhijit, "brahma": brahma, "choghadiya": chog, "analysis": results, "summary": {"total_muhurtas": len(MUHURTA_TYPES), "auspicious_for": [k for k,v in results.items() if v["is_auspicious"]], "avoid_for": [k for k,v in results.items() if not v["is_auspicious"]]}}
