import swisseph as swe
from datetime import datetime
from app.calculations.kundli import KundliCalculator
from app.calculations.recommendations import SIGN_LORDS

class VarshphalCalculator:

    @staticmethod
    def _find_solar_return(natal_sun_long: float, target_year: int) -> float:
        """
        Finds the exact Julian Day when the Sun returns to the natal_sun_long
        in the given target_year.
        """
        # Approximate the return time around the user's birth date in target year
        # We start searching from Jan 1st of target year to be safe, but we can be smarter.
        # Sun moves ~1 degree per day. 
        # But a simple step search is very fast.
        
        jd = swe.julday(target_year, 1, 1, 12.0)
        max_jd = swe.julday(target_year, 12, 31, 12.0)
        
        best_jd = jd
        min_diff = 360.0
        
        # Step 1: Find the closest day
        while jd <= max_jd:
            res = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
            long = res[0][0]
            
            diff = abs(long - natal_sun_long)
            if diff > 180:
                diff = 360 - diff
                
            if diff < min_diff:
                min_diff = diff
                best_jd = jd
                
            jd += 1.0
            
        # Step 2: Refine the exact hour/minute
        # Search within +/- 1.5 days of best_jd by small steps
        fine_jd = best_jd - 1.5
        fine_max = best_jd + 1.5
        step = 1.0 / 24.0 / 60.0 # 1 minute steps
        
        min_diff = 360.0
        exact_jd = best_jd
        
        while fine_jd <= fine_max:
            res = swe.calc_ut(fine_jd, swe.SUN, swe.FLG_SIDEREAL)
            long = res[0][0]
            
            diff = abs(long - natal_sun_long)
            if diff > 180:
                diff = 360 - diff
                
            if diff < min_diff:
                min_diff = diff
                exact_jd = fine_jd
                
            fine_jd += step
            
        return exact_jd

    @staticmethod
    def get_varshphal(natal_jd: float, lat: float, lon: float, target_year: int) -> dict:
        """
        Calculates the Varshphal (Annual Horoscope) for a given year.
        """
        # Get Natal Sun
        natal_positions = KundliCalculator.get_planetary_positions(natal_jd)
        natal_sun_long = natal_positions["Sun"]["longitude"]
        natal_houses = KundliCalculator.get_houses(natal_jd, lat, lon)
        natal_asc_sign = natal_houses["ascendant_sign"]
        
        # 1. Find Solar Return JD
        return_jd = VarshphalCalculator._find_solar_return(natal_sun_long, target_year)
        
        # Convert JD back to Date
        y, m, d, h = swe.revjul(return_jd)
        
        # 2. Cast new chart for return_jd
        varshphal_positions = KundliCalculator.get_planetary_positions(return_jd)
        varshphal_houses = KundliCalculator.get_houses(return_jd, lat, lon)
        varsh_asc_sign = varshphal_houses["ascendant_sign"]
        
        # 3. Calculate Muntha
        # Muntha = (Natal Ascendant Sign + Age) % 12
        # Age = target_year - birth_year
        natal_y, _, _, _ = swe.revjul(natal_jd)
        age = target_year - int(natal_y)
        
        muntha_sign = ((natal_asc_sign - 1 + age) % 12) + 1
        muntha_lord = SIGN_LORDS.get(muntha_sign, "Unknown")
        
        # 4. Varsheshwar (Year Lord)
        # Simplified: Usually Panchadhikaris are calculated, but we will use
        # the Lord of the Varshphal Ascendant as the primary Year Lord for this feature.
        year_lord = SIGN_LORDS.get(varsh_asc_sign, "Unknown")
        
        # Summary analysis based on Muntha placement
        muntha_house = ((muntha_sign - varsh_asc_sign + 12) % 12) + 1
        
        summary = "A standard year of mixed results."
        if muntha_house in [1, 2, 3, 9, 10, 11]:
            summary = "A highly favorable year! The Muntha is placed auspiciously, indicating success, health, and wealth."
        elif muntha_house in [4, 5, 7]:
            summary = "A year of effort and learning. Focus on family and partnerships."
        elif muntha_house in [6, 8, 12]:
            summary = "A challenging year. Prioritize health, avoid unnecessary conflicts, and practice patience."
        
        return {
            "year": target_year,
            "return_date": f"{int(d):02d}/{int(m):02d}/{int(y)}",
            "return_time": f"{int(h):02d}:{int((h % 1) * 60):02d}",
            "age": age,
            "muntha_sign": muntha_sign,
            "muntha_lord": muntha_lord,
            "muntha_house": muntha_house,
            "year_lord": year_lord,
            "varshphal_ascendant_sign": varsh_asc_sign,
            "summary": summary,
            "planets": varshphal_positions
        }
