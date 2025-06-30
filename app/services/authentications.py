from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from app.models.authentications import Token
from app.services.base import BaseDataManager
from app.services.users import UserDataManager
from app.utils.authentication import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Login(BaseDataManager):

    def login_for_access_token(
            self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        user = UserDataManager.authenticate_user(self.session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")
