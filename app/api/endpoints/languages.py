from fastapi import APIRouter
from app.core.languages_20 import LANGUAGES, LANG_NAMES

router = APIRouter()

@router.get("/20-list")
async def get_20_languages_list():
    return {
        "languages_20": LANGUAGES,
        "names": LANG_NAMES,
        "note": "20 languages compatible with everything - Panchang, Muhurta, Saham, Dasha, Charts",
        "count": len(LANGUAGES)
    }
