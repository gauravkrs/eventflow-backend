from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.services.collaboration_service import CollaborationService
from app.db.base import get_db

router = APIRouter(prefix="/api/events", tags=["Collaboration"])

@router.post("/{event_id}/share", response_model=PermissionResponse)
async def share_event(event_id: int, payload: PermissionCreate, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.share_event(event_id, payload.user_id, payload.role)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to share event")

@router.get("/{event_id}/permissions", response_model=List[PermissionResponse])
async def list_permissions(event_id: int, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.list_permission(event_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch permissions")

@router.put("/{event_id}/permissions/{user_id}", response_model=PermissionResponse)
async def update_permission(event_id: int, user_id: int, payload: PermissionUpdate, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.update_permission(event_id, user_id, payload.role)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update permission")

@router.delete("/{event_id}/permissions/{user_id}")
async def remove_permission(event_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        service.remove_permission(event_id, user_id)
        return {"message": "Permission removed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove permission")
