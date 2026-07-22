from pydantic import BaseModel
from typing import Optional

class AstrologicalInput(BaseModel):
    name: str
    dob: str # Format YYYY-MM-DD
    time: str # Format HH:MM:SS
    latitude: float
    longitude: float
    timezone: str # e.g. 'Asia/Kolkata'
    ayanamsa: Optional[str] = "Lahiri"
    siddhant: Optional[str] = "Drik Siddhant"

class MatchMakingInput(BaseModel):
    boy_name: str
    boy_dob: str
    boy_time: str
    boy_latitude: float
    boy_longitude: float
    boy_timezone: str
    girl_name: str
    girl_dob: str
    girl_time: str
    girl_latitude: float
    girl_longitude: float
    girl_timezone: str
    ayanamsa: Optional[str] = "Lahiri"
    siddhant: Optional[str] = "Drik Siddhant"

class DateLocationInput(BaseModel):
    date: str # YYYY-MM-DD
    latitude: float
    longitude: float
    timezone: str
