from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.api import api_router
from app.database.session import engine
from app.models.base import Base
from fastapi import Depends
from app.auth.api_key import get_api_key
from app.auth.rate_limit import verify_rate_limit
from app.database.session import engine
from app.models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(
    api_router, 
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_api_key), Depends(verify_rate_limit)]
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hindu Astrology REST API"}
