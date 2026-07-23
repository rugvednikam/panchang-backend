
import swisseph as swe
from datetime import date, datetime, timedelta
import math
swe.set_ephe_path('.')
NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
TITHIS = ["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima","Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Amavasya"]
YOGAS = ["Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shula","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]
KARANAS = ["Bava","Balava","Kaulava","Taitila","Garaja","Vanija","Vishti","Shakuni","Chatushpada","Naga","Kimstughna"]
SAMVATSARAS = [
    "Prabhava", "Vibhava", "Shukla", "Pramodoota", "Prajotpatti", 
    "Angirasa", "Srimukha", "Bhava", "Yuva", "Dhatu", 
    "Eswara", "Bahudhanya", "Pramathi", "Vikrama", "Vrisha", 
    "Chitrabhanu", "Svabhanu", "Tarana", "Parthiva", "Vyaya", 
    "Sarvajit", "Sarvadhari", "Virodhi", "Vikriti", "Khara", 
    "Nandana", "Vijaya", "Jaya", "Manmatha", "Durmukhi", 
    "Hevilambi", "Vilambi", "Vikari", "Sarvari", "Plava", 
    "Shubhakrit", "Shobhakrit", "Krodhi", "Vishvavasu", "Parabhava", 
    "Plavanga", "Kilaka", "Saumya", "Sadharana", "Virodhikrit", 
    "Paridhavi", "Pramadicha", "Ananda", "Rakshasa", "Nala", 
    "Pingala", "Kalayukti", "Siddharthi", "Raudri", "Durmati", 
    "Dundubhi", "Rudhirodgari", "Raktakshi", "Krodhana", "Akshaya"
]
RITUS = ["Vasant", "Grishma", "Varsha", "Sharad", "Hemant", "Shishir"]
LUNAR_MONTHS = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashwin", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"]

DAY_MUHURTAS = [
    "Rudra", "Ahi", "Mitra", "Pitr", "Vasu", "Varaha", "Visvedya", 
    "Vidhi (Abhijit)", "Sutamukhi", "Puruhuta", "Vahini", "Naktanakarā", 
    "Varuna", "Aryaman", "Bhaga"
]
NIGHT_MUHURTAS = [
    "Girisa", "Ajapada", "Ahirbudhnya", "Pusya", "Aswini", "Yama", 
    "Agni", "Vidhata", "Kanda", "Aditi", "Jiva", "Vishnu", 
    "Dyumadgadyuti", "Samudra", "Brahma"
]

def get_sun_times(d: date, lat: float, lon: float):
    try:
        jd = swe.julday(d.year, d.month, d.day, 0)
        res_rise = swe.rise_trans(jd, swe.SUN, "", swe.FLG_SWIEPH, swe.CALC_RISE, (lon, lat, 0), 0, 0, 1013.25)
        res_set = swe.rise_trans(jd, swe.SUN, "", swe.FLG_SWIEPH, swe.CALC_SET, (lon, lat, 0), 0, 0, 1013.25)
        rise_jd = res_rise[1][0]
        set_jd = res_set[1][0]
        def jd_to_ist_str(jd_val):
            y,m,day, hour = swe.revjul(jd_val)
            total_min = int((hour % 1)*60)
            h = int(hour)
            dt_ut = datetime(y,m,day,h,total_min)
            dt_ist = dt_ut + timedelta(hours=5, minutes=30)
            return dt_ist.strftime("%H:%M")
        return {"sunrise": jd_to_ist_str(rise_jd), "sunset": jd_to_ist_str(set_jd), "sunrise_jd": rise_jd, "sunset_jd": set_jd}
    except:
        return {"sunrise": "06:00", "sunset": "18:30", "sunrise_jd": 0, "sunset_jd": 0}

def time_to_minutes(t_str):
    try:
        h,m = map(int, t_str.split(":"))
        return h*60 + m
    except:
        return 0
def minutes_to_time(mins):
    mins = int(mins) % (24*60)
    h = mins // 60
    m = mins % 60
    return f"{h:02d}:{m:02d}"

def get_ghati_pala_vipala(target_mins: int, sunrise_mins: int) -> str:
    """
    Calculates Ghatika, Pala, Vipala from Sunrise.
    24 hours = 60 Ghatis, 1 Ghati = 24 mins = 60 Palas.
    """
    diff_mins = target_mins - sunrise_mins
    if diff_mins < 0:
        diff_mins += 24 * 60
        
    total_ghatis = diff_mins / 24.0
    ghati = int(total_ghatis)
    
    total_palas = (total_ghatis - ghati) * 60
    pala = int(total_palas)
    
    total_vipalas = (total_palas - pala) * 60
    vipala = int(round(total_vipalas))
    
    # Handle rounding edge cases
    if vipala == 60:
        vipala = 0
        pala += 1
    if pala == 60:
        pala = 0
        ghati += 1
        
    return f"{ghati:02d}:{pala:02d}:{vipala:02d}"

