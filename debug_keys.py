import asyncio
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.api_key import APIKey
from app.auth.security import hash_api_key

async def main():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(APIKey))
        keys = res.scalars().all()
        for k in keys:
            print(f"ID: {k.id}, Active: {k.is_active}, Hash: {k.hashed_key}, User: {k.user_id}")

asyncio.run(main())
