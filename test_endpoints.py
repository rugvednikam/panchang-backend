import asyncio
from httpx import AsyncClient
from app.main import app

async def test_endpoints():
    # The API key you just generated
    headers = {"x-api-key": "pp_test_vOL9iPznNgjh2vNq8n-huWj3kTupu7oBJiW7Go6Vrm8"}

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        print("\n--- 1. Testing WITHOUT API Key (Should be 403 Forbidden) ---")
        res_fail = await client.post("/api/v1/v29/panchang/ayanamsa/all-options")
        print(f"Status: {res_fail.status_code}\n")

        print("--- 2. Testing WITH API Key (Should be 200 OK) ---")
        # Test a v28.4 endpoint
        res = await client.post("/api/v1/v28_4/kp/prashna-1-249", headers=headers)
        print(f"V28.4 /kp/prashna-1-249: {res.status_code}")
        print(res.json())

        # Test a v29 endpoint
        res2 = await client.post("/api/v1/v29/panchang/ayanamsa/all-options", headers=headers)
        print(f"V29 /panchang/ayanamsa/all-options: {res2.status_code}")
        print(res2.json())

if __name__ == "__main__":
    asyncio.run(test_endpoints())
