from datetime import datetime, timezone
from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import get_db
from app.models.api_key import APIKey
from app.auth.security import hash_api_key

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
    
    # Compare plaintext key directly to avoid environment mismatch with SECRET_KEY
    result = await db.execute(select(APIKey).where(APIKey.hashed_key == api_key_header))
    api_key_obj = result.scalars().first()
    
    if not api_key_obj:
        raise HTTPException(status_code=403, detail="Could not validate API key")
        
    if not api_key_obj.is_active:
        raise HTTPException(status_code=403, detail="API key is disabled")
        
    if api_key_obj.expires_at and api_key_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=403, detail="API key has expired")
        
    # Update usage tracking
    api_key_obj.total_requests += 1
    api_key_obj.last_used_at = datetime.now(timezone.utc)
    db.add(api_key_obj)
    await db.commit()
    
    return api_key_obj
