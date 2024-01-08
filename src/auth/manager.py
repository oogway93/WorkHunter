from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import Request
from fastapi.openapi.models import Response
from fastapi_users import BaseUserManager
from fastapi_users import IntegerIDMixin
from fastapi_users import InvalidPasswordException
from fastapi_users.jwt import generate_jwt

from config import RESET_SECRET
from src.auth.database import User
from src.auth.database import get_user_db
from src.auth.schemas import UserCreate
from src.tasks.tasks import send_registration_email
from src.tasks.tasks import send_reset_email

SECRET = RESET_SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User Manager."""

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        token_data = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        send_registration_email("Email Confirmation", user.email, token, user.username)
        return {"msg": "Let's check an email address"}

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        send_reset_email("Reset Password", user.email, token)
        return {"msg": "Let's check an email address"}

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        print(f"User {user.id} logged in.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
