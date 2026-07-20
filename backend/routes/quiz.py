from fastapi import APIRouter, Depends, HTTPException, status

from ai_match import match_coffee_with_ai
from dependencies import get_current_user
from models import User
from schemas import QuizAnswerItem, QuizMatchRequest, QuizMatchResponse

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/match", response_model=QuizMatchResponse)
def match_quiz_to_coffee(
    data: QuizMatchRequest,
    current_user: User = Depends(get_current_user),
):
    _ = current_user  # auth required; user identity unused for matching for now

    if len(data.answers) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one quiz answer is required",
        )

    drink, personalized_match = match_coffee_with_ai(
        [answer.model_dump() for answer in data.answers]
    )

    return QuizMatchResponse(
        drink_id=drink["id"],
        drink_name=drink["name"],
        description=drink["description"],
        categories=drink["categories"],
        personalized_match=personalized_match,
    )
