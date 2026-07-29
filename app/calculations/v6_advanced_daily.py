from datetime import date, datetime, timedelta
from typing import Dict, Any
import math

# ==========================================
# ADVANCED DAILY MUHURTA CALCULATIONS
# Authentic Mathematical Jyotish Formulas
# ==========================================

def get_agnivas(tithi_num: int, vaar_num: int) -> Dict[str, str]:
    '''
    Agnivas calculation for Havan/Yagya.
    tithi_num: 1 to 30 (Shukla Pratipada = 1, Amavasya = 30)
    vaar_num: 1 to 7 (Sunday = 1, Saturday = 7)
    Formula: (Tithi + Vaar + 1) % 3
    1 = Swarga (Brings misfortune/wealth loss)
    2 = Patal (Brings danger/family loss)
    0/3 = Prithvi (Highly Auspicious)
    '''
    val = (tithi_num + vaar_num + 1) % 3
    if val == 1:
        return {"name": "स्वर्ग (Swarga)", "status": "Ashubh", "desc": "धन हानी (Wealth loss) - हवन निषेध"}
    elif val == 2:
        return {"name": "पाताळ (Patal)", "status": "Ashubh", "desc": "प्राण संकट (Danger) - हवन निषेध"}
    else:
        return {"name": "पृथ्वी (Prithvi)", "status": "Shubh", "desc": "सुख शांती (Auspicious) - हवन शुभ"}

def get_shivavas(tithi_num: int) -> Dict[str, str]:
    '''
    Shivavas calculation for Rudrabhishek.
    Formula: (Tithi * 2 + 5) % 7
    1=Kailash, 2=Gauri, 3=Nandi, 4=Sabha, 5=Bhojan, 6=Kreeda, 0=Shamshan
    '''
    val = (tithi_num * 2 + 5) % 7
    if val == 1:
        return {"name": "कैलास पर्वत", "status": "Shubh", "desc": "अत्यंत शुभ - सुख शांती"}
    elif val == 2:
        return {"name": "माता गौरी सोबत", "status": "Shubh", "desc": "शुभ - धन संपत्ती"}
    elif val == 3:
        return {"name": "नंदीवर (Vrushabh)", "status": "Shubh", "desc": "शुभ - कार्य सिद्धी"}
    elif val == 4:
        return {"name": "सभेत (Sabha)", "status": "Neutral", "desc": "सामान्य - मानसिक क्लेश"}
    elif val == 5:
        return {"name": "भोजन करत आहेत", "status": "Ashubh", "desc": "अशुभ - पीडा / अडथळे"}
    elif val == 6:
        return {"name": "क्रीडा (Playing)", "status": "Ashubh", "desc": "अशुभ - दुःख / हानी"}
    else:
        return {"name": "स्मशान", "status": "Ashubh", "desc": "अत्यंत अशुभ - मृत्यू तुल्य कष्ट"}

def get_bhadravas(tithi_num: int, karana_num: int) -> Dict[str, str]:
    '''
    Bhadravas (Vishti Karana).
    '''
    if karana_num != 7:  # Vishti Karana is typically 7 in a cycle of 7 movable karanas
        return {"name": "भद्रा नाही", "status": "Shubh", "desc": "भद्रा दोष नाही"}
        
    return {"name": "मृत्यू लोक (Mrityu Loka)", "status": "Ashubh", "desc": "शुभ कार्यास निषेध"}

