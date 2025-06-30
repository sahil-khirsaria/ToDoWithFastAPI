from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.configs.db import get_session
from app.models.users import User, UserCreate
from app.services.users import UserService

user_router = APIRouter()


@user_router.post("/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return UserService(session=session).create_user(user)
