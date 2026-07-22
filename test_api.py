import sys
import os
import asyncio
from datetime import datetime

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.schemas.astrology import AstrologicalInput
from app.api.endpoints.astrology import get_kundli

async def main():
    input_data = AstrologicalInput(
        name="Rugved",
        dob="1995-10-25",
        time="14:30:00",
        latitude=19.076,
        longitude=72.8777,
        timezone="Asia/Kolkata",
        ayanamsa="Lahiri"
    )
    
    try:
        res = await get_kundli(input_data, api_key="dummy")
        print("Success!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