def get_full_panchang(d: date, lat: float, lon: float, hour=12.0, month_type: str = "Amavasyant"):
    jd = swe.julday(d.year, d.month, d.day, hour)
    sun = swe.calc_ut(jd, swe.SUN)[0][0]
    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    diff = (moon - sun) % 360
    tithi_num = int(diff / 12) + 1
    tithi_name = TITHIS[tithi_num - 1]
    nak_num = int(moon / 13.3333333333) + 1
    nak_name = NAKSHATRAS[nak_num - 1]
    yoga_num = int((sun + moon) % 360 / 13.333333) + 1
    yoga_name = YOGAS[yoga_num - 1]
    karana_num = int(diff / 6) % 11 + 1
    karana_name = KARANAS[karana_num-1] if karana_num <= len(KARANAS) else f"Karana {karana_num}"
    vara = d.strftime("%A")
    is_bhadra = (karana_name == "Vishti")
    
    # Advanced Panchang Elements
    # 1. Years and Samvatsar
    chaitra_passed = (d.month > 3) or (d.month == 3 and d.day >= 22)
    kali_yuga_year = d.year + 3101 if chaitra_passed else d.year + 3100
    vikram_samvat = d.year + 57 if chaitra_passed else d.year + 56
    shaka_samvat = d.year - 78 if chaitra_passed else d.year - 79
    
    samvatsar_index = (kali_yuga_year + 12) % 60
    samvatsara_name = SAMVATSARAS[samvatsar_index]
    
    # 2. Ayana, Ritu, Masa
    ayana = "Uttarayana" if (sun >= 270 or sun < 90) else "Dakshinayana"
    ritu_index = int((sun % 360) / 60)
    ritu = RITUS[ritu_index]
    
    # Simple lunar month calculation based on Sun and Moon diff
    lunar_month_idx = int(sun / 30)
    if diff > 348: # Amanta system - nearing amavasya
        lunar_month_idx = (lunar_month_idx + 1) % 12
        
    if month_type == "Purnimant" and diff > 180: # Krishna Paksha
        lunar_month_idx = (lunar_month_idx + 1) % 12
        
    lunar_month = LUNAR_MONTHS[lunar_month_idx]
    
    rahu_map = {"Sunday": "16:30-18:00", "Monday": "07:30-09:00", "Tuesday": "15:00-16:30", "Wednesday": "12:00-13:30", "Thursday": "13:30-15:00", "Friday": "10:30-12:00", "Saturday": "09:00-10:30"}
    yamaganda_map = {"Sunday": "12:00-13:30", "Monday": "10:30-12:00", "Tuesday": "09:00-10:30", "Wednesday": "07:30-09:00", "Thursday": "06:00-07:30", "Friday": "15:00-16:30", "Saturday": "13:30-15:00"}
    gulika_map = {"Sunday": "15:00-16:30", "Monday": "13:30-15:00", "Tuesday": "12:00-13:30", "Wednesday": "10:30-12:00", "Thursday": "09:00-10:30", "Friday": "07:30-09:00", "Saturday": "06:00-07:30"}
    
    # Advanced UI Requirements
    agnivas = "Earth (Auspicious)" if tithi_num in [1, 4, 7, 10, 13] else ("Sky" if tithi_num in [2, 5, 8, 11, 14] else "Pataal")
    shivavas = "Kailash (Auspicious)" if tithi_num in [2, 9, 14] else "Nandi (Auspicious)"
    bhadravas = "Earth" if is_bhadra and moon >= 270 else ("Pataal" if is_bhadra and moon < 180 else "Swarga") if is_bhadra else "None"
    festivals = ["Sankashti Chaturthi"] if tithi_num == 19 else (["Ekadashi"] if tithi_num in [11, 26] else [])
    result = {
        "date": str(d),
        "vara": vara,
        "tithi": {"number": tithi_num, "name": tithi_name, "paksha": "Shukla" if tithi_num <=15 else "Krishna"},
        "nakshatra": {"number": nak_num, "name": nak_name, "pada": int((moon % 13.333333) / 3.333333)+1},
        "yoga": {"number": yoga_num, "name": yoga_name},
        "karana": {"number": karana_num, "name": karana_name},
        "vara": vara,
        "is_bhadra": is_bhadra,
        "advanced": {
            "kali_yuga_year": kali_yuga_year,
            "vikram_samvat": vikram_samvat,
            "shaka_samvat": shaka_samvat,
            "samvatsara": samvatsara_name,
            "ayana": ayana,
            "ritu": ritu,
            "lunar_month": lunar_month,
            "agnivas": agnivas,
            "shivavas": shivavas,
            "bhadravas": bhadravas,
            "festivals": festivals,
        }
    }
    
    # JD to Ghati Pala Vipala
    def jd_to_ghati(target_jd, sr_jd):
        diff = target_jd - sr_jd
        if diff < 0: diff += 1
        ghatis = diff * 60.0
        g = int(ghatis)
        palas = (ghatis - g) * 60.0
        p = int(palas)
        vipalas = (palas - p) * 60.0
        v = int(round(vipalas))
        if v == 60:
            v = 0
            p += 1
        if p == 60:
            p = 0
            g += 1
        return f"{g:02d}:{p:02d}:{v:02d}"
        
    def jd_to_hms(jd_val):
        y,m,day, hour = swe.revjul(jd_val)
        total_sec = int(round(hour * 3600))
        dt_ut = datetime(y,m,day) + timedelta(seconds=total_sec)
        dt_ist = dt_ut + timedelta(hours=5, minutes=30)
        return dt_ist.strftime("%H:%M:%S")

    # 15 Muhurtas Calculation
    sun_times_today = get_sun_times(d, lat, lon)
    sun_times_tmrw = get_sun_times(d + timedelta(days=1), lat, lon)
    sr_jd = sun_times_today["sunrise_jd"]
    ss_jd = sun_times_today["sunset_jd"]
    tmrw_sr_jd = sun_times_tmrw["sunrise_jd"]
    
    day_muhurtas_list = []
    night_muhurtas_list = []
    
    if sr_jd > 0 and ss_jd > sr_jd:
        muhurta_len = (ss_jd - sr_jd) / 15.0
        for i in range(15):
            s_jd = sr_jd + (i * muhurta_len)
            e_jd = s_jd + muhurta_len
            day_muhurtas_list.append({
                "name": DAY_MUHURTAS[i],
                "start": jd_to_hms(s_jd),
                "end": jd_to_hms(e_jd),
                "start_ghati": jd_to_ghati(s_jd, sr_jd),
                "end_ghati": jd_to_ghati(e_jd, sr_jd)
            })
            
    if ss_jd > 0 and tmrw_sr_jd > ss_jd:
        muhurta_len = (tmrw_sr_jd - ss_jd) / 15.0
        for i in range(15):
            s_jd = ss_jd + (i * muhurta_len)
            e_jd = s_jd + muhurta_len
            night_muhurtas_list.append({
                "name": NIGHT_MUHURTAS[i],
                "start": jd_to_hms(s_jd),
                "end": jd_to_hms(e_jd),
                "start_ghati": jd_to_ghati(s_jd, sr_jd), # Ghati always from today's sunrise
                "end_ghati": jd_to_ghati(e_jd, sr_jd)
            })
            
    result["advanced"]["day_muhurtas"] = day_muhurtas_list
    result["advanced"]["night_muhurtas"] = night_muhurtas_list
    
    result.update({
        "rahu_kaal": rahu_map.get(vara),
        "yamaganda": yamaganda_map.get(vara),
        "gulika_kaal": gulika_map.get(vara),
        "sun_deg": round(sun,2),
        "moon_deg": round(moon,2)
    })
    return result

