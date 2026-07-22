class MatchMakingCalculator:
    
    @staticmethod
    def calculate_ashtakoota(boy_moon_long: float, girl_moon_long: float):
        """
        Calculates Ashtakoota Milan (36 points) based on Moon longitudes (Nakshatra and Rasi).
        This is a simplified mock implementation that returns a deterministic score.
        In production, exact Gana, Nadi, Bhakoot matrices are computed based on Nakshatra and Pada.
        """
        # Basic deterministic pseudo-calculation
        diff = abs(boy_moon_long - girl_moon_long)
        
        # 1. Varna (1)
        varna = 1.0 if diff % 4 < 2 else 0.0
        # 2. Vashya (2)
        vashya = 2.0 if diff % 3 < 1.5 else 1.0
        # 3. Tara (3)
        tara = 1.5
        # 4. Yoni (4)
        yoni = 3.0
        # 5. Graha Maitri (5)
        maitri = 4.0
        # 6. Gana (6)
        gana = 6.0
        # 7. Bhakoot (7)
        bhakoot = 7.0 if diff > 60 else 0.0
        # 8. Nadi (8)
        nadi = 8.0 if diff > 120 else 0.0
        
        total = varna + vashya + tara + yoni + maitri + gana + bhakoot + nadi
        
        return {
            "varna": {"max": 1, "score": varna},
            "vashya": {"max": 2, "score": vashya},
            "tara": {"max": 3, "score": tara},
            "yoni": {"max": 4, "score": yoni},
            "graha_maitri": {"max": 5, "score": maitri},
            "gana": {"max": 6, "score": gana},
            "bhakoot": {"max": 7, "score": bhakoot},
            "nadi": {"max": 8, "score": nadi},
            "total_score": {"max": 36, "score": total},
            "status": "Excellent" if total >= 25 else ("Average" if total >= 18 else "Poor")
        }
