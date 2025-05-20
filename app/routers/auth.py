from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserOut, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.db.base import get_db
from app.core.security import create_access_token, create_refresh_token         

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model= UserResponse)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register_user(user_in)

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/login", response_model= UserResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.login_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    tokens = service.create_tokens(user.id)
    return UserResponse(
        email=user.email,
        username=user.username,
        access_token=tokens["access_token"],
        refresh_token=tokens.get("refresh_token"),
        token_type=tokens.get("token_type", "bearer")
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.refresh_access_token(refresh_token)

@router.post("/logout")
async def logout(db: Session = Depends(get_db), authorization: str = Header(...)):
    service = AuthService(db)
    try:
        token_type, access_token = authorization.split()
        if token_type.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")

    service.logout_user(access_token)
    return HTTPException(status_code=status.HTTP_200_OK, content={"message": "Logout successful"})