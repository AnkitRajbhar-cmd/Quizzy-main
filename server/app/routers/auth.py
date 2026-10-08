from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.schemas import UserCreate, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.database import users_collection
from datetime import timedelta

router = APIRouter()

@router.post('/signup')
async def signup(user: UserCreate):
    existing = await users_collection.find_one({'email': user.email})
    if existing:
        raise HTTPException(status_code=400, detail='User already exists')
    user_dict = user.dict()
    user_dict['hashed_password'] = get_password_hash(user_dict.pop('password'))
    new = await users_collection.insert_one(user_dict)
    return {'id': str(new.inserted_id), 'email': user.email}

@router.post('/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({'email': form_data.username})
    if not user or not verify_password(form_data.password, user.get('hashed_password')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect credentials')
    access_token = create_access_token({'sub': str(user['_id'])}, expires_delta=timedelta(minutes=60))
    return {'access_token': access_token, 'token_type': 'bearer'}


# JSON-friendly login endpoint (used by the React client)
from pydantic import BaseModel
from pydantic import EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post('/login', response_model=Token)
async def login(request: LoginRequest):
    user = await users_collection.find_one({'email': request.email})
    if not user or not verify_password(request.password, user.get('hashed_password')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect credentials')
    access_token = create_access_token({'sub': str(user['_id'])})
    return {'access_token': access_token, 'token_type': 'bearer'}