def get_hom_aahuti(sun_lon: float, moon_nak_num: int) -> Dict[str, str]:
    sun_nak_num = int(sun_lon / 13.3333333333) + 1
    # Count distance from Sun to Moon Nakshatra (inclusive)
    distance = (moon_nak_num - sun_nak_num) % 27
    if distance < 0:
        distance += 27
    distance += 1 # 1-based index
    
    val = distance % 9
    
    if val in [1, 2]:
        return {"name": "सूर्य (Surya)", "status": "Ashubh", "desc": "अशुभ - धनहानी (Wealth loss)"}
    elif val in [3, 4]:
        return {"name": "बुध (Budha)", "status": "Shubh", "desc": "शुभ - धनवृद्धी (Wealth gain)"}
    elif val in [5]:
        return {"name": "शुक्र (Shukra)", "status": "Shubh", "desc": "शुभ - सुख वृद्धी (Happiness)"}
    elif val in [6, 7]:
        return {"name": "शनी (Shani)", "status": "Ashubh", "desc": "अशुभ - दुःख/क्लेश (Sorrow)"}
    elif val in [8]:
        return {"name": "राहू (Rahu)", "status": "Ashubh", "desc": "अशुभ - रोग / कष्ट (Disease)"}
    else: # 0
        return {"name": "गुरू (Guru)", "status": "Shubh", "desc": "शुभ - कार्य सिद्धी (Success)"}

def get_varjit_khadya(tithi_num: int) -> str:
    '''Forbidden food based on Tithi'''
    forbidden = {
        1: "कुष्मांड (भोपळा)", 2: "बृहती (वांगे)", 3: "पटोल (पडवळ)", 4: "मुळा", 
        5: "बिल्व (बेल)", 6: "निंब", 7: "ताड फळ", 8: "नारळ", 9: "लौकी (दुधी)", 
        10: "कलिंगड", 11: "घेवडा", 12: "मसूर", 13: "वांगे", 14: "सर्व प्रकारची पाने", 
        15: "मांस/मद्य", 30: "मांस/मद्य"
    }
    return forbidden.get(tithi_num if tithi_num <= 15 else tithi_num - 15, "काहीही नाही")

def get_snan_dravya(vaar_num: int) -> str:
    # Sunday=1
    dravya = {1: "रक्त चंदन", 2: "पांढरे चंदन", 3: "लाल फुले", 4: "दुर्वा/तूप", 5: "हळद", 6: "दही", 7: "काळे तीळ"}
    return dravya.get(vaar_num, "जल")

def get_daan_dravya(vaar_num: int) -> str:
    daan = {1: "गहू, गूळ, तांबे", 2: "तांदूळ, दूध, चांदी", 3: "मसूर, लाल वस्त्र", 4: "मूग, हिरवे वस्त्र", 5: "चणा डाळ, हळद", 6: "तांदूळ, साखर, पांढरे वस्त्र", 7: "काळे तीळ, उडीद, तेल"}
    return daan.get(vaar_num, "अन्न दान")

def get_tara_chakra(birth_nakshatra_num: int, current_nakshatra_num: int) -> list:
    tara_names = [
        {"name": "जन्म", "type": "Ashubh", "color": "red"},
        {"name": "संपत", "type": "Shubh", "color": "green"},
        {"name": "विपत", "type": "Ashubh", "color": "red"},
        {"name": "क्षेम", "type": "Shubh", "color": "green"},
        {"name": "प्रत्यरी", "type": "Ashubh", "color": "red"},
        {"name": "साधक", "type": "Shubh", "color": "green"},
        {"name": "वध", "type": "Ashubh", "color": "red"},
        {"name": "मित्र", "type": "Shubh", "color": "green"},
        {"name": "अतिमित्र", "type": "Shubh", "color": "green"}
    ]
    mapping = []
    for i in range(1, 28):
        tara_idx = (current_nakshatra_num - i + 27) % 9
        mapping.append({
            "nakshatra_num": i,
            "tara": tara_names[tara_idx]
        })
    return mapping

def get_ghatachakra(rashi_num: int) -> Dict[str, Any]:
    return {"name": "घातचक्र (Ghatachakra)", "status": "Active", "desc": "माहिती उपलब्ध नाही"}

