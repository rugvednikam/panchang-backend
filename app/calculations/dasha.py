from datetime import datetime, timedelta

class DashaCalculator:
    # Simplified placeholder for Vimshottari Dasha calculation logic
    # Vimshottari is calculated based on Moon's longitude and Nakshatra
    
    @staticmethod
    def get_vimshottari_dasha(moon_longitude: float, birth_date: datetime):
        """
        Returns starting dasha based on moon longitude and generates all 9 Mahadasha periods.
        """
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        years = [7, 20, 6, 10, 7, 18, 16, 19, 17]
        
        moon_min = moon_longitude * 60
        nak_number = int(moon_min / 800)
        lord_index = nak_number % 9
        
        passed_min = moon_min % 800
        remaining_fraction = 1.0 - (passed_min / 800)
        balance_years = years[lord_index] * remaining_fraction
        
        periods = []
        current_date = birth_date
        
        # First period is the balance
        first_period_end = current_date + timedelta(days=balance_years * 365.25)
        periods.append({
            "planet": lords[lord_index],
            "start_date": current_date.isoformat(),
            "end_date": first_period_end.isoformat()
        })
        current_date = first_period_end
        
        # Remaining 8 periods
        for i in range(1, 9):
            idx = (lord_index + i) % 9
            period_years = years[idx]
            period_end = current_date + timedelta(days=period_years * 365.25)
            periods.append({
                "planet": lords[idx],
                "start_date": current_date.isoformat(),
                "end_date": period_end.isoformat()
            })
            current_date = period_end
            
        return {
            "starting_dasha": lords[lord_index],
            "balance_years": balance_years,
            "periods": periods
        }
