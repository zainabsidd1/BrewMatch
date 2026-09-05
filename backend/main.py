from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import cors_origins
from database import Base, engine
import models  # noqa: F401 — registers the User model with SQLAlchemy
from routes.auth import router as auth_router
from routes.calendar import router as calendar_router
from routes.quiz import router as quiz_router
from routes.recommendations import router as recommendations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="BrewMatch API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(quiz_router)
app.include_router(calendar_router)
app.include_router(recommendations_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
