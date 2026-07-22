RASHIS = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

def get_house(planet_rashi: str, asc_rashi: str) -> int:
    try:
        p_idx = RASHIS.index(planet_rashi)
        a_idx = RASHIS.index(asc_rashi)
        return ((p_idx - a_idx + 12) % 12) + 1
    except ValueError:
        return 1

def check_mangal_dosha(kundli: dict) -> dict:
    asc_rashi = kundli["ascendant"]["rashi"]
    mars = next((p for p in kundli["planets"] if p["name"] == "Mangal"), None)
    
    if not mars:
        return {"present": False, "description": "Mars data is missing."}
        
    house = get_house(mars["rashi"], asc_rashi)
    
    # Standard Mangal Dosha houses: 1, 2, 4, 7, 8, 12
    if house in [1, 2, 4, 7, 8, 12]:
        return {
            "present": True,
            "description": f"Mangal Dosha is present as Mars is placed in the {house}th house from the Ascendant. This requires careful matchmaking, but its effects can often be neutralized by the partner's chart or specific remedies."
        }
    else:
        return {
            "present": False,
            "description": f"Mars is safely positioned in the {house}th house. No severe Manglik effects are observed from the Ascendant."
        }

def check_kaal_sarp_dosha(kundli: dict) -> dict:
    rahu = next((p for p in kundli["planets"] if p["name"] == "Rahu"), None)
    
    if not rahu:
        return {"present": False, "description": "Rahu data is missing."}
        
    rahu_deg = rahu["degree"]
    
    # Primary planets excluding nodes
    primary_planets = ["Surya", "Chandra", "Mangal", "Budh", "Guru", "Shukra", "Shani"]
    
    all_between_0_180 = True
    all_between_180_360 = True
    
    for pname in primary_planets:
        planet = next((p for p in kundli["planets"] if p["name"] == pname), None)
        if not planet:
            continue
            
        deg_diff = (planet["degree"] - rahu_deg) % 360
        if not (0 <= deg_diff <= 180):
            all_between_0_180 = False
        if not (180 <= deg_diff <= 360):
            all_between_180_360 = False
            
    is_present = all_between_0_180 or all_between_180_360
    
    if is_present:
        return {
            "present": True,
            "description": "Kaal Sarp Dosha is present. All 7 primary planets are hemmed between the Rahu-Ketu axis. This may cause delays and intense spiritual awakening. Proper Vedic remedies and continuous perseverance are highly recommended."
        }
    else:
        return {
            "present": False,
            "description": "Planets are distributed outside the Rahu-Ketu axis. Kaal Sarp Dosha is not present in this chart."
        }

def check_pitra_dosha(kundli: dict) -> dict:
    asc_rashi = kundli["ascendant"]["rashi"]
    sun = next((p for p in kundli["planets"] if p["name"] == "Surya"), None)
    rahu = next((p for p in kundli["planets"] if p["name"] == "Rahu"), None)
    
    if not sun or not rahu:
        return {"present": False, "description": "Planet data is missing."}
        
    # Condition 1: Sun and Rahu conjunct
    sun_rahu_conjunct = (sun["rashi"] == rahu["rashi"])
    
    # Condition 2: Rahu in 9th house
    rahu_house = get_house(rahu["rashi"], asc_rashi)
    rahu_in_9th = (rahu_house == 9)
    
    if sun_rahu_conjunct or rahu_in_9th:
        return {
            "present": True,
            "description": "Pitra Dosha is indicated due to afflictions to the Sun or the 9th house (Bhagya/Dharma Bhava) by Rahu. It is advised to perform ancestral offerings and show deep respect to elders to mitigate these energies."
        }
    else:
        return {
            "present": False,
            "description": "The Sun and the 9th house are free from severe nodal afflictions. Ancestral blessings and general fortune are well supported."
        }

def get_all_doshas(kundli: dict) -> list:
    mangal = check_mangal_dosha(kundli)
    kaal = check_kaal_sarp_dosha(kundli)
    pitra = check_pitra_dosha(kundli)
    
    return [
        {
            "name": "Mangal Dosha (Kuja Dosha)",
            "present": mangal["present"],
            "description": mangal["description"]
        },
        {
            "name": "Kaal Sarp Dosha",
            "present": kaal["present"],
            "description": kaal["description"]
        },
        {
            "name": "Pitra Dosha",
            "present": pitra["present"],
            "description": pitra["description"]
        }
    ]
