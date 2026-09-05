from datetime import date, datetime

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


class CoffeeLogCreate(BaseModel):
    drink_id: str = Field(min_length=1, max_length=64)
    drink_name: str = Field(min_length=1, max_length=120)
    rating: int = Field(ge=1, le=5)
    date_tried: date | None = None
    notes: str | None = Field(default=None, max_length=500)
    is_favorite: bool = False
    source: str = Field(default="brewmatch_recommendation", max_length=64)


class CoffeeLogUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    notes: str | None = Field(default=None, max_length=500)
    is_favorite: bool | None = None
    date_tried: date | None = None


class CoffeeLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    drink_id: str
    drink_name: str
    date_added: datetime
    date_tried: date
    rating: int | None
    notes: str | None
    is_favorite: bool
    source: str
    temperature_tag: str | None = None


class CalendarDayEntry(BaseModel):
    date: date
    entries: list[CoffeeLogResponse]


class CalendarMonthResponse(BaseModel):
    year: int
    month: int
    days: list[CalendarDayEntry]


class CoffeeJourneyStats(BaseModel):
    streak_days: int
    coffees_tried: int
    favorite_drink: str | None
    favorite_drink_avg_rating: float | None


class TemperatureMix(BaseModel):
    iced: int = 0
    hot: int = 0


class SweetnessMix(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0


class TasteProfileResponse(BaseModel):
    preferred_temperature: str | None = None
    sweetness: str | None = None
    preferred_flavors: list[str] = []
    strength: str | None = None
    milk_preference: str | None = None
    confidence: str
    rated_count: int
    temperature_mix: TemperatureMix
    sweetness_mix: SweetnessMix


class PersonalizedDrinkResponse(BaseModel):
    drink_id: str
    base_drink: str
    display_name: str
    temperature: str
    sweetness: str
    syrup: str | None = None
    modifier: str | None = None
    explanation: str


class PersonalizedRecommendationsResponse(BaseModel):
    taste_profile: TasteProfileResponse
    what_you_might_like: PersonalizedDrinkResponse | None = None
    try_something_new: PersonalizedDrinkResponse | None = None
    message: str | None = None

