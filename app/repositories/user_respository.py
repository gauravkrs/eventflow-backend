from sqlalchemy.orm import Session
from app.models.user import User, TokenBlacklist
from app.schemas.user import UserCreate
from app.core.security import hash_password
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        hashed_password = hash_password(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def add_blacklisted_token(self, token: str, expires_at: datetime) -> None:
        blacklist_entry = TokenBlacklist(token=token, expires_at=expires_at)
        self.db.add(blacklist_entry)
        self.db.commit()

    def is_token_blacklisted(self, token: str) -> bool:
        return (
            self.db.query(TokenBlacklist)
            .filter(TokenBlacklist.token == token)
            .first()
            is not None
        )