from app.calculations.kp_system import KPSystemCalculator
from app.calculations.engine import engine
from datetime import datetime
import json

def run_test():
    dt = datetime(1990, 1, 1, 12, 0, 0)
    jd = engine.get_julian_day(dt, "Asia/Kolkata")
    
    print("--- KP Prashna 1-249 Table (First 5) ---")
    table = KPSystemCalculator.generate_249_table()
    for row in table[:5]:
        print(row)
        
    print("\n--- KP Prashna Ascendant for #100 ---")
    asc = KPSystemCalculator.get_prashna_ascendant(100)
    print(f"Ascendant: {asc} degrees")
    
    print("\n--- Ruling Planets ---")
    ruling = KPSystemCalculator.get_ruling_planets(jd, 19.0760, 72.8777)
    print(ruling)
    
    print("\n--- Khullar KP Kundli (Prashna 100) ---")
    kundli = KPSystemCalculator.get_kp_kundli(jd, 19.0760, 72.8777, prashna_number=100)
    
    # Print the Ascendant and 1st house lords
    print(f"Ascendant: {kundli['ascendant']}")
    h1 = kundli['houses'][1]
    print(f"House 1: Star={h1['star_lord']}, Sub={h1['sub_lord']}, SubSub={h1['sub_sub_lord']}")
    
    # Print Moon lords
    moon = kundli['planets']['Moon']
    print(f"Moon: Star={moon['star_lord']}, Sub={moon['sub_lord']}, SubSub={moon['sub_sub_lord']}")

if __name__ == "__main__":
    run_test()
