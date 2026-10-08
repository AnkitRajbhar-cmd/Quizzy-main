from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserInDB(UserCreate):
    id: Optional[PyObjectId] = Field(alias="_id")
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    correct_answer: str
    explanation: str

class QuizBase(BaseModel):
    title: str
    source_filename: str

class QuizCreate(QuizBase):
    questions: List[Question]

class QuizDB(QuizCreate):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = datetime.utcnow()
    user_id: str

class QuizPublic(QuizBase):
    id: str
    questions: List[dict] # Will hold stripped questions (no answer)
    created_at: datetime

class QuizSubmission(BaseModel):
    answers: dict[int, str] # {question_id: selected_option}

class QuizResult(BaseModel):
    score: int
    percentage: float
    analysis: List[dict] # Detailed breakdown
