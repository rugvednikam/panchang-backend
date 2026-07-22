import swisseph as swe
from app.calculations.engine import engine

class KundliCalculator:
    
    PLANETS = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": -1 # Special case
    }
    
    @staticmethod
    def get_planetary_positions(jd: float) -> dict:
        positions = {}
        for name, planet_id in KundliCalculator.PLANETS.items():
            if name == "Ketu":
                # Ketu is exactly 180 degrees opposite Rahu
                rahu_long = positions["Rahu"]["longitude"]
                ketu_long = (rahu_long + 180) % 360
                positions[name] = {
                    "longitude": ketu_long,
                    "is_retrograde": positions["Rahu"]["is_retrograde"],
                    "sign": int(ketu_long / 30) + 1
                }
                continue
                
            res = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL | swe.FLG_SPEED)
            long = res[0][0]
            speed = res[0][3]
            
            positions[name] = {
                "longitude": long,
                "is_retrograde": speed < 0,
                "sign": int(long / 30) + 1
            }
        return positions

    @staticmethod
    def get_ayanamsa(jd: float) -> float:
        return swe.get_ayanamsa_ut(jd)

    @staticmethod
    def get_houses(jd: float, lat: float, lon: float, hsys: str = 'P') -> dict:
        """
        hsys: Placidus = 'P', Koch = 'K', Whole Sign = 'W'
        Note: Swiss Ephemeris requires Geographic coordinates for house calculations.
        Returns Ascendant and House Cusps.
        """
        # True sidereal mode for houses
        cusps, ascmc = swe.houses_ex(jd, lat, lon, bytes(hsys, "ascii"), swe.FLG_SIDEREAL)
        
        # ascmc[0] is Ascendant
        ascendant = ascmc[0]
        
        houses = {}
        for i in range(12):
            houses[i+1] = {
                "cusp_longitude": cusps[i],
                "sign": int(cusps[i] / 30) + 1
            }
            
        return {
            "ascendant": ascendant,
            "ascendant_sign": int(ascendant / 30) + 1,
            "houses": houses
        }
