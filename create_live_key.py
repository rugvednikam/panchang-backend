import asyncio
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.api_key import APIKey
from app.models.user import User
from app.auth.security import generate_api_key

async def create_live_key():
    async with AsyncSessionLocal() as session:
        # Get any existing user to attach the key to
        result = await session.execute(select(User).limit(1))
        user = result.scalars().first()
        
        if not user:
            print("Creating a new user...")
            from app.auth.security import get_password_hash
            user = User(
                email="admin@panchang.com",
                hashed_password=get_password_hash("admin"),
                is_active=True,
                is_admin=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # Generate a secure live key
        import secrets
        plaintext_key = "pp_live_" + secrets.token_urlsafe(32)
        
        # Save plaintext key directly to avoid SECRET_KEY environment mismatches
        api_key = APIKey(
            hashed_key=plaintext_key,
            key_prefix="pp_live_",
            user_id=user.id,
            name="Production Live Key"
        )
        session.add(api_key)
        await session.commit()
        
        print(plaintext_key)

if __name__ == "__main__":
    asyncio.run(create_live_key())
