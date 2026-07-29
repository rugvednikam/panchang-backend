from datetime import date
from typing import Dict, Any

# ==========================================
# ADVANCED DAILY MUHURTA CALCULATIONS
# Based on Muhurta Chintamani / Mansagari
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
    '''
    # Basic standard logic: specific tithis have specific vasas.
    # We will expand this with proper formula.
    val = (tithi_num * 2) % 7
    status = "Shubh" if val in [1, 2, 5] else "Ashubh"
    return {"name": f"शिववास ({val})", "status": status, "desc": "रुद्राभिषेक विचार"}

def get_bhadravas(tithi_num: int, karana_num: int) -> Dict[str, str]:
    '''
    Bhadravas (Vishti Karana).
    '''
    return {"name": "स्वर्ग/पाताळ/मृत्यू", "status": "Neutral", "desc": "भद्रा विचार"}

def get_hom_aahuti() -> Dict[str, str]:
    return {"name": "होम आहुती", "status": "Shubh", "desc": "आजची आहुती शुभ आहे"}

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

def get_tara_chakra(birth_nakshatra_num: int, current_nakshatra_num: int) -> Dict[str, Any]:
    '''
    Returns the Tara for a given birth nakshatra against today's nakshatra.
    Formula: ((Current Nak - Birth Nak) % 9) + 1
    1=Janma, 2=Sampat, 3=Vipat, 4=Kshem, 5=Pratyari, 6=Sadhak, 7=Vadh, 8=Mitra, 9=Atimitra
    For daily panchang, we can generate a grid of all 27 nakshatras mapped to the 9 taras based on TODAY's nakshatra.
    '''
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
    
    # We will return the mapping for all 27 nakshatras for today's nakshatra
    # i.e. If you are X nakshatra, today's Tara for you is Y.
    # Today's nakshatra = current_nakshatra_num
    # tara = ((current_nak - birth_nak + 27) % 9)
    mapping = []
    for i in range(1, 28):
        tara_idx = (current_nakshatra_num - i + 27) % 9
        mapping.append({
            "nakshatra_num": i,
            "tara": tara_names[tara_idx]
        })
    return mapping

def get_ghatachakra(rashi_num: int) -> Dict[str, Any]:
    # Placeholder for Ghatachakra (Moon sign based inauspicious times)
    return {"status": "Active", "desc": "घातचक्र तपशील"}

def get_shul_chakras(vaar_num: int, tithi_num: int, nak_num: int) -> Dict[str, Any]:
    disha_shul = {
        1: "पश्चिम (West)", 2: "पूर्व (East)", 3: "उत्तर (North)", 
        4: "उत्तर (North)", 5: "दक्षिण (South)", 6: "पश्चिम (West)", 7: "पूर्व (East)"
    }
    return {
        "disha_shul": disha_shul.get(vaar_num, ""),
        "yatra_shul": "यात्रा शूल माहिती",
        "tithi_shul": "तिथी शूल माहिती",
        "vaar_shul": "वार शूल माहिती",
        "nakshatra_shul": "नक्षत्र शूल माहिती"
    }

def get_yogas_doshas(vaar_num: int, tithi_num: int, nak_num: int) -> Dict[str, Any]:
    return {
        "anandadi_yoga": "आनंदादि योग (Anandadi Yoga)",
        "panchban": "पंचबाण (Panchban)",
        "panchshul": "पंचशूल (Panchshul)",
        "gand_mool": "होय/नाही (Gand Mool)",
        "yaamardh": "यामार्द्ध (Yaamardh)",
        "mahendra_sanjnak": "माहेंद्र संज्ञक (Mahendra Sanjnak)",
        "goraksh_gaman": "गोरक्ष गमन (Goraksh Gaman)"
    }

def get_specific_times(sun_times: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "godhuli": "18:00 - 18:24",
        "kulik": "08:30 - 10:00",
        "kaalvela": "10:00 - 11:30",
        "kantak": "13:30 - 15:00"
    }

def get_advanced_daily_info(tithi_num: int, vaar_num: int, karana_num: int, nak_num: int, rashi_num: int, sun_times: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vasa_aahuti": {
            "agnivas": get_agnivas(tithi_num, vaar_num),
            "shivavas": get_shivavas(tithi_num),
            "bhadravas": get_bhadravas(tithi_num, karana_num),
            "hom_aahuti": get_hom_aahuti()
        },
        "daily_guidelines": {
            "varjit_khadya": get_varjit_khadya(tithi_num),
            "snan_dravya": get_snan_dravya(vaar_num),
            "daan_dravya": get_daan_dravya(vaar_num)
        },
        "tara_chakra": get_tara_chakra(1, nak_num),
        "ghatachakra": get_ghatachakra(rashi_num),
        "shul_chakras": get_shul_chakras(vaar_num, tithi_num, nak_num),
        "yogas_doshas": get_yogas_doshas(vaar_num, tithi_num, nak_num),
        "specific_times": get_specific_times(sun_times)
    }

