from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import get_db  
from app.core.security import verify_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    print(token)
    user_id = verify_token(token, scope="access_token")
    print(user_id)
    if user_id is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user