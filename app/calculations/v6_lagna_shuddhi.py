
# Lagna Shuddhi for Marriage and other Muhurtas
# Based on Muhurta Chintamani & BPHS

RASHIS = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]

MALEFIC = ["Mangal","Shani","Rahu","Ketu","Surya"]  # Natural malefics for marriage lagna
BENEFIC = ["Guru","Shukra","Budh","Chandra"]

def check_lagna_shuddhi(lagna_rashi, planets, muhurta_type="marriage"):
    '''
    planets: list of dict with name, rashi
    lagna_rashi: e.g., "Mithuna"
    '''
    lagna_idx = RASHIS.index(lagna_rashi) if lagna_rashi in RASHIS else 0
    
    # Find planets in Lagna, 7th, 8th, 12th
    planets_in_lagna = [p for p in planets if p["rashi"] == lagna_rashi]
    seventh_rashi = RASHIS[(lagna_idx + 6) % 12]
    eighth_rashi = RASHIS[(lagna_idx + 7) % 12]
    twelfth_rashi = RASHIS[(lagna_idx + 11) % 12]
    
    planets_in_7th = [p for p in planets if p["rashi"] == seventh_rashi]
    planets_in_8th = [p for p in planets if p["rashi"] == eighth_rashi]
    
    issues = []
    goods = []
    score = 10
    
    # Rule 1: Lagna should not have malefics for marriage
    for p in planets_in_lagna:
        if p["name"] in MALEFIC and muhurta_type == "marriage":
            issues.append(f"{p['name']} in Lagna ({lagna_rashi}) - Ashubh for {muhurta_type}, reduces shuddhi")
            score -= 2
        else:
            goods.append(f"{p['name']} in Lagna is okay")
    
    # Rule 2: 7th house should be empty or benefic only for marriage
    if muhurta_type == "marriage":
        for p in planets_in_7th:
            if p["name"] in MALEFIC:
                issues.append(f"Malefic {p['name']} in 7th house ({seventh_rashi}) - Very Ashubh for marriage")
                score -= 3
            else:
                goods.append(f"Benefic {p['name']} in 7th - Shubh")
    
    # Rule 3: 8th house should be empty (Mangal Dosha etc)
    for p in planets_in_8th:
        issues.append(f"{p['name']} in 8th house ({eighth_rashi}) - Avoid, causes obstacles")
        score -= 2
    
    # Rule 4: Benefic in Kendra/Trikona is good
    kendra_rashis = [RASHIS[(lagna_idx + i) % 12] for i in [0,3,6,9]]  # 1,4,7,10
    trikona_rashis = [RASHIS[(lagna_idx + i) % 12] for i in [0,4,8]]  # 1,5,9
    
    benefic_in_kendra = sum(1 for p in planets if p["rashi"] in kendra_rashis and p["name"] in BENEFIC)
    if benefic_in_kendra >= 2:
        goods.append(f"{benefic_in_kendra} benefics in Kendra (1,4,7,10) - Highly Shubh")
        score += 1
    
    # Rule 5: Lagna lord position (simplified)
    # Rule 6: Bhadra etc already checked in muhurta
    
    # Final verdict
    if score >= 7:
        verdict = "Lagna Shuddha - Highly Auspicious"
        is_shuddha = True
    elif score >= 5:
        verdict = "Lagna Madhyam - Acceptable with remedy"
        is_shuddha = True
    else:
        verdict = "Lagna Ashuddha - Avoid, choose another lagna"
        is_shuddha = False
    
    return {
        "lagna_rashi": lagna_rashi,
        "seventh_rashi": seventh_rashi,
        "eighth_rashi": eighth_rashi,
        "planets_in_lagna": [p["name"] for p in planets_in_lagna],
        "planets_in_7th": [p["name"] for p in planets_in_7th],
        "planets_in_8th": [p["name"] for p in planets_in_8th],
        "score": f"{max(0,score)}/10",
        "is_shuddha": is_shuddha,
        "verdict": verdict,
        "good_points": goods,
        "doshas": issues,
        "remedy": "Chant Guru mantra and do Gau Daan if score <7" if not is_shuddha else "No remedy needed"
    }

def get_shubh_lagna_list_for_date(dt, lat, lon):
    '''
    For a given date, gives all shubh lagnas in that day (approx every 2 hours)
    '''
    import swisseph as swe
    from datetime import timedelta
    swe.set_ephe_path('.')
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Check 12 lagnas in a day (every 2 hours from sunrise)
    lagnas = []
    base_jd = swe.julday(dt.year, dt.month, dt.day, 0)
    for h in range(0,24,2):
        jd = swe.julday(dt.year, dt.month, dt.day, h)
        asc_deg = swe.houses_ex(jd, lat, lon, b'A', swe.FLG_SIDEREAL)[0][0] % 360
        rashi = RASHIS[int(asc_deg/30)]
        # Get planets for this time
        planets = []
        for pid, name in [(swe.SUN,"Surya"),(swe.MOON,"Chandra"),(swe.MARS,"Mangal"),(swe.MERCURY,"Budh"),(swe.JUPITER,"Guru"),(swe.VENUS,"Shukra"),(swe.SATURN,"Shani")]:
            deg = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)[0][0] % 360
            prashi = RASHIS[int(deg/30)]
            planets.append({"name": name, "rashi": prashi})
        
        shuddhi = check_lagna_shuddhi(rashi, planets, "marriage")
        lagnas.append({
            "time": f"{h:02d}:00",
            "lagna_rashi": rashi,
            "lagna_degree": round(asc_deg,2),
            "is_shuddha": shuddhi["is_shuddha"],
            "score": shuddhi["score"],
            "verdict": shuddhi["verdict"]
        })
    
    return lagnas
