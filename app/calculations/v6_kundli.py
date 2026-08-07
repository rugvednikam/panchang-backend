
import swisseph as swe
from datetime import datetime
swe.set_ephe_path('.')
PLANETS = [(swe.SUN, "Surya"), (swe.MOON, "Chandra"), (swe.MARS, "Mangal"), (swe.MERCURY, "Budh"), (swe.JUPITER, "Guru"), (swe.VENUS, "Shukra"), (swe.SATURN, "Shani"), (swe.TRUE_NODE, "Rahu")]
NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
RASHIS = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]
def get_rashi(deg):
    return RASHIS[int(deg/30)]
def get_kundli(dt: datetime, lat: float, lon: float, outer_planets: bool = False):
    from app.calculations.ultimate_engine import get_timezone_offset_free
    offset = get_timezone_offset_free(lat, lon)["offset_hours"]
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 - offset)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planets_data = []
    
    planets_to_calc = list(PLANETS)
    if outer_planets:
        planets_to_calc.extend([(swe.URANUS, "Harshal"), (swe.NEPTUNE, "Varun"), (swe.PLUTO, "Yama")])
        
    for pid, ename in planets_to_calc:
        calc = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)
        deg = calc[0][0] % 360
        if pid == swe.TRUE_NODE:
            ketu_deg = (deg + 180) % 360
            planets_data.append({"name": ename, "degree": round(deg,2), "rashi": get_rashi(deg), "nakshatra": NAKSHATRAS[int(deg/13.3333)]})
            planets_data.append({"name": "Ketu", "degree": round(ketu_deg,2), "rashi": get_rashi(ketu_deg), "nakshatra": NAKSHATRAS[int(ketu_deg/13.3333)]})
        else:
            planets_data.append({"name": ename, "degree": round(deg,2), "rashi": get_rashi(deg), "nakshatra": NAKSHATRAS[int(deg/13.3333)]})
    asc = swe.houses_ex(jd, lat, lon, b'A', swe.FLG_SIDEREAL)[0][0] % 360
    moon_deg = [p for p in planets_data if p["name"]=="Chandra"][0]["degree"]
    return {"ascendant": {"degree": round(asc,2), "rashi": get_rashi(asc)}, "janma_nakshatra": NAKSHATRAS[int(moon_deg/13.3333)], "janma_rashi": get_rashi(moon_deg), "planets": planets_data}

def get_planet_nakshatra_map(dt, lat, lon):
    import swisseph as swe
    swe.set_ephe_path('.')
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    from app.calculations.ultimate_engine import get_timezone_offset_free
    offset = get_timezone_offset_free(lat, lon)["offset_hours"]
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 - offset)
    mapping = {}
    for pid, name in [(swe.SUN,"Ravi"),(swe.MOON,"Chandra"),(swe.MARS,"Mangal"),(swe.MERCURY,"Budh"),(swe.JUPITER,"Guru"),(swe.VENUS,"Shukra"),(swe.SATURN,"Shani"),(swe.TRUE_NODE,"Rahu")]:
        deg = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)[0][0] % 360
        nak_idx = int(deg/13.333333)
        mapping[name] = nak_idx
        if name == "Rahu":
            ketu_deg = (deg + 180) % 360
            mapping["Ketu"] = int(ketu_deg/13.333333)
            mapping["Shani_Margi"] = mapping.get("Shani",0)
            mapping["Shani_Vakri"] = mapping.get("Shani",0)
    # Also add Vakri/Margi Shani same for now
    return mapping
