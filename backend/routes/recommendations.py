from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import CoffeeLog, User
from personalized_recs import generate_personalized_recommendations
from schemas import PersonalizedRecommendationsResponse, TasteProfileResponse
from taste_profile import build_user_taste_profile, profile_public_dict

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/taste-profile", response_model=TasteProfileResponse)
def get_taste_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = list(
        db.scalars(
            select(CoffeeLog).where(CoffeeLog.user_id == current_user.id)
        ).all()
    )
    profile = build_user_taste_profile(logs)
    return TasteProfileResponse(**profile_public_dict(profile))


@router.get("/personalized", response_model=PersonalizedRecommendationsResponse)
def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = list(
        db.scalars(
            select(CoffeeLog).where(CoffeeLog.user_id == current_user.id)
        ).all()
    )
    payload = generate_personalized_recommendations(logs)
    return PersonalizedRecommendationsResponse(**payload)
