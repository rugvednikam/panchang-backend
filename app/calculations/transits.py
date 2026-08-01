import swisseph as swe
from datetime import datetime, timedelta
import math

class TransitCalculator:
    
    @staticmethod
    def _find_next_transit(start_jd: float, planet: int, target_sign: int, max_years: int = 40) -> tuple:
        """
        Finds when the planet enters and leaves the target_sign.
        Returns (entry_jd, exit_jd)
        """
        jd = start_jd
        # Step size in days
        step = 5
        entry_jd = None
        exit_jd = None
        
        # Max loop limit to prevent infinite loops
        max_jd = start_jd + (max_years * 365.25)
        
        in_target_sign = False
        
        while jd <= max_jd:
            res = swe.calc_ut(jd, planet, swe.FLG_SIDEREAL)
            long = res[0][0]
            current_sign = int(long / 30) + 1
            
            if current_sign == target_sign and not in_target_sign:
                # Entered the sign
                # Refine entry
                refined_jd = jd
                while True:
                    refined_jd -= 1
                    r_res = swe.calc_ut(refined_jd, planet, swe.FLG_SIDEREAL)
                    if int(r_res[0][0] / 30) + 1 != target_sign:
                        entry_jd = refined_jd + 1
                        break
                in_target_sign = True
                
            elif current_sign != target_sign and in_target_sign:
                # Exited the sign
                # Refine exit
                refined_jd = jd
                while True:
                    refined_jd -= 1
                    r_res = swe.calc_ut(refined_jd, planet, swe.FLG_SIDEREAL)
                    if int(r_res[0][0] / 30) + 1 == target_sign:
                        exit_jd = refined_jd + 1
                        break
                break # We found one full transit
            
            jd += step
            
        return entry_jd, exit_jd

    @staticmethod
    def get_sadhe_sati_timeline(natal_moon_sign: int, birth_date: datetime) -> list:
        """
        Calculates the 3 phases of Sadhe Sati starting from the person's birth or current date.
        We'll find the *current or next* Sadhe Sati period.
        Phase 1: Saturn in 12th from Moon
        Phase 2: Saturn in 1st from Moon
        Phase 3: Saturn in 2nd from Moon
        """
        phase1_sign = ((natal_moon_sign + 10) % 12) + 1
        phase2_sign = natal_moon_sign
        phase3_sign = (natal_moon_sign % 12) + 1
        
        # Start searching from a few years ago to see if currently in it, or from today.
        now = datetime.now()
        search_start = now - timedelta(days=365 * 5) # search from 5 years ago
        start_year = search_start.year
        start_month = search_start.month
        start_day = search_start.day
        
        start_jd = swe.julday(start_year, start_month, start_day, 12.0)
        
        # Find Phase 1
        p1_entry, p1_exit = TransitCalculator._find_next_transit(start_jd, swe.SATURN, phase1_sign)
        if not p1_entry:
            return []
            
        # Find Phase 2 (start from Phase 1 entry to save time)
        p2_entry, p2_exit = TransitCalculator._find_next_transit(p1_entry, swe.SATURN, phase2_sign)
        
        # Find Phase 3
        p3_entry, p3_exit = TransitCalculator._find_next_transit(p2_entry, swe.SATURN, phase3_sign)
        
        def jd_to_date(jd):
            if not jd: return None
            year, month, day, hour = swe.revjul(jd)
            try:
                return datetime(year, month, int(day)).strftime("%d %b %Y")
            except:
                return f"{int(day)}/{month}/{year}"

        phases = []
        if p1_entry:
            phases.append({
                "phase": "Phase 1 (Rising)",
                "sign": phase1_sign,
                "start": jd_to_date(p1_entry),
                "end": jd_to_date(p1_exit),
                "remedy": "Chant Hanuman Chalisa daily. Donate black clothes or shoes on Saturdays."
            })
        if p2_entry:
            phases.append({
                "phase": "Phase 2 (Peak)",
                "sign": phase2_sign,
                "start": jd_to_date(p2_entry),
                "end": jd_to_date(p2_exit),
                "remedy": "Recite Shani Stotram. Light a mustard oil lamp under a Peepal tree on Saturdays."
            })
        if p3_entry:
            phases.append({
                "phase": "Phase 3 (Setting)",
                "sign": phase3_sign,
                "start": jd_to_date(p3_entry),
                "end": jd_to_date(p3_exit),
                "remedy": "Offer water to Lord Shiva. Respect elders and avoid starting risky ventures."
            })
            
        return phases
