from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.api_key import APIKey

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
    db: AsyncSession = Depends(get_db)
):
    if not api_key_header:
        raise HTTPException(
            status_code=403, detail="Could not validate API key"
        )
    
    result = await db.execute(select(APIKey).where(APIKey.key == api_key_header))
    api_key_obj = result.scalars().first()
    
    if not api_key_obj or not api_key_obj.is_active:
        raise HTTPException(
            status_code=403, detail="Could not validate API key"
        )
        
    # Increment usage counter
    api_key_obj.total_requests += 1
    db.add(api_key_obj)
    await db.commit()
    
    return api_key_obj