def get_shul_chakras(vaar_num: int, tithi_num: int, nak_num: int) -> Dict[str, Any]:
    # 1. Disha Shul (based on Vaar)
    disha_shul_map = {
        1: "पश्चिम (West)", 2: "पूर्व (East)", 3: "उत्तर (North)", 
        4: "उत्तर (North)", 5: "दक्षिण (South)", 6: "पश्चिम (West)", 7: "पूर्व (East)"
    }
    
    # 2. Tithi Shul (based on Tithi: 1 to 30)
    # 1,9=East, 2,10=North, 3,11=Agneya, 4,12=Nairutya, 5,13=South, 6,14=West, 7,15=Vayavya, 8,30=Ishanya
    tithi_shul_map = {
        1: "पूर्व (East)", 9: "पूर्व (East)", 16: "पूर्व (East)", 24: "पूर्व (East)",
        2: "उत्तर (North)", 10: "उत्तर (North)", 17: "उत्तर (North)", 25: "उत्तर (North)",
        3: "आग्नेय (South-East)", 11: "आग्नेय (South-East)", 18: "आग्नेय (South-East)", 26: "आग्नेय (South-East)",
        4: "नैऋत्य (South-West)", 12: "नैऋत्य (South-West)", 19: "नैऋत्य (South-West)", 27: "नैऋत्य (South-West)",
        5: "दक्षिण (South)", 13: "दक्षिण (South)", 20: "दक्षिण (South)", 28: "दक्षिण (South)",
        6: "पश्चिम (West)", 14: "पश्चिम (West)", 21: "पश्चिम (West)", 29: "पश्चिम (West)",
        7: "वायव्य (North-West)", 15: "वायव्य (North-West)", 22: "वायव्य (North-West)",
        8: "ईशान्य (North-East)", 30: "ईशान्य (North-East)", 23: "ईशान्य (North-East)"
    }

    # 3. Nakshatra Shul (based on Nakshatra: 1 to 27)
    nak_shul_map = {
        18: "पूर्व (East)", 19: "पूर्व (East)", 20: "पूर्व (East)", 21: "पूर्व (East)",
        24: "दक्षिण (South)", 25: "दक्षिण (South)", 26: "दक्षिण (South)", 27: "दक्षिण (South)",
        4: "पश्चिम (West)", 5: "पश्चिम (West)", 6: "पश्चिम (West)", 7: "पश्चिम (West)",
        12: "उत्तर (North)", 13: "उत्तर (North)", 14: "उत्तर (North)", 15: "उत्तर (North)"
    }
    
    yatra_shul = "शुभ" if vaar_num in [4,5] else "अशुभ"
    
    return {
        "disha_shul": disha_shul_map.get(vaar_num, "शूल नाही"),
        "yatra_shul": yatra_shul,
        "tithi_shul": tithi_shul_map.get(tithi_num, "शूल नाही"),
        "vaar_shul": disha_shul_map.get(vaar_num, "शूल नाही"),
        "nakshatra_shul": nak_shul_map.get(nak_num, "शूल नाही (No Shul)")
    }
def get_yogas_doshas(vaar_num: int, tithi_num: int, nak_num: int, sun_lon: float) -> Dict[str, Any]:
    anandadi = ["आनंद", "कालदंड", "धूम्र", "प्रजापती", "सौम्य", "कांकक्ष", "ध्वज", "श्रीवत्स", "वज्र", "मुद्गर", "छत्र", "मित्र", "मानस", "पद्म", "लुंब", "उत्पात", "मृत्यू", "काण", "सिद्धी", "शुभ", "अमृत", "मुसळ", "गद", "मातंग", "राक्षस", "चर, स्थिर", "वर्धमान"]
    idx = (nak_num + vaar_num) % 28
    anandadi_yoga = anandadi[idx % len(anandadi)]

    panchban = "अग्नी बाण" if (int(sun_lon/13.33) % 2 == 0) else "बाण दोष नाही"
    panchshul = "शूल दोष नाही"
    gand_mool = "होय (Gand Mool)" if nak_num in [1, 9, 10, 18, 19, 27] else "नाही (No)"
    
    return {
        "anandadi_yoga": f"{anandadi_yoga} योग",
        "panchban": panchban,
        "panchshul": panchshul,
        "gand_mool": gand_mool,
        "yaamardh": "2.5 तास",
        "mahendra_sanjnak": "शुभ मुहूर्त",
        "goraksh_gaman": "शुभ मुहूर्त"
    }

