from fastapi import APIRouter
from app.api.endpoints import auth, astrology, advanced_astrology, languages, v28_4_endpoints, v29_endpoints

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(astrology.router, prefix="/astrology", tags=["astrology"])
api_router.include_router(advanced_astrology.router, prefix="/advanced", tags=["advanced_astrology"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])
api_router.include_router(v28_4_endpoints.router, prefix="/v28_4", tags=["v28_4"])
api_router.include_router(v29_endpoints.router, prefix="/v29", tags=["v29"])
