import swisseph as swe
from app.calculations.engine import engine

class KPSystemCalculator:
    VIMSHOTTARI_LORDS = [
        ("Ketu", 7), ("Venus", 20), ("Sun", 6),
        ("Moon", 10), ("Mars", 7), ("Rahu", 18),
        ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
    ]
    
    @staticmethod
    def get_star_and_sub(longitude: float) -> dict:
        nak_len = 360.0 / 27.0
        nak_idx = int(longitude / nak_len)
        lord_idx = nak_idx % 9
        
        star_lord = KPSystemCalculator.VIMSHOTTARI_LORDS[lord_idx][0]
        
        rem_long = longitude % nak_len
        current_lord_idx = lord_idx
        passed_arc = 0.0
        
        sub_lord = ""
        sub_sub_lord = ""
        
        for _ in range(9):
            lord_name, lord_years = KPSystemCalculator.VIMSHOTTARI_LORDS[current_lord_idx]
            sub_arc = (lord_years / 120.0) * nak_len
            
            if passed_arc + sub_arc > rem_long:
                sub_lord = lord_name
                # Find sub-sub lord
                sub_rem = rem_long - passed_arc
                ss_lord_idx = current_lord_idx
                ss_passed_arc = 0.0
                
                for _ in range(9):
                    ss_name, ss_years = KPSystemCalculator.VIMSHOTTARI_LORDS[ss_lord_idx]
                    ss_arc = (ss_years / 120.0) * sub_arc
                    if ss_passed_arc + ss_arc > sub_rem:
                        sub_sub_lord = ss_name
                        break
                    ss_passed_arc += ss_arc
                    ss_lord_idx = (ss_lord_idx + 1) % 9
                    
                break
                
            passed_arc += sub_arc
            current_lord_idx = (current_lord_idx + 1) % 9
            
        return {
            "star_lord": star_lord,
            "sub_lord": sub_lord,
            "sub_sub_lord": sub_sub_lord
        }

    @staticmethod
    def generate_249_table():
        table = []
        nak_len = 360.0 / 27.0
        
        current_deg = 0.0
        count = 1
        
        # Rounding protection
        while current_deg < 359.999:
            sign_idx = int(current_deg / 30.0)
            sign_end = (sign_idx + 1) * 30.0
            
            nak_idx = int(current_deg / nak_len)
            lord_idx = nak_idx % 9
            
            star_lord = KPSystemCalculator.VIMSHOTTARI_LORDS[lord_idx][0]
            
            rem_long = current_deg % nak_len
            curr_sub_idx = lord_idx
            passed_arc = 0.0
            sub_arc = 0.0
            
            for _ in range(9):
                lord_name, lord_years = KPSystemCalculator.VIMSHOTTARI_LORDS[curr_sub_idx]
                sub_arc = (lord_years / 120.0) * nak_len
                # 0.00001 handles float precision issues
                if passed_arc + sub_arc > rem_long + 0.00001:
                    break
                passed_arc += sub_arc
                curr_sub_idx = (curr_sub_idx + 1) % 9
                
            sub_end = (nak_idx * nak_len) + passed_arc + sub_arc
            segment_end = min(sub_end, sign_end)
            
            table.append({
                "prashna_number": count,
                "sign": sign_idx + 1,
                "star_lord": star_lord,
                "sub_lord": KPSystemCalculator.VIMSHOTTARI_LORDS[curr_sub_idx][0],
                "start_degree": current_deg,
                "end_degree": segment_end
            })
            
            current_deg = segment_end
            count += 1
            
        return table

    @staticmethod
    def get_prashna_ascendant(number: int) -> float:
        if number < 1 or number > 249:
            number = 1
        table = KPSystemCalculator.generate_249_table()
        # Number is 1-indexed
        return table[number - 1]["start_degree"]

    @staticmethod
    def get_ruling_planets(jd: float, lat: float, lon: float) -> dict:
        day_lords = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        jd_int = int(jd + 0.5)
        day_of_week = (jd_int + 1) % 7
        dl = day_lords[day_of_week]
        dl_map = {"Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", "Wednesday": "Mercury", "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"}
        
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
        asc = ascmc[0]
        
        moon_pos = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        
        def get_sign_lord(deg):
            sign = int(deg / 30)
            lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
            return lords[sign]
            
        asc_sl = get_sign_lord(asc)
        moon_sl = get_sign_lord(moon_pos)
        
        asc_star = KPSystemCalculator.get_star_and_sub(asc)["star_lord"]
        moon_star = KPSystemCalculator.get_star_and_sub(moon_pos)["star_lord"]
        
        return {
            "day_lord": dl_map[dl],
            "ascendant_sign_lord": asc_sl,
            "ascendant_star_lord": asc_star,
            "moon_sign_lord": moon_sl,
            "moon_star_lord": moon_star
        }

    @staticmethod
    def get_kp_kundli(jd: float, lat: float, lon: float, prashna_number: int = None) -> dict:
        """
        Generates a full KP chart with Placidus houses, Sub Lords, and Sub-Sub Lords (Khullar).
        If prashna_number is provided (1-249), the ascendant is fixed to that number's start degree.
        """
        # Get placidus cusps
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
        
        if prashna_number is not None and 1 <= prashna_number <= 249:
            synthetic_asc = KPSystemCalculator.get_prashna_ascendant(prashna_number)
            # In true Prashna, you cast the entire house system based on this Ascendant.
            # We would need to reverse calculate a time that gives this Ascendant, or manually shift cusps.
            # For scaffolding, we will just override the Ascendant.
            asc = synthetic_asc
        else:
            asc = ascmc[0]
            
        # Get planets
        from app.calculations.kundli import KundliCalculator
        planets = KundliCalculator.get_planetary_positions(jd)
        
        # Enrich planets with star and sub lords
        for name, data in planets.items():
            lords = KPSystemCalculator.get_star_and_sub(data["longitude"])
            data.update(lords)
            
        # Enrich houses
        enriched_houses = {}
        for i in range(12):
            h_deg = cusps[i]
            lords = KPSystemCalculator.get_star_and_sub(h_deg)
            enriched_houses[i+1] = {
                "degree": h_deg,
                "sign": int(h_deg / 30) + 1,
                **lords
            }
            
        ruling = KPSystemCalculator.get_ruling_planets(jd, lat, lon)
            
        return {
            "ascendant": asc,
            "houses": enriched_houses,
            "planets": planets,
            "ruling_planets": ruling,
            "prashna_number": prashna_number
        }