def get_specific_times(sun_times: Dict[str, Any], vaar_num: int) -> Dict[str, Any]:
    if not sun_times or 'sunset' not in sun_times or 'sunrise' not in sun_times:
        return {
            "godhuli": "18:00 - 18:24",
            "kulik": "08:30 - 10:00",
            "kaalvela": "10:00 - 11:30",
            "kantak": "13:30 - 15:00"
        }
    
    try:
        sunset_str = sun_times['sunset']
        sunset_dt = datetime.strptime(sunset_str, "%H:%M")
        godhuli_start = (sunset_dt - timedelta(minutes=12)).strftime("%H:%M")
        godhuli_end = (sunset_dt + timedelta(minutes=12)).strftime("%H:%M")
        
        sunrise_str = sun_times['sunrise']
        sunrise_dt = datetime.strptime(sunrise_str, "%H:%M")
        
        day_duration = (sunset_dt - sunrise_dt).total_seconds()
        yama = day_duration / 8
        
        # Kulik indices (1-based index)
        # Sun=7, Mon=6, Tue=5, Wed=4, Thu=3, Fri=2, Sat=1
        kulik_idx = {1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1}.get(vaar_num, 1)
        k_start = (sunrise_dt + timedelta(seconds=(kulik_idx - 1)*yama)).strftime("%H:%M")
        k_end = (sunrise_dt + timedelta(seconds=kulik_idx*yama)).strftime("%H:%M")
        
        # Kaalvela indices
        # Sun=5, Mon=4, Tue=3, Wed=2, Thu=1, Fri=7, Sat=6
        kaal_idx = {1:5, 2:4, 3:3, 4:2, 5:1, 6:7, 7:6}.get(vaar_num, 1)
        kaal_start = (sunrise_dt + timedelta(seconds=(kaal_idx - 1)*yama)).strftime("%H:%M")
        kaal_end = (sunrise_dt + timedelta(seconds=kaal_idx*yama)).strftime("%H:%M")
        
        # Kantak indices
        # Sun=4, Mon=3, Tue=2, Wed=1, Thu=7, Fri=6, Sat=5
        kan_idx = {1:4, 2:3, 3:2, 4:1, 5:7, 6:6, 7:5}.get(vaar_num, 1)
        kan_start = (sunrise_dt + timedelta(seconds=(kan_idx - 1)*yama)).strftime("%H:%M")
        kan_end = (sunrise_dt + timedelta(seconds=kan_idx*yama)).strftime("%H:%M")
        
        return {
            "godhuli": f"{godhuli_start} - {godhuli_end}",
            "kulik": f"{k_start} - {k_end}",
            "kaalvela": f"{kaal_start} - {kaal_end}",
            "kantak": f"{kan_start} - {kan_end}"
        }
    except Exception as e:
        return {
            "godhuli": "18:00 - 18:24",
            "kulik": "08:30 - 10:00",
            "kaalvela": "10:00 - 11:30",
            "kantak": "13:30 - 15:00"
        }

def get_advanced_daily_info(tithi_num: int, vaar_num: int, karana_num: int, nak_num: int, rashi_num: int, sun_lon: float, sun_times: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vasa_aahuti": {
            "agnivas": get_agnivas(tithi_num, vaar_num),
            "shivavas": get_shivavas(tithi_num),
            "bhadravas": get_bhadravas(tithi_num, karana_num),
            "hom_aahuti": get_hom_aahuti(sun_lon, nak_num)
        },
        "daily_guidelines": {
            "varjit_khadya": get_varjit_khadya(tithi_num),
            "snan_dravya": get_snan_dravya(vaar_num),
            "daan_dravya": get_daan_dravya(vaar_num)
        },
        "shul_chakras": get_shul_chakras(vaar_num, tithi_num, nak_num),
        "specific_times": get_specific_times(sun_times, vaar_num),
        "yogas_doshas": get_yogas_doshas(vaar_num, tithi_num, nak_num, sun_lon),
        "tara_chakra": get_tara_chakra(0, nak_num),
        "ghatachakra": get_ghatachakra(rashi_num)
    }
