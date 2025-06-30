from datetime import datetime, UTC
import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import select, Session

from app.models.users import UserCreate, User
from app.services.base import BaseService, BaseDataManager
from app.utils.encryption import get_password_hash, verify_password


class UserDataManager(BaseDataManager):

    @staticmethod
    def get_active_user_by_username(session: Session, username: str) -> Optional[User]:
        existing_user = session.exec(
            select(User).where(
                (User.username == username), User.deleted_at.is_(None)
            )
        ).first()
        return existing_user

    @staticmethod
    def authenticate_user(session: Session, username: Optional[str, None], password: str) -> Optional[User, bool]:
        user = UserDataManager.get_active_user_by_username(session, username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def check_user_exist_with_username_and_email(self, username: str):
        existing_user = self.get_active_user_by_username(session=self.session, username=username)
        if existing_user:
            # if existing_user.email == email:
            #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            if existing_user.username == username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already registered")

    def create_user(self, user: UserCreate) -> User:
        self.check_user_exist_with_username_and_email(username=user.username)
        now = datetime.now(UTC)
        new_public_id = uuid.uuid4()
        encrypted_pwd = get_password_hash(user.password)
        user = User(
            **user.model_dump(exclude={"password"}),
            password=encrypted_pwd,
            public_id=new_public_id,
            created_by=new_public_id,
            updated_by=new_public_id,
            created_at=now,
            updated_at=now,
            deleted_by=None,
            deleted_at=None
        )
        return self.add_one(model=user)


class UserService(BaseService):
    def create_user(self, user: UserCreate):
        return UserDataManager(self.session).create_user(user)
