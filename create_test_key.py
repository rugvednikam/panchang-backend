import asyncio
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.api_key import APIKey
from app.models.user import User
from app.auth.security import generate_api_key

async def create_test_key():
    async with AsyncSessionLocal() as session:
        # Get any existing user to attach the key to
        result = await session.execute(select(User).limit(1))
        user = result.scalars().first()
        
        if not user:
            print("❌ No users found in the database. Please create a user first.")
            return

        # Generate a secure key
        plaintext_key, hashed_key = generate_api_key(prefix="pp_test_")
        
        # Store ONLY the hashed key and prefix in the database
        new_key = APIKey(
            hashed_key=hashed_key,
            key_prefix=plaintext_key[:12],
            user_id=user.id,
            name="Developer Test Key"
        )
        session.add(new_key)
        await session.commit()
        
        print("\n✅ SUCCESS: API Key Created Successfully!")
        print("\n=======================================================")
        print(f"API Key (Plaintext): {plaintext_key}")
        print("=======================================================\n")
        print("⚠️  PLEASE COPY THIS KEY NOW.")
        print("⚠️  We only stored the secure hash. The plaintext key will never be shown again.\n")

if __name__ == "__main__":
    asyncio.run(create_test_key())
