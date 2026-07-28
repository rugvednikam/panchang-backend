class MatchMakingCalculator:
    
    @staticmethod
    def get_rashi(long: float) -> int:
        return int(long / 30.0) + 1
        
    @staticmethod
    def get_nakshatra(long: float) -> int:
        return int(long / (360.0/27.0)) + 1
        
    @staticmethod
    def calculate_ashtakoota(boy_moon_long: float, girl_moon_long: float):
        b_rashi = MatchMakingCalculator.get_rashi(boy_moon_long)
        g_rashi = MatchMakingCalculator.get_rashi(girl_moon_long)
        
        b_nak = MatchMakingCalculator.get_nakshatra(boy_moon_long)
        g_nak = MatchMakingCalculator.get_nakshatra(girl_moon_long)
        
        # 1. Varna
        def get_varna(rashi):
            if rashi in [4, 8, 12]: return 1
            if rashi in [1, 5, 9]: return 2
            if rashi in [2, 6, 10]: return 3
            return 4
            
        b_varna = get_varna(b_rashi)
        g_varna = get_varna(g_rashi)
        varna = 1.0 if b_varna <= g_varna else 0.0
        
        # 2. Vashya
        vashya = 2.0 if b_rashi == g_rashi else 1.0
        
        # 3. Tara
        def get_tara_points(b, g):
            t1 = ((g - b) % 27) % 9
            if t1 == 0: t1 = 9
            t2 = ((b - g) % 27) % 9
            if t2 == 0: t2 = 9
            b_good = t1 not in [3, 5, 7]
            g_good = t2 not in [3, 5, 7]
            if b_good and g_good: return 3.0
            if b_good or g_good: return 1.5
            return 0.0
            
        tara = get_tara_points(b_nak, g_nak)
        
        # 4. Yoni
        yoni = 4.0 if b_nak == g_nak else 2.0
        
        # 5. Graha Maitri
        maitri = 5.0 if b_rashi == g_rashi else 3.0
        
        # 6. Gana
        def get_gana(nak):
            deva = [1, 5, 7, 8, 13, 15, 17, 22, 27]
            manushya = [2, 4, 6, 11, 12, 20, 21, 25, 26]
            if nak in deva: return 1
            if nak in manushya: return 2
            return 3
            
        bg = get_gana(b_nak)
        gg = get_gana(g_nak)
        
        if bg == gg: gana = 6.0
        elif bg == 1 and gg == 2: gana = 6.0
        elif bg == 2 and gg == 1: gana = 5.0
        elif bg == 3 and gg == 1: gana = 1.0
        elif bg == 1 and gg == 3: gana = 0.0
        elif bg == 3 and gg == 2: gana = 0.0
        elif bg == 2 and gg == 3: gana = 0.0
        else: gana = 0.0
        
        # 7. Bhakoot
        def get_bhakoot(b, g):
            dist = (g - b) % 12
            if dist <= 0: dist += 12
            if dist in [1, 7, 3, 11, 4, 10]: return 7.0
            return 0.0
            
        bhakoot = get_bhakoot(b_rashi, g_rashi)
        
        # 8. Nadi
        def get_nadi(nak):
            rem = nak % 9
            if rem in [1, 6, 7, 0]: return 1
            if rem in [2, 5, 8]: return 2
            return 3
            
        bn = get_nadi(b_nak)
        gn = get_nadi(g_nak)
        nadi = 8.0 if bn != gn else 0.0
        
        total = varna + vashya + tara + yoni + maitri + gana + bhakoot + nadi
        
        return {
            "varna": {"max": 1, "score": varna},
            "vashya": {"max": 2, "score": vashya},
            "tara": {"max": 3, "score": tara},
            "yoni": {"max": 4, "score": yoni},
            "graha_maitri": {"max": 5, "score": maitri},
            "gana": {"max": 6, "score": gana},
            "bhakoot": {"max": 7, "score": bhakoot},
            "nadi": {"max": 8, "score": nadi},
            "total_score": {"max": 36, "score": total},
            "status": "Excellent" if total >= 25 else ("Average" if total >= 18 else "Poor")
        }

    @staticmethod
    def calculate_manglik_dosha(kundli_data: dict) -> dict:
        houses = kundli_data.get("houses", {})
        planets = kundli_data.get("planets", {})
        
        asc_sign = kundli_data.get("ascendant_sign", 1)
        mars_sign = MatchMakingCalculator.get_rashi(planets.get("Mars", {}).get("longitude", 0))
        moon_sign = MatchMakingCalculator.get_rashi(planets.get("Moon", {}).get("longitude", 0))
        venus_sign = MatchMakingCalculator.get_rashi(planets.get("Venus", {}).get("longitude", 0))
        
        def get_house_from(planet_sign, ref_sign):
            h = (planet_sign - ref_sign) + 1
            if h <= 0: h += 12
            return h
            
        h_asc = get_house_from(mars_sign, asc_sign)
        h_moon = get_house_from(mars_sign, moon_sign)
        h_venus = get_house_from(mars_sign, venus_sign)
        
        manglik_houses = [1, 2, 4, 7, 8, 12]
        is_manglik = h_asc in manglik_houses or h_moon in manglik_houses or h_venus in manglik_houses
        
        return {
            "is_manglik": is_manglik,
            "mars_from_ascendant": h_asc,
            "mars_from_moon": h_moon,
            "mars_from_venus": h_venus,
            "is_exception": False,
            "intensity": "High" if is_manglik else "None"
        }

    @staticmethod
    def calculate_papasamya(boy_kundli: dict, girl_kundli: dict) -> dict:
        malefics = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]
        
        def get_malefic_score(kundli):
            score = 0
            asc_sign = kundli.get("ascendant_sign", 1)
            moon_sign = MatchMakingCalculator.get_rashi(kundli.get("planets", {}).get("Moon", {}).get("longitude", 0))
            venus_sign = MatchMakingCalculator.get_rashi(kundli.get("planets", {}).get("Venus", {}).get("longitude", 0))
            
            for m in malefics:
                sign = MatchMakingCalculator.get_rashi(kundli.get("planets", {}).get(m, {}).get("longitude", 0))
                def check_houses(ref):
                    h = (sign - ref) + 1
                    if h <= 0: h += 12
                    return h in [1, 2, 4, 7, 8, 12]
                    
                if check_houses(asc_sign): score += 1
                if check_houses(moon_sign): score += 0.5
                if check_houses(venus_sign): score += 0.5
            return score
            
        boy_score = get_malefic_score(boy_kundli)
        girl_score = get_malefic_score(girl_kundli)
        
        return {
            "boy_dosha_points": boy_score,
            "girl_dosha_points": girl_score,
            "is_compatible": boy_score >= girl_score,
            "status": "Compatible" if boy_score >= girl_score else "Incompatible - Boy has less dosha"
        }

    @staticmethod
    def calculate_10_porutham(boy_nak: int, girl_nak: int) -> dict:
        dist = ((boy_nak - girl_nak) % 27) + 1
        dina = dist % 9 not in [3, 5, 7]
        return {
            "dina": dina,
            "gana": True,
            "mahendra": dist in [4, 7, 10, 13, 16, 19, 22, 25],
            "stree_deergha": dist > 15,
            "yoni": True,
            "rasi": True,
            "rasi_adhipati": True,
            "vasya": True,
            "rajju": True,
            "vedha": True,
            "total_matched": 8,
            "status": "Excellent" if dina else "Average"
        }
