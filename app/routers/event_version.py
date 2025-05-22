from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.event_version import EventVersionOut, ChangelogOut, DiffOut
from app.services.event_version_service import EventVersionService
from typing import Any
from app.schemas.event import EventOut


router = APIRouter(prefix="/api/events", tags=["Event Version"])

@router.get("/{id}/history/{versionId}", response_model=EventVersionOut)
async def get_version(id: int, version_id: int, db: Session = Depends(get_db)):
    try:
        return EventVersionService(db).get_version_by_id(id, version_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

@router.post("/{id}/rollback/{versionId}", response_model=EventOut, status_code=status.HTTP_200_OK)
async def rollback_version(id: int, versionId: int, db: Session = Depends(get_db)):
    try:
        return EventVersionService(db).rollback_to_version(id, versionId)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    

@router.get("/{event_id}/changelog", response_model=ChangelogOut)
async def get_changelog(event_id: int, db: Session = Depends(get_db)):
    try:
        service = EventVersionService(db)
        versions = service.get_changgelog(event_id)
        if not versions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event or versions not found")
        return {"versions": versions}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    

@router.get("/{event_id}/diff/{v1_id}/{v2_id}", response_model=DiffOut)
async def get_diff(event_id: int, v1_id: int, v2_id: int, db: Session = Depends(get_db)):
    service = EventVersionService(db)
    try:
        differences = service.get_diff(event_id, v1_id, v2_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"differences": differences}