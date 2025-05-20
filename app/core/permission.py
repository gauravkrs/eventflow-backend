from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from sqlalchemy.orm import Session
from app.db.repositories.event_share_repository import EventShareRepository
from app.core.deps import get_current_user

def event_permission_middleware(db: Session):
    async def middleware(request: Request, call_next):
        path = request.url.path

        if path.startswith("/api/events"):
            parts = path.split("/")
            try:
                event_idx = parts.index("events") + 1
                event_id = int(parts[event_idx])
            except(ValueError, IndexError):
                return await call_next(request)
            
            user = await get_current_user(request)
            if not user:
                return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized User"})
            
            repo = PermissionRepository(db)
            share = repo.get_by_event_and_user(event_id, user.id)

            if not share: 
                return HTTPException(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Access denied"})
        
        return await call_next(request)
    
    return middleware
            
