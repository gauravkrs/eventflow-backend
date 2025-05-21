from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from app.schemas.permission import PermissionCreate,PermissionUpdate, PermissionResponse, RoleEnum
from app.services.collaboration_service import CollaborationService
from app.db.base import get_db
from app.models.permission import Permission

router = APIRouter(prefix="/api/events", tags=["Collaboration"])

logger = logging.getLogger(__name__)

@router.post("/{event_id}/share", response_model= PermissionResponse)
async def share_event(event_id: int, payload:PermissionCreate, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.share_event(event_id, payload.user_id, payload.role)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Failed to share event")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/{event_id}/permissions", response_model= List[PermissionResponse])
async def list_permissions(event_id: int, db: Session = Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.list_permission(event_id)
    except Exception as e:
        logger.exception("Failed to list permissions")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.put("/{event_id}/permissions/{user_id}", response_model= PermissionResponse)
async def update_permission(event_id: int, user_id: int, payload: PermissionUpdate, db: Session =Depends(get_db)):
    try:
        service = CollaborationService(db)
        return service.update_permission(event_id, user_id, payload.role)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Failed to update permission")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.delete("/{event_id}/permissions/{user_id}")
async def remove_permission(event_id: int, user_id: int, db: Session= Depends(get_db)):
    try:
        service = CollaborationService(db)
        service.remove_permission(event_id, user_id)
        return {"message": "Permission removed"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Failed to remove permission")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

