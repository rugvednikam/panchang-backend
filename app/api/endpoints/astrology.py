from fastapi import APIRouter, Depends, Query
from datetime import datetime, date, timedelta
from fastapi.responses import FileResponse
import os
import calendar
from typing import Optional
from app.schemas.astrology import AstrologicalInput, MatchMakingInput, DateLocationInput
from app.auth.api_key import get_api_key
from app.calculations.engine import engine
from app.calculations.panchang import PanchangCalculator
from app.calculations.kundli import KundliCalculator
from app.calculations.dasha import DashaCalculator
from app.calculations.match_making import MatchMakingCalculator
from app.calculations.festivals import FestivalCalculator
from app.calculations.muhurta import MuhurtaCalculator

from app.calculations.v6_muhurta_rules import check_muhurta, get_all_muhurtas_for_day, MUHURTA_TYPES
from app.calculations.v6_chakras import get_all_chakras
from app.calculations.v6_yogas import detect_yogas
from app.calculations.v6_avastha import get_full_avastha
from app.calculations.v6_lagna_shuddhi import check_lagna_shuddhi, get_shubh_lagna_list_for_date
from app.calculations.v6_pdf_report import create_kundli_pdf
from app.calculations.v6_calculator import get_full_panchang, get_sun_times, TITHIS, NAKSHATRAS, YOGAS, KARANAS, LUNAR_MONTHS
from app.calculations.v6_kundli import get_kundli as v6_get_kundli, get_planet_nakshatra_map
from app.calculations.v6_doshas import get_all_doshas
from app.calculations.v6_predictions import get_all_predictions
from app.calculations.horoscope import get_daily_horoscope

router = APIRouter()

def get_jd_for_input(input_data: AstrologicalInput) -> float:
    dt_str = f"{input_data.dob} {input_data.time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    engine.set_ayanamsa(input_data.ayanamsa)
    engine.set_siddhant(input_data.siddhant)
    return engine.get_julian_day(dt, input_data.timezone)

from app.core.languages_20 import t

