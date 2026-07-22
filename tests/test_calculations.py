import pytest
from datetime import datetime
from app.calculations.engine import engine
from app.calculations.panchang import PanchangCalculator

def test_julian_day_calculation():
    # Known JD for J2000 epoch: 2000-01-01 12:00:00 UTC is exactly 2451545.0
    dt = datetime(2000, 1, 1, 12, 0, 0)
    jd = engine.get_julian_day(dt, "UTC")
    assert abs(jd - 2451545.0) < 0.0001

def test_panchang_elements():
    # Just a smoke test to ensure no exceptions are thrown and shapes are correct
    jd = 2451545.0
    tithi = PanchangCalculator.get_tithi(jd)
    assert "tithi_number" in tithi
    assert 1 <= tithi["tithi_number"] <= 30
    
    nakshatra = PanchangCalculator.get_nakshatra(jd)
    assert "nakshatra_number" in nakshatra
    assert 1 <= nakshatra["nakshatra_number"] <= 27
    
    yoga = PanchangCalculator.get_yoga(jd)
    assert "yoga_number" in yoga
    assert 1 <= yoga["yoga_number"] <= 27
