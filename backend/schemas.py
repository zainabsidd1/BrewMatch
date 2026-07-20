from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime


class QuizAnswerItem(BaseModel):
    question_id: int
    question: str
    option_key: str = Field(min_length=1, max_length=1)
    option_label: str = Field(min_length=1)


class QuizMatchRequest(BaseModel):
    answers: list[QuizAnswerItem] = Field(min_length=1)


class QuizMatchResponse(BaseModel):
    drink_id: str
    drink_name: str
    description: str
    categories: list[str]
    personalized_match: str
