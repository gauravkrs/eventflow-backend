from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None  # fixed typo

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None

class EventOut(EventBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class EventCreateBatch(BaseModel):
    events: List[EventBase]
    
    class Config:
        from_attributes = True
        extra = "forbid"
