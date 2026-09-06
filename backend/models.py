from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    coffee_logs: Mapped[list["CoffeeLog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class CoffeeLog(Base):
    """A coffee the user saved/tried — the coffee journal entry."""

    __tablename__ = "coffee_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    drink_id: Mapped[str] = mapped_column(String(64), index=True)
    drink_name: Mapped[str] = mapped_column(String(120))

    date_added: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    date_tried: Mapped[date] = mapped_column(Date, index=True)

    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    source: Mapped[str] = mapped_column(
        String(64),
        default="brewmatch_recommendation",
    )
    temperature: Mapped[str | None] = mapped_column(String(8), nullable=True)

    user: Mapped["User"] = relationship(back_populates="coffee_logs")
