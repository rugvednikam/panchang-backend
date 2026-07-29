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
        return {"name": "à¤¸à¥ à¤µà¤°à¥ à¤— (Swarga)", "status": "Ashubh", "desc": "à¤§à¤¨ à¤¹à¤¾à¤¨à¥€ (Wealth loss) - à¤¹à¤µà¤¨ à¤¨à¤¿à¤·à¥‡à¤§"}
    elif val == 2:
        return {"name": "à¤ªà¤¾à¤¤à¤¾à¤³ (Patal)", "status": "Ashubh", "desc": "à¤ªà¥ à¤°à¤¾à¤£ à¤¸à¤‚à¤•à¤Ÿ (Danger) - à¤¹à¤µà¤¨ à¤¨à¤¿à¤·à¥‡à¤§"}
    else:
        return {"name": "à¤ªà¥ƒà¤¥à¥ à¤µà¥€ (Prithvi)", "status": "Shubh", "desc": "à¤¸à¥ à¤– à¤¶à¤¾à¤‚à¤¤à¥€ (Auspicious) - à¤¹à¤µà¤¨ à¤¶à¥ à¤­"}

def get_shivavas(tithi_num: int) -> Dict[str, str]:
    '''
    Shivavas calculation for Rudrabhishek.
    Formula: (Tithi * 2 + 5) % 7
    1=Kailash, 2=Gauri, 3=Nandi, 4=Sabha, 5=Bhojan, 6=Kreeda, 0=Shamshan
    '''
    val = (tithi_num * 2 + 5) % 7
    if val == 1:
        return {"name": "à¤•à¥ˆà¤²à¤¾à¤¸ à¤ªà¤°à¥ à¤µà¤¤", "status": "Shubh", "desc": "à¤…à¤¤à¥ à¤¯à¤‚à¤¤ à¤¶à¥ à¤­ - à¤¸à¥ à¤– à¤¶à¤¾à¤‚à¤¤à¥€"}
    elif val == 2:
        return {"name": "à¤®à¤¾à¤¤à¤¾ à¤—à¥Œà¤°à¥€ à¤¸à¥‹à¤¬à¤¤", "status": "Shubh", "desc": "à¤¶à¥ à¤­ - à¤§à¤¨ à¤¸à¤‚à¤ªà¤¤à¥ à¤¤à¥€"}
    elif val == 3:
        return {"name": "à¤¨à¤‚à¤¦à¥€à¤µà¤° (Vrushabh)", "status": "Shubh", "desc": "à¤¶à¥ à¤­ - à¤•à¤¾à¤°à¥ à¤¯ à¤¸à¤¿à¤¦à¥ à¤§à¥€"}
    elif val == 4:
        return {"name": "à¤¸à¤­à¥‡à¤¤ (Sabha)", "status": "Neutral", "desc": "à¤¸à¤¾à¤®à¤¾à¤¨à¥ à¤¯ - à¤®à¤¾à¤¨à¤¸à¤¿à¤• à¤•à¥ à¤²à¥‡à¤¶"}
    elif val == 5:
        return {"name": "à¤­à¥‹à¤œà¤¨ à¤•à¤°à¤¤ à¤†à¤¹à¥‡à¤¤", "status": "Ashubh", "desc": "à¤…à¤¶à¥ à¤­ - à¤ªà¥€à¤¡à¤¾ / à¤…à¤¡à¤¥à¤³à¥‡"}
    elif val == 6:
        return {"name": "à¤•à¥ à¤°à¥€à¤¡à¤¾ (Playing)", "status": "Ashubh", "desc": "à¤…à¤¶à¥ à¤­ - à¤¦à¥ à¤ƒà¤– / à¤¹à¤¾à¤¨à¥€"}
    else:
        return {"name": "à¤¸à¥ à¤®à¤¶à¤¾à¤¨", "status": "Ashubh", "desc": "à¤…à¤¤à¥ à¤¯à¤‚à¤¤ à¤…à¤¶à¥ à¤­ - à¤®à¥ƒà¤¤à¥ à¤¯à¥‚ à¤¤à¥ à¤²à¥ à¤¯ à¤•à¤·à¥ à¤Ÿ"}

