from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.core.database import engine

from app.core.exception_handlers import register_exception_handlers
from app.middleware.middleware import register_middleware
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-flutter-domain.com",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
# register_middleware(app)