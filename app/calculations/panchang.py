import swisseph as swe
from datetime import datetime
from app.calculations.engine import engine

class PanchangCalculator:
    
    @staticmethod
    def _jd_to_utc_iso(jd: float) -> str:
        # GREG_CAL = 1 in pyswisseph
        yr, mo, dy, hr = swe.revjul(jd, 1)
        hrs = int(hr)
        mins = int((hr - hrs) * 60)
        secs = int((((hr - hrs) * 60) - mins) * 60)
        return f"{yr}-{mo:02d}-{dy:02d}T{hrs:02d}:{mins:02d}:{secs:02d}Z"

    @staticmethod
    def _find_exact_time(jd_start: float, jd_end: float, target_angle: float, func) -> float:
        left = jd_start
        right = jd_end
        val_left = func(left)
        val_right = func(right)
        
        # Handle wrap-around
        if val_left > val_right and target_angle <= val_left:
            val_right += 360
        if target_angle < val_left and val_right > 360:
            target_angle += 360
            
        for _ in range(30):
            mid = (left + right) / 2.0
            val_mid = func(mid)
            if val_mid < val_left and target_angle >= val_left:
                val_mid += 360
                
            if val_mid < target_angle:
                left = mid
            else:
                right = mid
        return left

    @staticmethod
    def _get_tithi_angle(jd: float) -> float:
        sun_long = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_long = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        return (moon_long - sun_long) % 360

    @staticmethod
    def get_tithi(jd: float) -> dict:
        angle = PanchangCalculator._get_tithi_angle(jd)
        tithi_number = int(angle / 12) + 1
        paksha = "Shukla" if tithi_number <= 15 else "Krishna"
        
        start_angle = (tithi_number - 1) * 12
        end_angle = tithi_number * 12
        jd_start = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, start_angle, PanchangCalculator._get_tithi_angle)
        jd_end = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, end_angle, PanchangCalculator._get_tithi_angle)
        
        return {
            "tithi_number": tithi_number,
            "paksha": paksha,
            "degrees": angle % 12,
            "total_angle": angle,
            "start_time": PanchangCalculator._jd_to_utc_iso(jd_start),
            "end_time": PanchangCalculator._jd_to_utc_iso(jd_end)
        }

    @staticmethod
    def _get_moon_long(jd: float) -> float:
        return swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

    @staticmethod
    def get_nakshatra(jd: float) -> dict:
        moon_long = PanchangCalculator._get_moon_long(jd)
        nakshatra_length = 360.0 / 27.0
        nakshatra_number = int(moon_long / nakshatra_length) + 1
        pada = int((moon_long % nakshatra_length) / (nakshatra_length / 4)) + 1
        
        start_angle = (nakshatra_number - 1) * nakshatra_length
        end_angle = nakshatra_number * nakshatra_length
        jd_start = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, start_angle, PanchangCalculator._get_moon_long)
        jd_end = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, end_angle, PanchangCalculator._get_moon_long)
        
        return {
            "nakshatra_number": nakshatra_number,
            "pada": pada,
            "longitude": moon_long,
            "start_time": PanchangCalculator._jd_to_utc_iso(jd_start),
            "end_time": PanchangCalculator._jd_to_utc_iso(jd_end)
        }

    @staticmethod
    def _get_yoga_angle(jd: float) -> float:
        sun_long = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
        moon_long = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        return (sun_long + moon_long) % 360

    @staticmethod
    def get_yoga(jd: float) -> dict:
        sum_long = PanchangCalculator._get_yoga_angle(jd)
        yoga_length = 360.0 / 27.0
        yoga_number = int(sum_long / yoga_length) + 1
        
        start_angle = (yoga_number - 1) * yoga_length
        end_angle = yoga_number * yoga_length
        jd_start = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, start_angle, PanchangCalculator._get_yoga_angle)
        jd_end = PanchangCalculator._find_exact_time(jd - 1.5, jd + 1.5, end_angle, PanchangCalculator._get_yoga_angle)
        
        return {
            "yoga_number": yoga_number,
            "longitude": sum_long,
            "start_time": PanchangCalculator._jd_to_utc_iso(jd_start),
            "end_time": PanchangCalculator._jd_to_utc_iso(jd_end)
        }

    @staticmethod
    def get_karana(jd: float) -> dict:
        angle = PanchangCalculator._get_tithi_angle(jd)
        karana_number = int(angle / 6) + 1
        
        start_angle = (karana_number - 1) * 6
        end_angle = karana_number * 6
        jd_start = PanchangCalculator._find_exact_time(jd - 1.0, jd + 1.0, start_angle, PanchangCalculator._get_tithi_angle)
        jd_end = PanchangCalculator._find_exact_time(jd - 1.0, jd + 1.0, end_angle, PanchangCalculator._get_tithi_angle)
        
        return {
            "karana_number": karana_number,
            "total_angle": angle,
            "start_time": PanchangCalculator._jd_to_utc_iso(jd_start),
            "end_time": PanchangCalculator._jd_to_utc_iso(jd_end)
        }
        
    @staticmethod
    def get_vara(date: datetime) -> int:
        return (date.weekday() + 1) % 7