@router.post("/panchang")
async def get_panchang(input_data: AstrologicalInput, lang: str = "en", api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    
    dt = datetime.strptime(input_data.dob, "%Y-%m-%d")
    
    tithi = PanchangCalculator.get_tithi(jd)
    nakshatra = PanchangCalculator.get_nakshatra(jd)
    yoga = PanchangCalculator.get_yoga(jd)
    karana = PanchangCalculator.get_karana(jd)
    vara = PanchangCalculator.get_vara(dt)
    
    # Advanced calculation
    advanced_panchang = get_full_panchang(dt.date(), input_data.latitude, input_data.longitude, 12.0, input_data.month_type)
    sun_times = get_sun_times(dt.date(), input_data.latitude, input_data.longitude)
    
    return {
        "tithi": tithi,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "karana": karana,
        "vara": vara,
        "sun_times": sun_times,
        "advanced": advanced_panchang.get("advanced", {})
    }

@router.post("/kundli")
async def get_kundli(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    
    positions = KundliCalculator.get_planetary_positions(jd)
    houses = KundliCalculator.get_houses(jd, input_data.latitude, input_data.longitude)
    
    return {
        "ascendant": houses["ascendant"],
        "ascendant_sign": houses["ascendant_sign"],
        "houses": houses["houses"],
        "planets": positions
    }

@router.post("/dasha")
async def get_dasha(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    positions = KundliCalculator.get_planetary_positions(jd)
    
    dt_str = f"{input_data.dob} {input_data.time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    
    moon_long = positions["Moon"]["longitude"]
    dasha_info = DashaCalculator.get_vimshottari_dasha(moon_long, dt)
    
    return dasha_info

@router.post("/match-making")
async def get_match_making(input_data: MatchMakingInput, api_key=Depends(get_api_key)):
    # Calculate JD for boy
    dt_boy = datetime.strptime(f"{input_data.boy_dob} {input_data.boy_time}", "%Y-%m-%d %H:%M:%S")
    jd_boy = engine.get_julian_day(dt_boy, input_data.boy_timezone)
    pos_boy = KundliCalculator.get_planetary_positions(jd_boy)
    boy_moon = pos_boy["Moon"]["longitude"]
    
    # Calculate JD for girl
    dt_girl = datetime.strptime(f"{input_data.girl_dob} {input_data.girl_time}", "%Y-%m-%d %H:%M:%S")
    jd_girl = engine.get_julian_day(dt_girl, input_data.girl_timezone)
    pos_girl = KundliCalculator.get_planetary_positions(jd_girl)
    girl_moon = pos_girl["Moon"]["longitude"]
    
    return MatchMakingCalculator.calculate_ashtakoota(boy_moon, girl_moon)

@router.post("/festivals")
async def get_festivals(input_data: DateLocationInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(input_data.date, "%Y-%m-%d")
    return FestivalCalculator.get_festivals_for_month(dt.year, dt.month)

@router.post("/muhurta")
async def get_muhurta(event_type: str, input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    return MuhurtaCalculator.evaluate_muhurta(jd, event_type)

@router.post("/all")
async def get_all_in_one(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    
    dt_str = f"{input_data.dob} {input_data.time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    dt_only = datetime.strptime(input_data.dob, "%Y-%m-%d")
    
    # Panchang
    advanced_panchang = get_full_panchang(dt_only.date(), input_data.latitude, input_data.longitude, 12.0, input_data.month_type)
    sun_times = get_sun_times(dt_only.date(), input_data.latitude, input_data.longitude)
    
    panchang_data = {
        "tithi": PanchangCalculator.get_tithi(jd),
        "nakshatra": PanchangCalculator.get_nakshatra(jd),
        "yoga": PanchangCalculator.get_yoga(jd),
        "karana": PanchangCalculator.get_karana(jd),
        "vara": PanchangCalculator.get_vara(dt_only),
        "sun_times": sun_times,
        "advanced": advanced_panchang.get("advanced", {})
    }
    
    # Kundli
    positions = KundliCalculator.get_planetary_positions(jd)
    houses = KundliCalculator.get_houses(jd, input_data.latitude, input_data.longitude)
    kundli_data = {
        "ascendant": houses["ascendant"],
        "ascendant_sign": houses["ascendant_sign"],
        "houses": houses["houses"],
        "planets": positions,
        "ayanamsa": KundliCalculator.get_ayanamsa(jd)
    }
    
    # Dasha
    moon_long = positions["Moon"]["longitude"]
    dasha_data = DashaCalculator.get_vimshottari_dasha(moon_long, dt)
    
    # V6 Premium Extensions
    v6_k = v6_get_kundli(dt, input_data.latitude, input_data.longitude, input_data.outer_planets)
    nak_map = get_planet_nakshatra_map(dt, input_data.latitude, input_data.longitude)
    janma_nak_idx = nak_map["Chandra"]
    
    yogas = detect_yogas(v6_k)
    avasthas = get_full_avastha(dt, input_data.latitude, input_data.longitude)
    chakras = get_all_chakras(janma_nak_idx, nak_map)
    doshas = get_all_doshas(v6_k)
    predictions = get_all_predictions(v6_k, dasha_data)
    
    return {
        "panchang": panchang_data,
        "kundli": kundli_data,
        "dasha": dasha_data,
        "yogas": yogas,
        "avasthas": avasthas,
        "chakras": chakras,
        "doshas": doshas,
        "predictions": predictions
    }

# New Premium Endpoints

@router.post("/premium/chakras")
async def get_premium_chakras(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    nak_map = get_planet_nakshatra_map(dt, input_data.latitude, input_data.longitude)
    janma_nak_idx = nak_map["Chandra"]
    return get_all_chakras(janma_nak_idx, nak_map)

@router.post("/premium/yogas")
async def get_premium_yogas(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    kundli = v6_get_kundli(dt, input_data.latitude, input_data.longitude)
    return detect_yogas(kundli)

@router.post("/premium/avastha")
async def get_premium_avastha(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    return get_full_avastha(dt, input_data.latitude, input_data.longitude)

@router.post("/premium/lagna-shuddhi")
async def get_premium_lagna_shuddhi(input_data: AstrologicalInput, muhurta_type: str = "marriage", api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    kundli = v6_get_kundli(dt, input_data.latitude, input_data.longitude)
    return check_lagna_shuddhi(kundli["ascendant"]["rashi"], kundli["planets"], muhurta_type)

@router.post("/premium/muhurta")
async def get_premium_muhurta(input_data: AstrologicalInput, type: str = "Brahma", api_key=Depends(get_api_key)):
    date_val = datetime.strptime(input_data.dob, "%Y-%m-%d").date()
    p = get_full_panchang(date_val, input_data.latitude, input_data.longitude)
    sun_times = get_sun_times(date_val, input_data.latitude, input_data.longitude)
    return check_muhurta(p, type, sun_times)

@router.post("/premium/muhurta/all")
async def get_premium_muhurta_all(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    date_val = datetime.strptime(input_data.dob, "%Y-%m-%d").date()
    return get_all_muhurtas_for_day(date_val, input_data.latitude, input_data.longitude)

@router.post("/premium/pdf")
async def get_premium_pdf(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    kundli = v6_get_kundli(dt, input_data.latitude, input_data.longitude)
    avastha = get_full_avastha(dt, input_data.latitude, input_data.longitude)
    panchang = get_full_panchang(dt.date(), input_data.latitude, input_data.longitude)
    filename = f"/tmp/kundli_{input_data.dob}_{input_data.time.replace(':','')}.pdf"
    os.makedirs("/tmp", exist_ok=True)
    create_kundli_pdf(filename, input_data.dob, input_data.time, input_data.latitude, input_data.longitude, kundli, avastha, panchang)
    return FileResponse(filename, filename=f"Kundli_{input_data.dob}.pdf", media_type="application/pdf")

@router.post("/premium/doshas")
async def get_premium_doshas(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    kundli = v6_get_kundli(dt, input_data.latitude, input_data.longitude)
    return get_all_doshas(kundli)

@router.post("/premium/predictions")
async def get_premium_predictions(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    kundli = v6_get_kundli(dt, input_data.latitude, input_data.longitude)
    
    jd = engine.get_julian_day(dt, input_data.timezone)
    positions = KundliCalculator.get_planetary_positions(jd)
    moon_long = positions["Moon"]["longitude"]
    dasha_data = DashaCalculator.get_vimshottari_dasha(moon_long, dt)
    
    return get_all_predictions(kundli, dasha_data)


@router.post("/horoscope/daily")
async def get_daily_horoscope_api(input_data: AstrologicalInput, current_date: str = Query(..., description="YYYY-MM-DD"), api_key=Depends(get_api_key)):
    # 1. Calculate Natal Moon Sign
    dt_natal = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    engine.set_ayanamsa(input_data.ayanamsa)
    jd_natal = engine.get_julian_day(dt_natal, input_data.timezone)
    natal_positions = KundliCalculator.get_planetary_positions(jd_natal)
    natal_moon_lon = natal_positions.get("Moon", {}).get("longitude_nirayana", 0.0)
    natal_moon_sign = int(natal_moon_lon / 30) + 1
    
    # 2. Calculate Transit Moon Sign for current_date (at noon)
    dt_transit = datetime.strptime(f"{current_date} 12:00:00", "%Y-%m-%d %H:%M:%S")
    jd_transit = engine.get_julian_day(dt_transit, input_data.timezone)
    transit_positions = KundliCalculator.get_planetary_positions(jd_transit)
    transit_moon_lon = transit_positions.get("Moon", {}).get("longitude_nirayana", 0.0)
    transit_moon_sign = int(transit_moon_lon / 30) + 1
    
    # 3. Get Horoscope Prediction
    result = get_daily_horoscope(natal_moon_sign, transit_moon_sign)
    if "error" in result:
        return {"status": "error", "message": result["error"]}
        
    return {"status": "success", "feature": "Daily Horoscope Gochar", "data": result}

@router.post("/panchang/month")
async def get_panchang_month(input_data: DateLocationInput, month_type: Optional[str] = Query("Amavasyant"), api_key=Depends(get_api_key)):
    """
    Calculate panchang summary for every day of a given month.
    Input date determines the year and month (day is ignored).
    Returns an array of day summaries with Tithi, Nakshatra, Yoga, Karana,
    festivals, and special day flags (Ekadashi, Purnima, Amavasya, etc.)
    """
    dt = datetime.strptime(input_data.date, "%Y-%m-%d")
    year = dt.year
    month = dt.month
    num_days = calendar.monthrange(year, month)[1]

    days = []
    for day_num in range(1, num_days + 1):
        d = date(year, month, day_num)
        try:
            panchang = get_full_panchang(d, input_data.latitude, input_data.longitude, 12.0, month_type)
            sun_times = get_sun_times(d, input_data.latitude, input_data.longitude)

            tithi_num = panchang["tithi"]["number"]
            tithi_name = panchang["tithi"]["name"]
            paksha = panchang["tithi"]["paksha"]
            nak_name = panchang["nakshatra"]["name"]
            nak_num = panchang["nakshatra"]["number"]
            pada = panchang["nakshatra"]["pada"]
            yoga_name = panchang["yoga"]["name"]
            karana_name = panchang["karana"]["name"]
            lunar_month = panchang.get("advanced", {}).get("lunar_month", "")
            vara = panchang.get("vara", d.strftime("%A"))

            # Dynamic festival/special day detection
            special = FestivalCalculator.get_special_days_for_tithi(tithi_num, paksha)
            festivals = FestivalCalculator.get_festivals_for_date(d, tithi_num, paksha)

            # Sankranti check
            sankranti = FestivalCalculator.check_sankranti(d)

            day_data = {
                "date": str(d),
                "day_of_week": d.weekday(),  # 0=Monday, 6=Sunday
                "vara": vara,
                "tithi_number": tithi_num,
                "tithi_name": tithi_name,
                "paksha": paksha,
                "nakshatra_name": nak_name,
                "nakshatra_number": nak_num,
                "pada": pada,
                "yoga_name": yoga_name,
                "karana_name": karana_name,
                "lunar_month": lunar_month,
                "sunrise": sun_times.get("sunrise", "06:00"),
                "sunset": sun_times.get("sunset", "18:00"),
                "is_ekadashi": special["is_ekadashi"],
                "is_purnima": special["is_purnima"],
                "is_amavasya": special["is_amavasya"],
                "is_chaturthi": special["is_chaturthi"],
                "is_pradosh": special["is_pradosh"],
                "is_sankranti": sankranti is not None,
                "sankranti_name": sankranti,
                "festivals": festivals,
                "special_tag": special["special_tag"],
            }
            days.append(day_data)
        except Exception as e:
            # If a single day fails, return minimal data so the calendar isn't broken
            days.append({
                "date": str(d),
                "day_of_week": d.weekday(),
                "vara": d.strftime("%A"),
                "tithi_number": 0,
                "tithi_name": "",
                "paksha": "",
                "nakshatra_name": "",
                "nakshatra_number": 0,
                "pada": 0,
                "yoga_name": "",
                "karana_name": "",
                "lunar_month": "",
                "sunrise": "06:00",
                "sunset": "18:00",
                "is_ekadashi": False,
                "is_purnima": False,
                "is_amavasya": False,
                "is_chaturthi": False,
                "is_pradosh": False,
                "is_sankranti": False,
                "sankranti_name": None,
                "festivals": [],
                "special_tag": None,
                "error": str(e),
            })

    return {
        "year": year,
        "month": month,
        "num_days": num_days,
        "days": days,
    }