def get_bhadravas(tithi_num: int, karana_num: int) -> Dict[str, str]:
    '''
    Bhadravas (Vishti Karana).
    '''
    if karana_num != 7:  # Vishti Karana is typically 7 in a cycle of 7 movable karanas
        return {"name": "à¤­à¤¦à¥ à¤°à¤¾ à¤¨à¤¾à¤¹à¥€", "status": "Shubh", "desc": "à¤­à¤¦à¥ à¤°à¤¾ à¤¦à¥‹à¤· à¤¨à¤¾à¤¹à¥€"}
        
    return {"name": "à¤®à¥ƒà¤¤à¥ à¤¯à¥‚ à¤²à¥‹à¤• (Mrityu Loka)", "status": "Ashubh", "desc": "à¤¶à¥ à¤­ à¤•à¤¾à¤°à¥ à¤¯à¤¾à¤¸ à¤¨à¤¿à¤·à¥‡à¤§"}

def get_hom_aahuti(sun_lon: float, moon_nak_num: int) -> Dict[str, str]:
    sun_nak_num = int(sun_lon / 13.3333333333) + 1
    # Count distance from Sun to Moon Nakshatra (inclusive)
    distance = (moon_nak_num - sun_nak_num) % 27
    if distance < 0:
        distance += 27
    distance += 1 # 1-based index
    
    val = distance % 9
    
    if val in [1, 2]:
        return {"name": "à¤¸à¥‚à¤°à¥ à¤¯ (Surya)", "status": "Ashubh", "desc": "à¤…à¤¶à¥ à¤­ - à¤§à¤¨à¤¹à¤¾à¤¨à¥€ (Wealth loss)"}
    elif val in [3, 4]:
        return {"name": "à¤¬à¥ à¤§ (Budha)", "status": "Shubh", "desc": "à¤¶à¥ à¤­ - à¤§à¤¨à¤µà¥ƒà¤¦à¥ à¤§à¥€ (Wealth gain)"}
    elif val in [5]:
        return {"name": "à¤¶à¥ à¤•à¥ à¤° (Shukra)", "status": "Shubh", "desc": "à¤¶à¥ à¤­ - à¤¸à¥ à¤– à¤µà¥ƒà¤¦à¥ à¤§à¥€ (Happiness)"}
    elif val in [6, 7]:
        return {"name": "à¤¶à¤¨à¥€ (Shani)", "status": "Ashubh", "desc": "à¤…à¤¶à¥ à¤­ - à¤¦à¥ à¤ƒà¤–/à¤•à¥ à¤²à¥‡à¤¶ (Sorrow)"}
    elif val in [8]:
        return {"name": "à¤°à¤¾à¤¹à¥‚ (Rahu)", "status": "Ashubh", "desc": "à¤…à¤¶à¥ à¤­ - à¤°à¥‹à¤— / à¤•à¤·à¥ à¤Ÿ (Disease)"}
    else: # 0
        return {"name": "à¤—à¥ à¤°à¥‚ (Guru)", "status": "Shubh", "desc": "à¤¶à¥ à¤­ - à¤•à¤¾à¤°à¥ à¤¯ à¤¸à¤¿à¤¦à¥ à¤§à¥€ (Success)"}

def get_varjit_khadya(tithi_num: int) -> str:
    '''Forbidden food based on Tithi'''
    forbidden = {
        1: "à¤•à¥ à¤·à¥ à¤®à¤¾à¤‚à¤¡ (à¤­à¥‹à¤ªà¤³à¤¾)", 2: "à¤¬à¥ƒà¤¹à¤¤à¥€ (à¤µà¤¾à¤‚à¤—à¥‡)", 3: "à¤ªà¤Ÿà¥‹à¤² (à¤ªà¤¡à¤µà¤³)", 4: "à¤®à¥ à¤³à¤¾", 
        5: "à¤¬à¤¿à¤²à¥ à¤µ (à¤¬à¥‡à¤²)", 6: "à¤¨à¤¿à¤‚à¤¬", 7: "à¤¤à¤¾à¤¡ à¤«à¤³", 8: "à¤¨à¤¾à¤°à¤³", 9: "à¤²à¥Œà¤•à¥€ (à¤¦à¥ à¤§à¥€)", 
        10: "à¤•à¤²à¤¿à¤‚à¤—à¤¡", 11: "à¤˜à¥‡à¤µà¤¡à¤¾", 12: "à¤®à¤¸à¥‚à¤°", 13: "à¤µà¤¾à¤‚à¤—à¥‡", 14: "à¤¸à¤°à¥ à¤µ à¤ªà¥ à¤°à¤•à¤¾à¤°à¤šà¥€ à¤ªà¤¾à¤¨à¥‡", 
        15: "à¤®à¤¾à¤‚à¤¸/à¤®à¤¦à¥ à¤¯", 30: "à¤®à¤¾à¤‚à¤¸/à¤®à¤¦à¥ à¤¯"
    }
    return forbidden.get(tithi_num if tithi_num <= 15 else tithi_num - 15, "à¤•à¤¾à¤¹à¥€à¤¹à¥€ à¤¨à¤¾à¤¹à¥€")

