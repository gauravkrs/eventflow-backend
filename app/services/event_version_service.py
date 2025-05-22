from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.event_version_repository import EventVersionRepository
from app.repositories.event_repository import EventRepository
from app.models import Event, EventVersion
from typing import List, Dict, Any

class EventVersionService:
    def __init__(self, db: Session):
        self.db = db
        self.version_repo = EventVersionRepository(db)
        self.event_repo = EventRepository(db)

    def get_version_by_id(self, event_id: int, version_id: int) -> EventVersion:
        try:
            version = self.version_repo.get_by_id(event_id, version_id)
            if not version:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Version not found"
                )
            return version
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching version: {str(e)}"
            )

    def rollback_to_version(self, event_id: int, version_id: int) -> Event:
        try:
            version = self.version_repo.get_by_id(event_id, version_id)
            if not version:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Version not found"
                )

            event = self.event_repo.get(event_id)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )

            for key in [
                'title', 'description', 'start_time', 'end_time',
                'location', 'is_recurring', 'recurrence_pattern'
            ]:
                if key in version.version_data:
                    setattr(event, key, version.version_data[key])

            self.db.commit()
            self.db.refresh(event)
            return event
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rollback failed: {str(e)}"
            )

    def get_changgelog(self, event_id: int) -> List[EventVersion]:
        try:
            versions = self.version_repo.get_versions_by_event(event_id)
            if not versions:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No versions found for the event"
                )
            return versions
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get changelog: {str(e)}"
            )

    def get_diff(self, event_id: int, v1_id: int, v2_id: int) -> Dict[str, Dict[str, Any]]:
        try:
            v1 = self.get_version_by_id(event_id, v1_id)
            v2 = self.get_version_by_id(event_id, v2_id)

            diff = {}
            data1 = v1.version_data
            data2 = v2.version_data

            all_keys = set(data1.keys()).union(data2.keys())
            for key in all_keys:
                val1 = data1.get(key)
                val2 = data2.get(key)
                if val1 != val2:
                    diff[key] = {"from": val1, "to": val2}

            return diff
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to compute diff: {str(e)}"
            )
