import swisseph as swe
from datetime import datetime, date, timedelta


class FestivalCalculator:

    # Tithi-based special day detection
    TITHI_NAMES = [
        "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
        "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
    ]

    # Static known festivals mapped by (month, day) for common Gregorian dates
    # This is a fallback; dynamic detection is preferred
    STATIC_FESTIVALS = {
        (1, 14): "Makar Sankranti",
        (1, 15): "Pongal",
        (1, 26): "Republic Day",
        (3, 8): "Maha Shivaratri",
        (3, 25): "Holi",
        (3, 26): "Dhulandi",
        (4, 6): "Ugadi / Gudi Padwa",
        (4, 10): "Ram Navami",
        (4, 14): "Baisakhi",
        (5, 12): "Akshaya Tritiya",
        (7, 17): "Guru Purnima",
        (8, 15): "Independence Day",
        (8, 26): "Janmashtami",
        (9, 5): "Ganesh Chaturthi",
        (10, 2): "Gandhi Jayanti",
        (10, 12): "Dussehra",
        (10, 20): "Karwa Chauth",
        (11, 1): "Diwali",
        (11, 2): "Govardhan Puja",
        (11, 3): "Bhai Dooj",
        (11, 15): "Kartik Purnima",
        (11, 27): "Guru Nanak Jayanti",
        (12, 25): "Christmas",
    }

    RASHI_NAMES = [
        "Mesha", "Vrishabha", "Mithuna", "Karka",
        "Simha", "Kanya", "Tula", "Vrishchika",
        "Dhanu", "Makara", "Kumbha", "Meena",
    ]

    SANKRANTI_NAMES = [
        "Mesha Sankranti", "Vrishabha Sankranti", "Mithuna Sankranti",
        "Karka Sankranti", "Simha Sankranti", "Kanya Sankranti",
        "Tula Sankranti", "Vrishchika Sankranti", "Dhanu Sankranti",
        "Makara Sankranti", "Kumbha Sankranti", "Meena Sankranti",
    ]

    @staticmethod
    def get_special_days_for_tithi(tithi_number: int, paksha: str) -> dict:
        """
        Detect special days from tithi number (1-30).
        Returns a dict with boolean flags and labels.
        """
        result = {
            "is_ekadashi": False,
            "is_purnima": False,
            "is_amavasya": False,
            "is_chaturthi": False,
            "is_pradosh": False,
            "is_ashtami": False,
            "special_tag": None,
        }

        # Map tithi_number to its name index (0-based)
        if tithi_number < 1 or tithi_number > 30:
            return result

        tithi_in_paksha = tithi_number if tithi_number <= 15 else tithi_number - 15

        if tithi_in_paksha == 11:
            result["is_ekadashi"] = True
            if paksha == "Shukla":
                result["special_tag"] = "Shukla Ekadashi"
            else:
                result["special_tag"] = "Krishna Ekadashi"

        if tithi_number == 15:
            result["is_purnima"] = True
            result["special_tag"] = "Purnima"

        if tithi_number == 30:
            result["is_amavasya"] = True
            result["special_tag"] = "Amavasya"

        if tithi_in_paksha == 4:
            result["is_chaturthi"] = True
            if paksha == "Shukla":
                result["special_tag"] = "Vinayaki Chaturthi"
            else:
                result["special_tag"] = "Sankashti Chaturthi"

        if tithi_in_paksha == 13:
            result["is_pradosh"] = True
            result["special_tag"] = f"{paksha} Pradosh Vrat"

        if tithi_in_paksha == 8:
            result["is_ashtami"] = True

        return result

    @staticmethod
    def check_sankranti(d: date) -> str | None:
        """
        Check if the Sun enters a new Rashi on this date.
        Compares Sun longitude at noon today vs yesterday.
        """
        try:
            jd_today = swe.julday(d.year, d.month, d.day, 6.0)  # noon IST ≈ 6:30 UTC
            jd_yesterday = jd_today - 1.0

            sun_today = swe.calc_ut(jd_today, swe.SUN)[0][0]
            sun_yesterday = swe.calc_ut(jd_yesterday, swe.SUN)[0][0]

            rashi_today = int(sun_today / 30)
            rashi_yesterday = int(sun_yesterday / 30)

            if rashi_today != rashi_yesterday:
                return FestivalCalculator.SANKRANTI_NAMES[rashi_today]
        except Exception:
            pass
        return None

    @staticmethod
    def get_festivals_for_date(d: date, tithi_number: int, paksha: str) -> list:
        """
        Get all festivals/special events for a specific date.
        Combines dynamic Tithi-based detection with static festival map.
        """
        festivals = []

        # Dynamic Tithi-based
        special = FestivalCalculator.get_special_days_for_tithi(tithi_number, paksha)
        if special["special_tag"]:
            festivals.append(special["special_tag"])

        # Sankranti check
        sankranti = FestivalCalculator.check_sankranti(d)
        if sankranti:
            festivals.append(sankranti)

        # Static festival overlay
        key = (d.month, d.day)
        if key in FestivalCalculator.STATIC_FESTIVALS:
            static_name = FestivalCalculator.STATIC_FESTIVALS[key]
            if static_name not in festivals:
                festivals.append(static_name)

        return festivals

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
