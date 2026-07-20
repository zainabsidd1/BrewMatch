from collections import defaultdict
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import CoffeeLog, User
from schemas import (
    CalendarDayEntry,
    CalendarMonthResponse,
    CoffeeJourneyStats,
    CoffeeLogCreate,
    CoffeeLogResponse,
    CoffeeLogUpdate,
)

router = APIRouter(prefix="/calendar", tags=["calendar"])


def _compute_streak(tried_dates: set[date]) -> int:
    if not tried_dates:
        return 0

    today = date.today()
    cursor = today if today in tried_dates else today - timedelta(days=1)
    if cursor not in tried_dates:
        return 0

    streak = 0
    while cursor in tried_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def _favorite_drink(logs: list[CoffeeLog]) -> tuple[str | None, float | None]:
    rated = [log for log in logs if log.rating is not None]
    if not rated:
        return None, None

    by_drink: dict[str, list[int]] = defaultdict(list)
    for log in rated:
        by_drink[log.drink_name].append(int(log.rating))

    best_name = None
    best_avg = -1.0
    best_count = 0
    for name, ratings in by_drink.items():
        avg = sum(ratings) / len(ratings)
        if avg > best_avg or (avg == best_avg and len(ratings) > best_count):
            best_name = name
            best_avg = avg
            best_count = len(ratings)

    return best_name, round(best_avg, 1) if best_name else None


@router.post("/logs", response_model=CoffeeLogResponse, status_code=status.HTTP_201_CREATED)
def create_coffee_log(
    data: CoffeeLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = CoffeeLog(
        user_id=current_user.id,
        drink_id=data.drink_id,
        drink_name=data.drink_name,
        date_tried=data.date_tried or date.today(),
        rating=data.rating,
        notes=data.notes,
        is_favorite=data.is_favorite,
        source=data.source,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/logs", response_model=list[CoffeeLogResponse])
def list_coffee_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = db.scalars(
        select(CoffeeLog)
        .where(CoffeeLog.user_id == current_user.id)
        .order_by(CoffeeLog.date_tried.desc(), CoffeeLog.id.desc())
    ).all()
    return list(logs)


@router.patch("/logs/{log_id}", response_model=CoffeeLogResponse)
def update_coffee_log(
    log_id: int,
    data: CoffeeLogUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = db.get(CoffeeLog, log_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")

    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffee_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = db.get(CoffeeLog, log_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")

    db.delete(entry)
    db.commit()


@router.get("/month", response_model=CalendarMonthResponse)
def get_calendar_month(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

    logs = db.scalars(
        select(CoffeeLog)
        .where(
            CoffeeLog.user_id == current_user.id,
            CoffeeLog.date_tried >= start,
            CoffeeLog.date_tried < end,
        )
        .order_by(CoffeeLog.date_tried.asc(), CoffeeLog.id.asc())
    ).all()

    by_day: dict[date, list[CoffeeLog]] = defaultdict(list)
    for log in logs:
        by_day[log.date_tried].append(log)

    days = [
        CalendarDayEntry(
            date=day,
            entries=[CoffeeLogResponse.model_validate(entry) for entry in entries],
        )
        for day, entries in sorted(by_day.items())
    ]

    return CalendarMonthResponse(year=year, month=month, days=days)


@router.get("/stats", response_model=CoffeeJourneyStats)
def get_coffee_journey_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = list(
        db.scalars(
            select(CoffeeLog).where(CoffeeLog.user_id == current_user.id)
        ).all()
    )
    tried_dates = {log.date_tried for log in logs}
    favorite_name, favorite_avg = _favorite_drink(logs)

    return CoffeeJourneyStats(
        streak_days=_compute_streak(tried_dates),
        coffees_tried=len(logs),
        favorite_drink=favorite_name,
        favorite_drink_avg_rating=favorite_avg,
    )
