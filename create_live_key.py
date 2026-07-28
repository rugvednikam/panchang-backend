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
        plaintext_key, hashed_key = generate_api_key(prefix="pp_live_")
        
        # Store ONLY the hashed key and prefix in the database
        new_key = APIKey(
            hashed_key=hashed_key,
            key_prefix=plaintext_key[:12],
            user_id=user.id,
            name="Production Mobile App Key"
        )
        session.add(new_key)
        await session.commit()
        
        print(plaintext_key)

if __name__ == "__main__":
    asyncio.run(create_live_key())