def get_abhijit_muhurta(d: date, lat: float, lon: float):
    times = get_sun_times(d, lat, lon)
    sr = time_to_minutes(times["sunrise"])
    ss = time_to_minutes(times["sunset"])
    day_len = ss - sr if ss > sr else 12*60
    mid = sr + day_len/2
    return {"start": minutes_to_time(mid - 24), "end": minutes_to_time(mid + 24), "duration": "48 minutes"}

def get_brahma_muhurta(d: date, lat: float, lon: float):
    times = get_sun_times(d, lat, lon)
    sr = time_to_minutes(times["sunrise"])
    return {"start": minutes_to_time(sr - 96), "end": minutes_to_time(sr - 48)}

def get_choghadiya(d: date, lat: float, lon: float):
    times = get_sun_times(d, lat, lon)
    sr = time_to_minutes(times["sunrise"])
    ss = time_to_minutes(times["sunset"])
    vara = d.strftime("%A")
    day_lords = {
        "Sunday": ["Udveg","Chal","Labh","Amrit","Kaal","Shubh","Rog","Udveg"],
        "Monday": ["Amrit","Kaal","Shubh","Rog","Udveg","Chal","Labh","Amrit"],
        "Tuesday": ["Rog","Udveg","Chal","Labh","Amrit","Kaal","Shubh","Rog"],
        "Wednesday": ["Labh","Amrit","Kaal","Shubh","Rog","Udveg","Chal","Labh"],
        "Thursday": ["Shubh","Rog","Udveg","Chal","Labh","Amrit","Kaal","Shubh"],
        "Friday": ["Chal","Labh","Amrit","Kaal","Shubh","Rog","Udveg","Chal"],
        "Saturday": ["Kaal","Shubh","Rog","Udveg","Chal","Labh","Amrit","Kaal"]
    }
    day_duration = ss - sr if ss > sr else 720
    slot = day_duration / 8
    chogh = []
    good = ["Amrit","Shubh","Labh","Chal"]
    for i in range(8):
        start = sr + i*slot
        end = start + slot
        lord = day_lords.get(vara, ["Shubh"]*8)[i]
        chogh.append({"time": f"{minutes_to_time(start)}-{minutes_to_time(end)}", "choghadiya": lord, "is_shubh": lord in good})
    return chogh
