from fastapi import HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.repositories.event_repository import EventRepository
from app.repositories.collaboration_repository import CollaborationRepository
from app.schemas.event import EventBase, EventUpdate, EventCreateBatch
from app.models.changelog import Changelog
from app.models.permission import RoleEnum
from app.models.event import Event
from datetime import datetime

class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EventRepository(db)
        self.collab_repo = CollaborationRepository(db)

    def create_event(self, user_id: int, data: EventBase) -> Event:
        try:
            event = self.repo.create(user_id, data)
            self.collab_repo.create_role(event.id, user_id, RoleEnum.owner)
            changelog = Changelog(
                event_id=event.id,
                version_id=None,
                changes={},
                description="Event created",
                created_by=user_id
            )
            self.db.add(changelog)
            self.db.commit()
            self.db.refresh(event)
            return event
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create event: {str(e)}"
            )

    def get_event(self, event_id: int, requester_id: int) -> Optional[Event]:
        try:
            event = self.repo.get(event_id)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            permission = self.collab_repo.get_by_event_and_user(event_id, requester_id)
            if not permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied"
                )
            return event
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve event: {str(e)}"
            )

    def list_events(self, user_id: int) -> List[Event]:
        try:
            return self.repo.list_by_user(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list events: {str(e)}"
            )

    def update_event(self, event_id: int, data: EventUpdate, user_id: int) -> Event:
        try:
            permission = self.collab_repo.get_by_event_and_user(event_id, user_id)
            if not permission or permission.role not in [RoleEnum.owner, RoleEnum.editor]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied"
                )

            event = self.repo.update(event_id, data)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            self.db.commit()
            return event
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update event: {str(e)}"
            )

    def create_batch(self, data: EventCreateBatch, owner_id: int) -> List[Event]:
        try:
            events = self.repo.create_batch(data.events, owner_id)
            self.db.commit()
            return events
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create events in batch: {str(e)}"
            )

    def delete_event(self, event_id: int):
        try:
            success = self.repo.delete(event_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event not found"
                )
            self.db.commit()
            return {"detail": "Deleted"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete event: {str(e)}"
            )

    def get_event_with_versions(self, event_id: int) -> Optional[Event]:
        try:
            event = self.db.query(Event)\
                .options(joinedload(Event.versions))\
                .filter(Event.id == event_id)\
                .first()
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Event with versions not found"
                )
            return event
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get event with versions: {str(e)}"
            )
