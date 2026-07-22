from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.config import settings
from app.auth.security import verify_password
from app.auth.jwt import create_access_token
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.services.user_service import get_user_by_email, create_user

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=User)
async def register_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await create_user(db, user_in=user_in)
    return user

@router.post("/api-key")
async def generate_api_key(
    email: str,
    name: str = "Default Key",
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    Generate a new API key for testing by providing your registered email.
    """
    import secrets
    from app.models.api_key import APIKey
    
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    new_key = secrets.token_urlsafe(32)
    db_obj = APIKey(
        key=new_key,
        user_id=user.id,
        name=name
    )
    db.add(db_obj)
    await db.commit()
    
    return {"api_key": new_key, "name": name}
