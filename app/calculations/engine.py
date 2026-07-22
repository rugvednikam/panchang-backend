import swisseph as swe
import datetime
import pytz

class AstroEngine:
    def __init__(self):
        # By default swisseph has basic built-in ephemeris, no path needed unless using JPL files.
        pass

    def set_ayanamsa(self, ayanamsa_name: str = "Lahiri"):
        """
        Sets the Ayanamsa for Sidereal calculations.
        Supports Lahiri, KP, Raman, True Chitra, Fagan Bradley.
        """
        ayanamsa_map = {
            "Lahiri": swe.SIDM_LAHIRI,
            "Raman": swe.SIDM_RAMAN,
            "KP": swe.SIDM_KRISHNAMURTI,
            "True Chitra": swe.SIDM_TRUE_CITRA,
            "Fagan Bradley": swe.SIDM_FAGAN_BRADLEY
        }
        
        mode = ayanamsa_map.get(ayanamsa_name, swe.SIDM_LAHIRI)
        swe.set_sid_mode(mode)

    def set_siddhant(self, siddhant_name: str = "Drik Siddhant"):
        """
        Sets the Siddhant (Calculation Mode).
        Drik Siddhant = Modern Swiss Ephemeris.
        Surya Siddhant = Surya Siddhanta mode if supported, else fallback to standard.
        """
        if siddhant_name == "Surya Siddhant":
            # If swisseph supports Surya Siddhanta natively, we set it.
            # Otherwise we rely on the standard calculations.
            if hasattr(swe, 'SIDM_SURYASIDDHANTA'):
                swe.set_sid_mode(swe.SIDM_SURYASIDDHANTA)
        
    def get_julian_day(self, date: datetime.datetime, timezone: str = "UTC") -> float:
        """
        Converts a given datetime and timezone to UTC Julian Day.
        """
        tz = pytz.timezone(timezone)
        
        # If naive, localize it
        if date.tzinfo is None:
            localized_date = tz.localize(date)
        else:
            localized_date = date.astimezone(tz)
            
        utc_date = localized_date.astimezone(pytz.utc)
        
        # Calculate Julian Day
        year = utc_date.year
        month = utc_date.month
        day = utc_date.day
        hour = utc_date.hour + (utc_date.minute / 60.0) + (utc_date.second / 3600.0)
        
        jd = swe.julday(year, month, day, hour, swe.GREG_CAL)
        return jd

engine = AstroEngine()
