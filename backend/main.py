from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from config import cors_origin_regex, cors_origins
from database import Base, engine
import models  # noqa: F401 — registers the User model with SQLAlchemy
from routes.auth import router as auth_router
from routes.calendar import router as calendar_router
from routes.catalog import router as catalog_router
from routes.quiz import router as quiz_router
from routes.recommendations import router as recommendations_router


def _ensure_coffee_log_temperature_column() -> None:
    inspector = inspect(engine)
    if "coffee_logs" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("coffee_logs")}
    if "temperature" in columns:
        return
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE coffee_logs ADD COLUMN temperature VARCHAR(8)")
        )


def _ensure_user_name_column() -> None:
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("users")}
    if "name" in columns:
        return
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(80)"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _ensure_coffee_log_temperature_column()
    _ensure_user_name_column()
    yield


app = FastAPI(title="BrewMatch API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_origin_regex=cors_origin_regex(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(quiz_router)
app.include_router(calendar_router)
app.include_router(catalog_router)
app.include_router(recommendations_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