def get_snan_dravya(vaar_num: int) -> str:
    # Sunday=1
    dravya = {1: "à¤°à¤•à¥ à¤¤ à¤šà¤‚à¤¦à¤¨", 2: "à¤ªà¤¾à¤‚à¤¢à¤°à¥‡ à¤šà¤‚à¤¦à¤¨", 3: "à¤²à¤¾à¤² à¤«à¥ à¤²à¥‡", 4: "à¤¦à¥ à¤°à¥ à¤µà¤¾/à¤¤à¥‚à¤ª", 5: "à¤¹à¤³à¤¦", 6: "à¤¦à¤¹à¥€", 7: "à¤•à¤¾à¤³à¥‡ à¤¤à¥€à¤³"}
    return dravya.get(vaar_num, "à¤œà¤²")

def get_daan_dravya(vaar_num: int) -> str:
    daan = {1: "à¤—à¤¹à¥‚, à¤—à¥‚à¤³, à¤¤à¤¾à¤‚à¤¬à¥‡", 2: "à¤¤à¤¾à¤‚à¤¦à¥‚à¤³, à¤¦à¥‚à¤§, à¤šà¤¾à¤‚à¤¦à¥€", 3: "à¤®à¤¸à¥‚à¤°, à¤²à¤¾à¤² à¤µà¤¸à¥ à¤¤à¥ à¤°", 4: "à¤®à¥‚à¤—, à¤¹à¤¿à¤°à¤µà¥‡ à¤µà¤¸à¥ à¤¤à¥ à¤°", 5: "à¤šà¤£à¤¾ à¤¡à¤¾à¤³, à¤¹à¤³à¤¦", 6: "à¤¤à¤¾à¤‚à¤¦à¥‚à¤³, à¤¸à¤¾à¤–à¤°, à¤ªà¤¾à¤‚à¤¢à¤°à¥‡ à¤µà¤¸à¥ à¤¤à¥ à¤°", 7: "à¤•à¤¾à¤³à¥‡ à¤¤à¥€à¤³, à¤‰à¤¡à¥€à¤¦, à¤¤à¥‡à¤²"}
    return daan.get(vaar_num, "à¤…à¤¨à¥ à¤¨ à¤¦à¤¾à¤¨")

