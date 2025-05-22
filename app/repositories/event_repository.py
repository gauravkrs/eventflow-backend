from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.event import Event
from app.models.event_version import EventVersion
from app.schemas.event import EventBase, EventUpdate
import json
from pydantic.json import pydantic_encoder
from fastapi import HTTPException, status

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: int, data: EventBase) -> Event:
        try:
            event = Event(**data.dict(), owner_id=owner_id)
            self.db.add(event)
            self.db.flush()
            self.create_event_version(event.id, 1, data.dict(), owner_id)
            return event
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create event")

    def get(self, event_id: int) -> Optional[Event]:
        try:
            return self.db.query(Event).filter(Event.id == event_id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch event")

    def list_by_user(self, user_id: int) -> List[Event]:
        try:
            return self.db.query(Event).filter(Event.owner_id == user_id).all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list events")

    def update(self, event_id: int, data: EventUpdate) -> Optional[Event]:
        try:
            event = self.get(event_id)
            if not event:
                return None
            for field, value in data.dict(exclude_unset=True).items():
                if value is not None:
                    setattr(event, field, value)
            self.db.flush()
            latest_version = (
                self.db.query(EventVersion)
                .filter(EventVersion.event_id == event_id)
                .order_by(EventVersion.version_number.desc())
                .first()
            )
            next_version = 1 if not latest_version else latest_version.version_number + 1
            self.create_event_version(event_id, next_version, data.dict(exclude_unset=True), event.owner_id)
            return event
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update event")

    def create_batch(self, events_data: List[EventBase], owner_id: int) -> List[Event]:
        try:
            events = [Event(**data.dict(), owner_id=owner_id) for data in events_data]
            self.db.add_all(events)
            self.db.flush()
            return events
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create batch events")

    def delete(self, event_id: int) -> bool:
        try:
            event = self.get(event_id)
            if not event:
                return False
            self.db.delete(event)
            self.db.flush()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete event")

    def create_event_version(self, event_id: int, version_number: int, data: dict, created_by: int) -> EventVersion:
        try:
            version = EventVersion(
                event_id=event_id,
                version_number=version_number,
                version_data=json.loads(json.dumps(data, default=pydantic_encoder)),
                created_by=created_by
            )
            self.db.add(version)
            self.db.flush()
            return version
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create event version")
