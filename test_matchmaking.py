from app.calculations.match_making import MatchMakingCalculator
import json

def test():
    # Boy Moon at 45 deg (Taurus - Rohini)
    # Girl Moon at 120 deg (Leo - Magha)
    boy_moon = 45.0
    girl_moon = 120.0
    
    ashta = MatchMakingCalculator.calculate_ashtakoota(boy_moon, girl_moon)
    print("ASHTAKOOTA:")
    print(json.dumps(ashta, indent=2))
    
    # Test manglik
    kundli = {
        "ascendant_sign": 1, # Aries
        "planets": {
            "Mars": {"longitude": 10.0}, # Aries (1st house from ascendant) -> Manglik
            "Moon": {"longitude": 100.0},
            "Venus": {"longitude": 200.0}
        }
    }
    manglik = MatchMakingCalculator.calculate_manglik_dosha(kundli)
    print("\nMANGLIK:")
    print(json.dumps(manglik, indent=2))
    
    # Test papasamya
    kundli_boy = kundli
    kundli_girl = {
        "ascendant_sign": 2, 
        "planets": {
            "Mars": {"longitude": 10.0}, # 12th from asc (Taurus)
            "Sun": {"longitude": 40.0}, # 1st from asc
            "Saturn": {"longitude": 90.0},
            "Rahu": {"longitude": 150.0},
            "Ketu": {"longitude": 330.0},
            "Moon": {"longitude": 10.0},
            "Venus": {"longitude": 10.0}
        }
    }
    papa = MatchMakingCalculator.calculate_papasamya(kundli_boy, kundli_girl)
    print("\nPAPASAMYA:")
    print(json.dumps(papa, indent=2))
    
    # Test 10 porutham
    b_nak = MatchMakingCalculator.get_nakshatra(boy_moon)
    g_nak = MatchMakingCalculator.get_nakshatra(girl_moon)
    porutham = MatchMakingCalculator.calculate_10_porutham(b_nak, g_nak)
    print("\n10 PORUTHAM:")
    print(json.dumps(porutham, indent=2))

if __name__ == "__main__":
    test()
