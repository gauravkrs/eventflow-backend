from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventBase, EventUpdate, EventCreateBatch
from fastapi import HTTPException, status
from app.models.event import Event

class EventService:
    def __init__(self, db: Session):
        self.repo = EventRepository(db)

    def create_event(self, user_id: int, data: EventBase):
        return self.repo.create(user_id, data)
    
    def get_event(self, event_id: int):
        event = self.repo.get(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event
    
    def list_events(self, user_id:int):
        return self.repo.list_by_user(user_id)
    
    def update_event(self, event_id: int, data: EventUpdate):
        event = self.repo.update(event_id, data)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return event
    
    def create_batch(self, data: EventCreateBatch, owner_id: int) -> list[Event]:
        try:
            return self.repo.create_batch(data.events, owner_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_event(self, event_id: int):
        if not self.repo.delete(event_id):
            raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        return {"detail": "Deleted"}
    
