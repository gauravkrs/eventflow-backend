from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.event import Event
from app.schemas.event import EventBase, EventUpdate

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: EventBase) -> Event:
        event = Event(
            owner_id=user_id,
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            location=data.location,
            is_recurring=data.is_recurring,
            recurrence_pattern=data.recurrence_pattern,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def list_by_user(self, user_id: int) -> List[Event]:
        return self.db.query(Event).filter(Event.owner_id == user_id)

    def get(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def update(self, event_id: int, data: EventUpdate) -> Optional[Event]:
        event = self.get(event_id)
        if event:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(event, key, value)
            self.db.commit()
            self.db.refresh(event)
        return event
    
    def create_batch(self, events_data: List[EventBase], owner_id:int) -> List[Event]:
        events = [Event(**e.dict(), owner_id = owner_id) for e in events_data]
        self.db.add_all(events)
        self.db.commit()
        for event in events:
            self.db.refresh(event)
        return events
    
    def delete(self, event_id: int) -> bool:
        event = self.get(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False