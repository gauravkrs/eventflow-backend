from sqlalchemy.orm import Session
from app.models.event_version import EventVersion
from typing import Optional, List
from fastapi import HTTPException, status

class EventVersionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, event_id: int, version_id: int) -> Optional[EventVersion]:
        try:
            return (
                self.db.query(EventVersion)
                .filter(EventVersion.id == version_id, EventVersion.event_id == event_id)
                .first()
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch version")

    def list_versions(self, event_id: int) -> List[EventVersion]:
        try:
            return self.db.query(EventVersion).filter(EventVersion.event_id == event_id).all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list versions")

    def create(self, event_id: int, version_number: int, data: dict) -> EventVersion:
        try:
            version = EventVersion(event_id=event_id, version_number=version_number, data=data)
            self.db.add(version)
            self.db.commit()
            self.db.refresh(version)
            return version
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create version")

    def get_versions_by_event(self, event_id: int) -> List[EventVersion]:
        try:
            return (
                self.db.query(EventVersion)
                .filter(EventVersion.event_id == event_id)
                .order_by(EventVersion.version_number.asc())
                .all()
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch versions")
