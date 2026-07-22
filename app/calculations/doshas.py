def evaluate_15_doshas_and_rajju(
    muhurta_type: str = "Griha Pravesh",
    bride_nak: int = 13,
    groom_nak: int = 22
):
    nak_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
        "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
        "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    
    # 5 Rajju
    rajju_groups = {
        "Pada Rajju (Feet) - Mrityu": [6, 15, 24, 5, 14, 23],
        "Kati Rajju (Waist) - Mrityu": [2, 11, 20, 4, 13, 22],
        "Nabhi Rajju (Navel) - Vansh Nash": [3, 12, 21, 7, 16, 25],
        "Kantha Rajju (Neck) - Putra Shok": [8, 17, 26, 1, 10, 19],
        "Shiro Rajju (Head) - Bride death": [9, 18, 27]
    }
    
    bride_rajju = "Unknown"
    groom_rajju = "Unknown"
    for rajju, naks in rajju_groups.items():
        if bride_nak in naks:
            bride_rajju = rajju
        if groom_nak in naks:
            groom_rajju = rajju
            
    rajju_dosh = bride_rajju == groom_rajju
    
    # Saptashalaka
    saptashalaka_dosh = abs(bride_nak - groom_nak) in [1, 2, 6, 8, 11, 14, 16, 19, 21]
    
    # Vedha
    vedha_pairs = {1:18, 2:19, 3:20, 4:21, 5:22, 6:23, 7:24, 8:25, 9:26, 10:27, 11:28, 12:1, 13:2, 14:3}
    vedha_dosh = vedha_pairs.get(bride_nak) == groom_nak

    # 15 generic doshas
    doshas_15 = {
        "saptashalaka": {"present": saptashalaka_dosh, "rule": "7 Shalaka grid - if bride groom or muhurta nak in same line - Ashubh"},
        "rajju_vedha": {"rule": "5 Rajju - Pada/Kati/Nabhi/Kantha/Shiro - same Rajju = Death/Vansh Nash", "present": rajju_dosh, "bride_rajju": bride_rajju, "groom_rajju": groom_rajju},
        "vedha": {"rule": "Vedha - nakshatra vedha - Ashubh", "present": vedha_dosh},
        "latta": {"rule": "Latta - planet kicks nakshatra - if malefic in Latta of muhurta nak - Ashubh", "present": False},
        "tara": {"rule": "Tara - Janma, Sampat SHUBH, Vipat ASHUBH etc", "present": ((groom_nak - bride_nak + 27) % 9 + 1) in [3, 5, 7]},
        "chandra": {"rule": "Chandra - 4,8,12 from Janma Rashi Ashubh", "present": False},
        "kumbh_chakra": {"rule": "Kumbh Chakra - 4 Kumbha - if muhurta in Kumbh Rashi Ashubh for some", "present": False},
        "panchak": {"rule": "Panchak - Dhanishta to Revati 5 nak - fire fear - avoid for Griha Pravesh, Griha Arambh", "present": bride_nak in [23, 24, 25, 26, 27]},
        "bhadra": {"rule": "Bhadra - Prithvi Bhadra - avoid all shubh", "present": False},
        "lath": {"rule": "Lath - stick - inauspicious yoga", "present": False},
        "ekargala": {"rule": "Ekargala - obstruction - nak blocked", "present": False},
        "upgraha": {"rule": "Upgraha - Gulik, Mandi etc in muhurta lagna - Ashubh", "present": False},
        "kranti_samya": {"rule": "Kranti Samya - Sun and planet same declination - Ashubh", "present": False},
        "gochara": {"rule": "Gochara Shuddhi - malefic in 4,8,12 from Moon - Ashubh", "present": False},
        "nadi": {"rule": "Nadi - Aadi/Madhya/Antya - same Nadi for Vivah - Nadi Dosh Putra Dosh - ATI ASHUBH", "present": False}
    }
    
    overall = "ASHUBH - Remedy needed" if any(v.get("present", False) for v in doshas_15.values()) else "SHUBH"

    return {
        "muhurta_type": muhurta_type,
        "bride_nak": bride_nak,
        "groom_nak": groom_nak,
        "bride_nak_name": nak_names[bride_nak - 1] if 1 <= bride_nak <= 27 else "Unknown",
        "groom_nak_name": nak_names[groom_nak - 1] if 1 <= groom_nak <= 27 else "Unknown",
        "15_doshas": doshas_15,
        "overall": overall
    }
