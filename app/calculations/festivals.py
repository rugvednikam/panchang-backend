from datetime import datetime

class FestivalCalculator:
    
    @staticmethod
    def get_festivals_for_month(year: int, month: int):
        """
        Returns a list of Hindu festivals for a given Gregorian month.
        In a real scenario, this involves cross-referencing Tithi with Hindu lunar months.
        This provides a deterministic static map for demonstration.
        """
        # Static mapping for demonstration purposes
        festivals = []
        if month == 10:
            festivals = [
                {"name": "Diwali", "date": f"{year}-10-24", "tithi": "Amavasya"},
                {"name": "Dussehra", "date": f"{year}-10-05", "tithi": "Dashami"}
            ]
        elif month == 3:
            festivals = [
                {"name": "Holi", "date": f"{year}-03-08", "tithi": "Purnima"}
            ]
            
        # Always return Ekadashi / Purnima / Amavasya approximate dates deterministically
        festivals.append({"name": "Ekadashi", "date": f"{year}-{month:02d}-11"})
        festivals.append({"name": "Ekadashi", "date": f"{year}-{month:02d}-26"})
        
        return festivals
