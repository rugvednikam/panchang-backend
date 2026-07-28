import time
from collections import defaultdict
from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In-memory rate limiter (Fixed window)
# For scalable multi-worker production, this should be backed by Redis.
_request_counts = defaultdict(list)

async def verify_rate_limit(api_key: str = Depends(api_key_header)):
    if not settings.RATE_LIMIT_ENABLED:
        return
        
    if not api_key:
        return  # The get_api_key dependency will handle the 403 Forbidden
        
    now = time.time()
    minute_ago = now - 60
    
    # Clean up requests older than 1 minute
    _request_counts[api_key] = [t for t in _request_counts[api_key] if t > minute_ago]
    
    if len(_request_counts[api_key]) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    _request_counts[api_key].append(now)
