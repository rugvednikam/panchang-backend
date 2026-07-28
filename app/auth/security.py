from passlib.context import CryptContext
import hmac
import hashlib
import secrets
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def hash_api_key(api_key: str) -> str:
    """Hash an API key using HMAC-SHA256 and the application's SECRET_KEY."""
    return hmac.new(
        settings.SECRET_KEY.encode(),
        api_key.encode(),
        hashlib.sha256
    ).hexdigest()

def generate_api_key(prefix: str = "pp_live_") -> tuple[str, str]:
    """
    Generate a cryptographically secure API key.
    Returns: (plaintext_key, hashed_key)
    """
    token = secrets.token_urlsafe(32)
    plaintext_key = f"{prefix}{token}"
    hashed_key = hash_api_key(plaintext_key)
    return plaintext_key, hashed_key
