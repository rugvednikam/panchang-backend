from typing import Dict, List

# Basic Mantras and Remedies for each planet
PLANET_REMEDIES = {
    "Sun": {
        "mantra": "Om Hraam Hreem Hroum Sah Suryaya Namah",
        "beej_mantra": "Om Ghrini Suryaya Namah",
        "charity": "Donate wheat, jaggery, and copper on Sundays.",
        "karma": "Respect your father and authority figures. Wake up before sunrise.",
        "fasting": "Observe fast on Sundays."
    },
    "Moon": {
        "mantra": "Om Shraam Shreem Shroum Sah Chandramase Namah",
        "beej_mantra": "Om Som Somaya Namah",
        "charity": "Donate milk, rice, and silver on Mondays.",
        "karma": "Respect your mother. Meditate daily for emotional balance.",
        "fasting": "Observe fast on Mondays."
    },
    "Mars": {
        "mantra": "Om Kraam Kreem Kroum Sah Bhaumaya Namah",
        "beej_mantra": "Om Ang Angarakaya Namah",
        "charity": "Donate red lentils (masoor dal) and red clothes on Tuesdays.",
        "karma": "Control anger. Donate blood if possible. Recite Hanuman Chalisa.",
        "fasting": "Observe fast on Tuesdays."
    },
    "Mercury": {
        "mantra": "Om Braam Breem Broum Sah Budhaya Namah",
        "beej_mantra": "Om Bum Budhaya Namah",
        "charity": "Donate green gram (moong dal) and green clothes on Wednesdays.",
        "karma": "Help students with their education. Feed cows green grass.",
        "fasting": "Observe fast on Wednesdays."
    },
    "Jupiter": {
        "mantra": "Om Graam Greem Groum Sah Gurave Namah",
        "beej_mantra": "Om Brim Brihaspataye Namah",
        "charity": "Donate chana dal, turmeric, and yellow clothes on Thursdays.",
        "karma": "Respect teachers, gurus, and elders. Read spiritual texts.",
        "fasting": "Observe fast on Thursdays."
    },
    "Venus": {
        "mantra": "Om Draam Dreem Droum Sah Shukraya Namah",
        "beej_mantra": "Om Shum Shukraya Namah",
        "charity": "Donate sugar, rice, and white clothes on Fridays.",
        "karma": "Maintain cleanliness. Respect women. Use pleasant fragrances.",
        "fasting": "Observe fast on Fridays."
    },
    "Saturn": {
        "mantra": "Om Praam Preem Proum Sah Shanaischaraya Namah",
        "beej_mantra": "Om Sham Shanaischaraya Namah",
        "charity": "Donate mustard oil, black sesame seeds, and black clothes on Saturdays.",
        "karma": "Help the poor, elderly, and differently-abled. Be disciplined and honest.",
        "fasting": "Observe fast on Saturdays."
    },
    "Rahu": {
        "mantra": "Om Bhraam Bhreem Bhroum Sah Rahave Namah",
        "beej_mantra": "Om Ram Rahave Namah",
        "charity": "Donate coconut, barley, and dark clothes on Saturdays or Wednesdays.",
        "karma": "Feed street dogs. Avoid unethical shortcuts and cheating.",
        "fasting": "Observe fast on Saturdays."
    },
    "Ketu": {
        "mantra": "Om Sraam Sreem Sroum Sah Ketave Namah",
        "beej_mantra": "Om Kem Ketave Namah",
        "charity": "Donate black and white blankets, and sesame seeds.",
        "karma": "Feed stray dogs. Practice detachment and spirituality.",
        "fasting": "Observe fast on Tuesdays or Thursdays."
    }
}

class RemediesCalculator:
    
    @staticmethod
    def get_remedies_for_dasha(maha_dasha_lord: str, antar_dasha_lord: str) -> dict:
        """
        Returns the remedies for the current Maha Dasha and Antar Dasha lords.
        """
        remedies = {}
        
        if maha_dasha_lord in PLANET_REMEDIES:
            remedies["maha_dasha"] = {
                "planet": maha_dasha_lord,
                **PLANET_REMEDIES[maha_dasha_lord]
            }
            
        if antar_dasha_lord in PLANET_REMEDIES:
            remedies["antar_dasha"] = {
                "planet": antar_dasha_lord,
                **PLANET_REMEDIES[antar_dasha_lord]
            }
            
        return remedies
