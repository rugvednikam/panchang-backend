def calculate_numerology(dob: str):
    """
    Calculates Moolank (Root Number) and Bhagyank (Destiny Number) from Date of Birth.
    Format of dob: YYYY-MM-DD
    """
    try:
        parts = dob.split('-')
        if len(parts) != 3:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
            
        day_str = parts[2]
        
        # Moolank is sum of day digits
        moolank_sum = sum(int(d) for d in day_str if d.isdigit())
        moolank = _reduce_to_single_digit(moolank_sum)
        
        # Bhagyank is sum of all digits in DOB
        bhagyank_sum = sum(int(d) for d in dob if d.isdigit())
        bhagyank = _reduce_to_single_digit(bhagyank_sum)
        
        return {
            "moolank": {
                "number": moolank,
                "planet": _get_ruling_planet(moolank),
                "traits": _get_traits(moolank),
                "lucky_colors": _get_lucky_colors(moolank)
            },
            "bhagyank": {
                "number": bhagyank,
                "planet": _get_ruling_planet(bhagyank),
                "traits": _get_traits(bhagyank),
                "lucky_colors": _get_lucky_colors(bhagyank)
            }
        }
    except Exception as e:
        return {"error": str(e)}

def _reduce_to_single_digit(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _get_ruling_planet(n: int) -> str:
    planets = {
        1: "Sun (Surya)",
        2: "Moon (Chandra)",
        3: "Jupiter (Guru)",
        4: "Rahu",
        5: "Mercury (Budh)",
        6: "Venus (Shukra)",
        7: "Ketu",
        8: "Saturn (Shani)",
        9: "Mars (Mangal)"
    }
    return planets.get(n, "Unknown")

def _get_traits(n: int) -> str:
    traits = {
        1: "Leadership, independence, originality, ambition.",
        2: "Cooperation, sensitivity, balance, diplomacy.",
        3: "Creativity, self-expression, optimism, communication.",
        4: "Discipline, practicality, hard work, organization.",
        5: "Freedom, adaptability, adventure, curiosity.",
        6: "Responsibility, harmony, nurturing, family-oriented.",
        7: "Spirituality, analysis, intuition, introspection.",
        8: "Ambition, authority, material success, realism.",
        9: "Humanitarianism, compassion, endings, selflessness."
    }
    return traits.get(n, "No traits found.")

def _get_lucky_colors(n: int) -> list:
    colors = {
        1: ["Gold", "Orange", "Yellow"],
        2: ["White", "Silver", "Pale Green"],
        3: ["Yellow", "Purple", "Lilac"],
        4: ["Blue", "Grey", "Khaki"],
        5: ["Green", "Turquoise", "Light Blue"],
        6: ["Blue", "Pink", "White"],
        7: ["Light Green", "Light Yellow", "White"],
        8: ["Black", "Dark Blue", "Dark Grey"],
        9: ["Red", "Crimson", "Pink"]
    }
    return colors.get(n, [])