def get_tara_chakra(birth_nakshatra_num: int, current_nakshatra_num: int) -> list:
    tara_names = [
        {"name": "à¤œà¤¨à¥ à¤®", "type": "Ashubh", "color": "red"},
        {"name": "à¤¸à¤‚à¤ªà¤¤", "type": "Shubh", "color": "green"},
        {"name": "à¤µà¤¿à¤ªà¤¤", "type": "Ashubh", "color": "red"},
        {"name": "à¤•à¥ à¤·à¥‡à¤®", "type": "Shubh", "color": "green"},
        {"name": "à¤ªà¥ à¤°à¤¤à¥ à¤¯à¤°à¥€", "type": "Ashubh", "color": "red"},
        {"name": "à¤¸à¤¾à¤§à¤•", "type": "Shubh", "color": "green"},
        {"name": "à¤µà¤§", "type": "Ashubh", "color": "red"},
        {"name": "à¤®à¤¿à¤¤à¥ à¤°", "type": "Shubh", "color": "green"},
        {"name": "à¤…à¤¤à¤¿à¤®à¤¿à¤¤à¥ à¤°", "type": "Shubh", "color": "green"}
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
    # Placeholder mapping
    months = {1: "à¤šà¥ˆà¤¤à¥ à¤°", 2: "à¤µà¥ˆà¤¶à¤¾à¤–", 3: "à¤œà¥ à¤¯à¥‡à¤·à¥ à¤ "}
    return {"name": "à¤˜à¤¾à¤¤à¤šà¤•à¥ à¤° (Ghatachakra)", "status": "Active", "desc": "à¤®à¤¾à¤¹à¤¿à¤¤à¥€ à¤‰à¤ªà¤²à¤¬à¥ à¤§ à¤¨à¤¾à¤¹à¥€"}

def get_shul_chakras(vaar_num: int, tithi_num: int, nak_num: int) -> Dict[str, Any]:
    disha_shul = {
        1: "à¤ªà¤¶à¥ à¤šà¤¿à¤® (West)", 2: "à¤ªà¥‚à¤°à¥ à¤µ (East)", 3: "à¤‰à¤¤à¥ à¤¤à¤° (North)", 
        4: "à¤‰à¤¤à¥ à¤¤à¤° (North)", 5: "à¤¦à¤•à¥ à¤·à¤¿à¤£ (South)", 6: "à¤ªà¤¶à¥ à¤šà¤¿à¤® (West)", 7: "à¤ªà¥‚à¤°à¥ à¤µ (East)"
    }
    yatra_shul = "à¤¶à¥ à¤­" if vaar_num in [4,5] else "à¤…à¤¶à¥ à¤­"
    
    return {
        "disha_shul": disha_shul.get(vaar_num, "None"),
        "yatra_shul": yatra_shul,
        "tithi_shul": "None",
        "vaar_shul": disha_shul.get(vaar_num, "None"),
        "nakshatra_shul": "None"
    }

def get_yogas_doshas(vaar_num: int, tithi_num: int, nak_num: int, sun_lon: float) -> Dict[str, Any]:
    anandadi = ["à¤†à¤¨à¤‚à¤¦", "à¤•à¤¾à¤²à¤¦à¤‚à¤¡", "à¤§à¥‚à¤®à¥ à¤°", "à¤ªà¥ à¤°à¤œà¤¾à¤ªà¤¤à¥€", "à¤¸à¥Œà¤®à¥ à¤¯", "à¤•à¤¾à¤‚à¤•à¥ à¤·", "à¤§à¥ à¤µà¤œ", "à¤¶à¥ à¤°à¥€à¤µà¤¤à¥ à¤¸", "à¤µà¤œà¥ à¤°", "à¤®à¥ à¤¦à¥ à¤—à¤°", "à¤›à¤¤à¥ à¤°", "à¤®à¤¿à¤¤à¥ à¤°", "à¤®à¤¾à¤¨à¤¸", "à¤ªà¤¦à¥ à¤®", "à¤²à¥ à¤‚à¤¬", "à¤‰à¤¤à¥ à¤ªà¤¾à¤¤", "à¤®à¥ƒà¤¤à¥ à¤¯à¥‚", "à¤•à¤¾à¤£", "à¤¸à¤¿à¤¦à¥ à¤§à¥€", "à¤¶à¥ à¤­", "à¤…à¤®à¥ƒà¤¤", "à¤®à¥ à¤¸à¤³", "à¤—à¤¦", "à¤®à¤¾à¤¤à¤‚à¤—", "à¤°à¤¾à¤•à¥ à¤·à¤¸", "à¤šà¤°, à¤¸à¥ à¤¥à¤¿à¤°", "à¤µà¤°à¥ à¤§à¤®à¤¾à¤¨"]
    idx = (nak_num + vaar_num) % 28
    anandadi_yoga = anandadi[idx % len(anandadi)]

    panchban = "à¤…à¤—à¥ à¤¨à¥€ à¤¬à¤¾à¤£" if (int(sun_lon/13.33) % 2 == 0) else "à¤¬à¤¾à¤£ à¤¦à¥‹à¤· à¤¨à¤¾à¤¹à¥€"
    panchshul = "à¤¶à¥‚à¤² à¤¦à¥‹à¤· à¤¨à¤¾à¤¹à¥€"
    gand_mool = "à¤¹à¥‹à¤¯ (Gand Mool)" if nak_num in [1, 9, 10, 18, 19, 27] else "à¤¨à¤¾à¤¹à¥€ (No)"
    
    return {
        "anandadi_yoga": f"{anandadi_yoga} à¤¯à¥‹à¤—",
        "panchban": panchban,
        "panchshul": panchshul,
        "gand_mool": gand_mool,
        "yaamardh": "2.5 à¤¤à¤¾à¤¸",
        "mahendra_sanjnak": "à¤¶à¥ à¤­ à¤®à¥ à¤¹à¥‚à¤°à¥ à¤¤",
        "goraksh_gaman": "à¤¶à¥ à¤­ à¤®à¥ à¤¹à¥‚à¤°à¥ à¤¤"
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
