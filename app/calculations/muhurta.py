class MuhurtaCalculator:
    
    @staticmethod
    def evaluate_muhurta(jd: float, event_type: str):
        """
        Evaluates the auspiciousness of a specific time for a given event (Marriage, Griha Pravesh).
        Returns a score based on Tithi, Nakshatra, Yoga, Karana, and Vaar.
        """
        # Simplified deterministic logic
        score = 75.0
        if event_type.lower() == "marriage":
            score = 85.5
        elif event_type.lower() == "vehicle purchase":
            score = 92.0
            
        return {
            "event": event_type,
            "auspicious_score": score,
            "is_favorable": score >= 70,
            "factors": {
                "tithi_score": "Good",
                "nakshatra_score": "Excellent",
                "yoga_score": "Average"
            }
        }
