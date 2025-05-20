from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_respository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password, verify_password, create_access_token, 
    create_refresh_token, verify_token, get_token_expiration
)
from jose import JWTError
class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(self, user_data: UserCreate):

        existing = (
            self.user_repository.get_user_by_username(user_data.username)
            or self.user_repository.get_user_by_email(user_data.email)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        hashed_password = hash_password(user_data.password)
        user = self.user_repository.create_user(
             user_data, 
        )
        return user

    def login_user(self, username_or_email: str, password: str):
        user = (
            self.user_repository.get_user_by_email(username_or_email)
            or self.user_repository.get_user_by_username(username_or_email)
        )
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return user

    def create_tokens(self, user_id: int):
        access_token = create_access_token({"sub": str(user_id)})
        refresh_token = create_refresh_token({"sub": str(user_id)})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str):
        user_id = verify_token(refresh_token, scope="refresh_token")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        access_token = create_access_token({"sub": str(user_id)})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def logout_user(self, access_token: str) -> None:
        try:
            user_id = verify_token(access_token, scope="access_token")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

            if self.user_repository.is_token_blacklisted(self.db, access_token):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token already logged out"
                )

            expires_at = get_token_expiration(access_token)
            self.user_repository.add_blacklisted_token(self.db, access_token, expires_at)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or malformed token"
            )

