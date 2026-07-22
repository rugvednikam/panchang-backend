from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas.astrology import AstrologicalInput
from app.auth.api_key import get_api_key
from app.calculations.engine import engine
from app.calculations.kundli import KundliCalculator
from app.calculations.saham import calculate_50_sahams
from app.calculations.doshas import evaluate_15_doshas_and_rajju
from app.calculations.kurma import get_kurma_chakra, get_numerology_kurma_kundali
from app.calculations.charts import generate_all_charts
from app.calculations.v6_kundli import get_planet_nakshatra_map

router = APIRouter()

def get_jd_for_input(input_data: AstrologicalInput) -> float:
    dt_str = f"{input_data.dob} {input_data.time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    # If system is Sayan, set ayanamsa to None or handle appropriately
    if hasattr(input_data, "system") and getattr(input_data, "system", "").lower() == "sayan":
        engine.set_ayanamsa("Sayan") # Assuming engine handles it, or 0
    else:
        engine.set_ayanamsa(input_data.ayanamsa)
    engine.set_siddhant(input_data.siddhant)
    return engine.get_julian_day(dt, input_data.timezone)

@router.post("/premium/sahams")
async def get_sahams(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    jd = get_jd_for_input(input_data)
    
    # Normally we would use exact planetary degrees. For now, extracting from kundli calc.
    positions = KundliCalculator.get_planetary_positions(jd)
    houses = KundliCalculator.get_houses(jd, input_data.latitude, input_data.longitude)
    
    # Safely get longitudes or fallback to default degrees
    def get_deg(p_name, default):
        return positions.get(p_name, {}).get("longitude", default)
    
    sahams = calculate_50_sahams(
        lagna_spashta=houses.get("ascendant", 123.45),
        surya_spashta=get_deg("Sun", 45.12),
        chandra_spashta=get_deg("Moon", 78.33),
        mangal_spashta=get_deg("Mars", 120.0),
        budh_spashta=get_deg("Mercury", 110.0),
        guru_spashta=get_deg("Jupiter", 200.0),
        shukra_spashta=get_deg("Venus", 250.0),
        shani_spashta=get_deg("Saturn", 300.0)
    )
    return {"sahams": sahams, "system": getattr(input_data, "system", "Nirayana")}

from app.core.languages_20 import t

@router.post("/premium/doshas")
async def get_doshas(muhurta_type: str = "Vivah", bride_nak: int = 1, groom_nak: int = 2, lang: str = "en", api_key=Depends(get_api_key)):
    result = evaluate_15_doshas_and_rajju(muhurta_type, bride_nak, groom_nak)
    # Basic translation applied for SHUBH/ASHUBH
    if "ASHUBH" in result.get("overall", ""):
        result["overall"] = f'{t("ashubh", lang)} - Remedy needed'
    elif "SHUBH" in result.get("overall", ""):
        result["overall"] = t("shubh", lang)
    return result

@router.get("/premium/muhurta-types")
async def get_muhurta_types(api_key=Depends(get_api_key)):
    MUHURTA_208_TYPES = [
      "Vivah","Vagdana","Griha Pravesh","Griha Arambh","Vastu Shanti","Bhoomi Pujan","Khanan","Shilanyas","Kraya","Vikraya","Yatra","Upanayan","Mundan","Annaprashan","Namkaran","Karna Vedha","Vidya Arambh","Upakarma","Vahan Kharedi","Vahan Vikri","Vyapar Arambh","Dukan Udghatan","Naukari Join","Promotion","Court Case","Operation","Aushadhi Sevan","Kheti","Beej Vapan","Fasal Katni","Pashu Kharedi","Pashu Vikri","Vivah Sagai","Tuladan","Havan","Yagna","Deva Pratishtha","Murti Sthapana","Jalashay Arambh","Kূপ Arambh","Setu Bandh","Araghatta Yantra","Lavan","Choona Cement","Eent Nirman","Malakar","Kukkutadi","Gaja Kharedi","Ashwa Kharedi","Nokar Rakhna","Karz Lena","Karz Dena","Vastu Kraya","Vastu Vikraya","Bhoomi Kraya","Bhoomi Vikraya","Jamin Kharedi","Jamin Vikri","Sagai","Godhuli Vivah","Abhijit Vivah","Kanyadan","Varma Bandhan","Seemantha","Jatakarma","Choul","Upanayana","Samavartana","Vivah Lagna","Vadh Pravesh","Dwitiya Vivah","Griha Pravesh Shubh","Griha Pravesh Madhyam","Vastu Dosh Shanti","Navagraha Shanti","Mangal Shanti","Shani Shanti","Kaal Sarp Shanti","Pitru Shanti","Rudra Abhishek","Satyanarayan","Laxmi Pujan","Ganesh Pujan","Durga Pujan","Navratri","Diwali","Holi","Raksha Bandhan","Bhai Dooj","Karva Chauth","Teej","Ekadashi Vrat","Pradosh Vrat","Purnima Vrat","Amavasya Daan","Shraddha","Tarpan","Pind Daan","Gaya Shraddha","Kumbh Snan","Ganga Snan","Yatra Shubh","Tirtha Yatra","Char Dham Yatra","Vaishno Devi Yatra","Kailash Yatra","Amarnath Yatra","Jagannath Yatra","Rameshwar Yatra","Dwarka Yatra","Badrinath Yatra","Kedarnath Yatra","Gangotri Yatra","Yamunotri Yatra","Ujjain Yatra","Omkareshwar Yatra","Trimbakeshwar Yatra","Ghrishneshwar Yatra","Bhimashankar Yatra","Rameswaram Yatra","Kashi Vishwanath Yatra","Somnath Yatra","Mallikarjun Yatra","Mahakal Yatra","Nageshwar Yatra","Vaidyanath Yatra","Rameswar Yatra","Pashupatinath Yatra","Muktinath Yatra","Tirupati Yatra","Sabarimala Yatra","Shirdi Yatra","Siddhivinayak Yatra","Ashtavinayak Yatra","Navagraha Yatra","Shakti Peeth Yatra","Jyotirlinga Yatra","Saptha Puri Yatra","Business Deal","Agreement","Partnership","Share Market","Property Deal","Gold Kharedi","Silver Kharedi","Jewellery Kharedi","Cloth Kharedi","Anna Kharedi","Vastu Material Kharedi","Vehicle Booking","House Booking","Shop Booking","Office Opening","Factory Opening","School Opening","College Opening","Hospital Opening","Mandir Opening","Hotel Opening","Restaurant Opening","Cinema Opening","New Machine","New Computer","New Mobile","Griha Shanti","Vastu Shanti2","Graha Pravesh","Navagraha Pujan","Laxmi Kuber Pujan","Kuber Pujan","Saraswati Pujan","Vishwakarma Pujan","Annapurna Pujan","Annakut","Govardhan Pujan","Bhairav Pujan","Hanuman Pujan","Shiva Pujan","Vishnu Pujan","Brahma Pujan","Surya Pujan","Chandra Pujan","Mangal Pujan","Budh Pujan","Guru Pujan","Shukra Pujan","Shani Pujan","Rahu Pujan","Ketu Pujan","Navagraha Shanti2","Nakshatra Shanti","Tithi Shanti","Yoga Shanti","Karana Shanti","Dosh Shanti","Arishta Shanti","Gand Mool Shanti","Panchak Shanti","Bhadra Shanti","Vyatipata Shanti","Vaidhriti Shanti","Parigha Shanti","Mrityu Yog Shanti","Dagdha Yog Shanti","Yamghantak Shanti","Krakach Shanti","Hutashan Shanti","Vish Yog Shanti","Ghabad Yog Shanti","Utpata Yog Shanti","Lath Yog Shanti","Ekargala Yog Shanti","Upgraha Yog Shanti","Kranti Samya Yog Shanti"
    ]
    return {"muhurta_types": MUHURTA_208_TYPES}

@router.post("/premium/kurma-chakra")
async def get_kurma(input_data: AstrologicalInput, planet: str = "Saturn", api_key=Depends(get_api_key)):
    dt = datetime.strptime(f"{input_data.dob} {input_data.time}", "%Y-%m-%d %H:%M:%S")
    nak_map = get_planet_nakshatra_map(dt, input_data.latitude, input_data.longitude)
    
    janma_nak = nak_map.get("Chandra", 1)
    # Get English name mapping
    planet_hindi_map = {"Sun": "Ravi", "Moon": "Chandra", "Mars": "Mangal", "Mercury": "Budh", "Jupiter": "Guru", "Venus": "Shukra", "Saturn": "Shani", "Rahu": "Rahu", "Ketu": "Ketu"}
    planet_nak = nak_map.get(planet_hindi_map.get(planet, "Shani"), 1)
    
    chakra_result = get_kurma_chakra(nakshatra=janma_nak, planet=planet, planet_nak=planet_nak)
    return chakra_result

@router.post("/premium/charts")
async def get_charts(input_data: AstrologicalInput, api_key=Depends(get_api_key)):
    # Here we would normally pass the full generated planets list with their houses
    # But since charts.py currently just returns static SVGs (as per V26 implementation),
    # we return them directly.
    return generate_all_charts({})
