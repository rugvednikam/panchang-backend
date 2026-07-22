from fastapi import APIRouter
from app.api.endpoints import auth, astrology, advanced_astrology, languages

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(astrology.router, prefix="/astrology", tags=["astrology"])
api_router.include_router(advanced_astrology.router, prefix="/advanced", tags=["advanced_astrology"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])

